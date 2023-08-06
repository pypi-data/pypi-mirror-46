#include "dreal/solver/icp_parallel.h"

#include <atomic>
#include <thread>
#include <tuple>

#include "dreal/solver/branch.h"
#include "dreal/solver/icp_stat.h"
#include "dreal/util/interrupt.h"
#include "dreal/util/logging.h"
#include "dreal/util/thread.h"

using std::pair;
using std::tie;
using std::vector;

namespace dreal {

namespace {

bool ParallelBranch(const ibex::BitSet& bitset, const bool stack_left_box_first,
                    Box* const box, Stack<Box::IntervalVector>* const stack) {
  // TODO(soonho): For now, we fixated the branching heuristics.
  // Generalize it later.
  const pair<double, int> max_diam_and_idx{FindMaxDiam(*box, bitset)};
  const int branching_point{max_diam_and_idx.second};
  if (branching_point >= 0) {
    const auto boxes1 = box->interval_vector().bisect(branching_point, 0.33333);
    const auto boxes2 = boxes1.second.bisect(branching_point);
    const Box::IntervalVector& iv1{boxes1.first};
    const Box::IntervalVector& iv2{boxes2.first};
    const Box::IntervalVector& iv3{boxes2.second};
    if (stack_left_box_first) {
      DREAL_LOG_DEBUG(
          "Branch {}\n"
          "on {}\n"
          "Box1=\n{}\n"
          "Box2=\n{}\n"
          "Box3=\n{}",
          *box, box->variable(branching_point), iv1, iv2, iv3);
      stack->push(iv1);
      stack->push(iv2);
      box->mutable_interval_vector() = iv3;
    } else {
      DREAL_LOG_DEBUG(
          "Branch {}\n"
          "on {}\n"
          "Box1=\n{}\n"
          "Box2=\n{}\n"
          "Box3=\n{}",
          *box, box->variable(branching_point), iv3, iv2, iv1);
      stack->push(iv3);
      stack->push(iv2);
      box->mutable_interval_vector() = iv1;
    }
    return true;
  }
  // Fail to find a branching point.
  return false;
}

// Returns -1 if it detects that the interval vector is non-bisectable.
int FindMaxDiamIdx(const Box::IntervalVector& iv) {
  double max_diam{0.0};
  int max_diam_idx{-1};
  for (int i = 0; i < iv.size(); ++i) {
    const Box::Interval& iv_i{iv[i]};
    const double diam_i{iv_i.diam()};
    if (diam_i > max_diam && iv_i.is_bisectable()) {
      max_diam_idx = i;
    }
  }
  return max_diam_idx;
}

vector<Box::IntervalVector> DoubleUp(
    const vector<Box::IntervalVector>& interval_vectors) {
  vector<Box::IntervalVector> ret;
  ret.reserve(interval_vectors.size() * 2);
  for (const auto& iv : interval_vectors) {
    const int max_diam_idx{FindMaxDiamIdx(iv)};
    if (max_diam_idx >= 0) {
      const auto bisect_result = iv.bisect(max_diam_idx);
      ret.push_back(bisect_result.first);
      ret.push_back(bisect_result.second);
    }
  }
  return ret;
}

vector<Box::IntervalVector> FillUp(const Box::IntervalVector& iv, int n) {
  vector<Box::IntervalVector> ret;
  ret.push_back(iv);
  while (ret.size() <= static_cast<unsigned>(n)) {
    vector<Box::IntervalVector> new_ones{DoubleUp(ret)};
    if (new_ones.size() == ret.size()) {
      break;
    } else {
      ret = new_ones;
    }
  }
  return ret;
}

void Worker(const Contractor& contractor, const Config& config,
            const vector<FormulaEvaluator>& formula_evaluators,
            const unsigned id, const bool main_thread,
            Stack<Box::IntervalVector>* const stack, ContractorStatus* const cs,
            std::atomic_bool* const found_delta_sat,
            std::atomic<int>* const number_of_boxes,
            std::atomic<int>* const winner_thread, IcpStat* const stat) {
  CdsScopeGuard cds_scope_guard(!main_thread);

  bool stack_left_box_first = config.stack_left_box_first();

  // `current_box` always points to the box in the contractor status
  // as a mutable reference.
  Box& current_box{cs->mutable_box()};

  bool need_to_pop{true};

  while (!(*found_delta_sat) && *number_of_boxes > 0) {
    DREAL_LOG_INFO("IcpParallel::Worker() Loop Head {}, {}", *found_delta_sat,
                   *number_of_boxes);

    // Note that 'DREAL_CHECK_INTERRUPT' is only defined in setup.py,
    // when we build dReal python package.
#ifdef DREAL_CHECK_INTERRUPT
    // TODO(soonho): Enable this.
    //
    // if (g_interrupted) {
    //   DREAL_LOG_DEBUG("KeyboardInterrupt(SIGINT) Detected.");
    //   throw std::runtime_error("KeyboardInterrupt(SIGINT) Detected.");
    // }
#endif

    // 1. Pop the current box from the stack
    if (need_to_pop &&
        !stack->pop(cs->mutable_box().mutable_interval_vector())) {
      DREAL_LOG_INFO("IcpParallel::Worker() NO BOX.");
      std::this_thread::yield();
      continue;
    }

    need_to_pop = true;

    // 2. Prune the current box.
    DREAL_LOG_TRACE("IcpParallel::Worker() Current Box:\n{}", current_box);
    contractor.Prune(cs);
    stat->increase_prune();
    DREAL_LOG_TRACE(
        "IcpParallel::Worker() After pruning, the current box =\n{}",
        current_box);

    if (current_box.empty()) {
      // 3.1. The box is empty after pruning.
      --(*number_of_boxes);
      DREAL_LOG_INFO("IcpParallel::Worker() Box is empty after pruning");
      continue;
    }
    // 3.2. The box is non-empty. Check if the box is still feasible
    // under evaluation and it's small enough.
    const optional<ibex::BitSet> evaluation_result{
        EvaluateBox(formula_evaluators, current_box, config.precision(), cs)};
    if (!evaluation_result) {
      // 3.2.1. We detect that the current box is not a feasible solution.
      --(*number_of_boxes);
      DREAL_LOG_INFO(
          "IcpParallel::Worker() Detect that the current box is not feasible "
          "by "
          "evaluation:\n{}",
          current_box);
      continue;
    }
    if (evaluation_result->empty()) {
      // 3.2.2. delta-SAT : We find a box which is smaller enough.
      DREAL_LOG_INFO("IcpParallel::Worker() Found a delta-box:\n{}",
                     current_box);
      if (!(*found_delta_sat)) {
        *winner_thread = id;
        *found_delta_sat = true;
      }
      return;
    }
    // 3.2.3. This box is bigger than delta. Need branching.
    *number_of_boxes += 2;
    if (!ParallelBranch(*evaluation_result, stack_left_box_first, &current_box,
                        stack)) {
      DREAL_LOG_INFO(
          "IcpParallel::Worker() Found that the current box is not "
          "satisfying "
          "delta-condition but it's not bisectable.:\n{}",
          current_box);
      if (!(*found_delta_sat)) {
        *winner_thread = id;
        *found_delta_sat = true;
      }
      return;
    }

    need_to_pop = false;

    // We alternate between adding-the-left-box-first policy and
    // adding-the-right-box-first policy.
    stack_left_box_first = !stack_left_box_first;
    stat->increase_branch();
  }
  return;
}

}  // namespace

IcpParallel::IcpParallel(const Config& config) : Icp{config} {
  std::cerr << "IcpParallel::IcpParallel\n";
}

bool IcpParallel::CheckSat(const Contractor& contractor,
                           const vector<FormulaEvaluator>& formula_evaluators,
                           ContractorStatus* const cs) {
  std::cerr << "IcpParallel::CheckSat\n";
  DREAL_LOG_DEBUG("IcpParallel::CheckSat()");

  std::atomic_bool found_delta_sat{false};
  std::atomic<int> number_of_boxes{1};
  std::atomic<int> winner_thread{-1};

  static CdsInit cds_init{
      true /* main thread is using lock-free containers. */};

  const int num_threads = config().number_of_jobs();

  Stack<Box::IntervalVector> shared_stack;

  for (const auto& iv : FillUp(cs->box().interval_vector(), num_threads)) {
    shared_stack.push(iv);
  }

  // Use the stacking policy set by the configuration.
  stack_left_box_first_ = config().stack_left_box_first();
  static IcpStat stat{DREAL_LOG_INFO_ENABLED};

  vector<ContractorStatus> status_vector;
  status_vector.reserve(num_threads);
  {
    vector<JoiningThread> workers;
    workers.reserve(num_threads);

    DREAL_LOG_INFO("Main Thread: # of hardware concurrency = {}", num_threads);
    for (int i = 0; i < num_threads; ++i) {
      status_vector.push_back(*cs);
    }
    for (int i = 0; i < num_threads - 1; ++i) {
      status_vector.push_back(*cs);
      workers.emplace_back(Worker, contractor, config(), formula_evaluators, i,
                           false /* not main thread */, &shared_stack,
                           &status_vector[i], &found_delta_sat,
                           &number_of_boxes, &winner_thread, &stat);
    }
    Worker(contractor, config(), formula_evaluators, num_threads - 1,
           true /* main thread */, &shared_stack,
           &status_vector[num_threads - 1], &found_delta_sat, &number_of_boxes,
           &winner_thread, &stat);
  }
  // Post-processing: Join all the contractor statuses.
  for (const auto& cs_i : status_vector) {
    cs->InplaceJoin(cs_i);
  }
  if (found_delta_sat) {
    cs->mutable_box() = status_vector[winner_thread].box();
    return true;
  } else {
    cs->mutable_box().set_empty();
    return false;
  }
}
}  // namespace dreal

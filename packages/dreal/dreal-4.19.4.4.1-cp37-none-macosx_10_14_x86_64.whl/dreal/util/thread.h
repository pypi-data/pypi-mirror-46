#pragma once

#include <pthread.h>
#include <memory>
#include <utility>

#include <cds/container/treiber_stack.h>
#include <cds/gc/hp.h>  // for cds::HP (Hazard Pointer) SMR
#include <cds/init.h>   // for cds::Initialize and cds::Terminate

namespace dreal {

class JoiningThread {
 public:
  template <typename F, typename... Args>
  explicit JoiningThread(F&& f, Args&&... args)
      : t_(std::forward<F>(f), std::forward<Args>(args)...) {}

  JoiningThread(JoiningThread&& jt) noexcept : t_{std::move(jt.t_)} {}

  ~JoiningThread() {
    if (t_.joinable()) {
      t_.join();
    }
  }

  JoiningThread(JoiningThread&) = delete;
  JoiningThread& operator=(JoiningThread const&) = delete;

 private:
  std::thread t_;
};

class CdsScopeGuard {
 public:
  explicit CdsScopeGuard(bool use) : use_{use} {
    if (use_) {
      cds::threading::Manager::attachThread();
    }
  }
  ~CdsScopeGuard() {
    if (use_) {
      cds::threading::Manager::detachThread();
    }
  }

 private:
  const bool use_{};
};

class CdsInit {
 public:
  explicit CdsInit(bool use_lock_free_container) {
    // Initialize libcds
    cds::Initialize();
    hpGC_ = std::make_unique<cds::gc::HP>();
    if (use_lock_free_container) {
      cds::threading::Manager::attachThread();
    }
  }
  ~CdsInit() {
    // Terminate libcds
    cds::Terminate();
  }

 private:
  // Initialize Hazard Pointer singleton
  std::unique_ptr<cds::gc::HP> hpGC_;
};

/* struct StackTraits : public cds::container::treiber_stack::traits { */
/*   typedef cds::intrusive::treiber_stack::stat<> stat; */
/*   typedef cds::atomicity::item_counter item_counter; */
/* }; */

template <typename T>
using Stack = cds::container::TreiberStack<cds::gc::HP, T>;

}  // namespace dreal

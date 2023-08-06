#pragma once

#include <cfenv>

namespace dreal {

class RoundModeGuard {
 public:
  /// Saves the current round-mode and switch to @p new_round.
  explicit RoundModeGuard(int new_round) : round_mode_{fegetround()} {
    fesetround(new_round);
  }

  /// Deleted Copy-constructor.
  RoundModeGuard(const RoundModeGuard&) = delete;

  /// Deleted Move-constructor.
  RoundModeGuard(RoundModeGuard&&) = delete;

  /// Deleted Copy-assignment.
  RoundModeGuard& operator=(const RoundModeGuard&) = delete;

  /// Deleted Move-assignment.
  RoundModeGuard& operator=(RoundModeGuard&&) = delete;

  /// Destructor. Restore the saved round-mode.
  ~RoundModeGuard() { fesetround(round_mode_); }

 private:
  /// Saved round-mode at the construction.
  const int round_mode_{};
};
}  // namespace dreal

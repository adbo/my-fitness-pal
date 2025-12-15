export interface Exercise {
  id: string;
  name: string;
  name_pl?: string;
  description?: string;
  difficulty: number;
  progression_order: number;
  default_sets: number;
  default_reps: number;
  default_hold_seconds?: number;
  muscle_groups: string[];
  tips: string[];
  common_mistakes: string[];
}

export interface ProgressionChain {
  id: string;
  name: string;
  name_pl?: string;
  description?: string;
  exercises: Exercise[];
}

// Stored in Firebase per user
export interface UserProgress {
  chain_id: string;
  current_order: number;
  best_sets: number;
  best_reps: number;
  workouts_at_level: number;
  updated_at: number;
}

// Computed status for display
export interface ProgressionStatus {
  chain: ProgressionChain;
  progress: UserProgress;
  current_exercise: Exercise;
  next_exercise?: Exercise;
  can_progress: boolean;
  progress_percentage: number;
}

export const REPS_TO_PROGRESS = 12;
export const SETS_TO_PROGRESS = 3;

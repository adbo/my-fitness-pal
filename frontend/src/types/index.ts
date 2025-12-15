export interface Exercise {
  id: string;
  name: string;
  name_pl: string | null;
  description: string | null;
  difficulty: number;
  chain_id: string | null;
  progression_order: number;
  default_sets: number;
  default_reps: number;
  default_hold_seconds: number | null;
  muscle_groups: string[];
  tips: string[];
  common_mistakes: string[];
}

export interface ProgressionChain {
  id: string;
  name: string;
  name_pl: string | null;
  description: string | null;
  exercises: Exercise[];
}

export interface ProgressionChainList {
  id: string;
  name: string;
  name_pl: string | null;
  description: string | null;
  total_levels: number;
}

export interface ProgressionStatus {
  chain_id: string;
  chain_name: string;
  chain_name_pl: string | null;
  current_level: number;
  total_levels: number;
  current_exercise: Exercise;
  next_exercise: Exercise | null;
  previous_exercise: Exercise | null;
  best_reps: number;
  best_sets: number;
  reps_to_progress: number;
  sets_to_progress: number;
  can_progress: boolean;
  total_workouts_at_level: number;
  progress_percentage: number;
}

export interface RecordWorkoutResponse {
  message: string;
  can_progress: boolean;
  best_reps: number;
  best_sets: number;
}

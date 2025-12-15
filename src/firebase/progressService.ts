import {
  doc,
  getDoc,
  setDoc,
  updateDoc,
  collection,
  getDocs,
} from 'firebase/firestore';
import { db } from './config';
import { PROGRESSIONS, getExercise } from '../data/exercises';
import type { UserProgress, ProgressionStatus } from '../types';
import { REPS_TO_PROGRESS, SETS_TO_PROGRESS } from '../types';

const COLLECTION = 'user_progress';

function getDocId(userId: string, chainId: string): string {
  return `${userId}_${chainId}`;
}

function createDefaultProgress(chainId: string): UserProgress {
  return {
    chain_id: chainId,
    current_order: 0,
    best_sets: 0,
    best_reps: 0,
    workouts_at_level: 0,
    updated_at: Date.now(),
  };
}

export async function getUserProgress(
  userId: string,
  chainId: string
): Promise<UserProgress> {
  const docRef = doc(db, COLLECTION, getDocId(userId, chainId));
  const docSnap = await getDoc(docRef);

  if (docSnap.exists()) {
    return docSnap.data() as UserProgress;
  }

  // Create default progress if not exists
  const defaultProgress = createDefaultProgress(chainId);
  await setDoc(docRef, defaultProgress);
  return defaultProgress;
}

export async function getAllUserProgress(userId: string): Promise<UserProgress[]> {
  const results: UserProgress[] = [];

  for (const chain of PROGRESSIONS) {
    const progress = await getUserProgress(userId, chain.id);
    results.push(progress);
  }

  return results;
}

export async function recordWorkout(
  userId: string,
  chainId: string,
  sets: number,
  reps: number
): Promise<{ canProgress: boolean; message: string; progress: UserProgress }> {
  const docRef = doc(db, COLLECTION, getDocId(userId, chainId));
  const progress = await getUserProgress(userId, chainId);

  // Update best stats
  const newBestSets = Math.max(progress.best_sets, sets);
  const newBestReps = Math.max(progress.best_reps, reps);

  await updateDoc(docRef, {
    best_sets: newBestSets,
    best_reps: newBestReps,
    workouts_at_level: progress.workouts_at_level + 1,
    updated_at: Date.now(),
  });

  const updatedProgress: UserProgress = {
    ...progress,
    best_sets: newBestSets,
    best_reps: newBestReps,
    workouts_at_level: progress.workouts_at_level + 1,
  };

  const canProgress = newBestSets >= SETS_TO_PROGRESS && newBestReps >= REPS_TO_PROGRESS;

  const chain = PROGRESSIONS.find(p => p.id === chainId);
  const currentExercise = getExercise(chainId, progress.current_order);
  const nextExercise = getExercise(chainId, progress.current_order + 1);

  let message: string;
  if (canProgress && nextExercise) {
    message = `Świetnie! Możesz przejść do: ${nextExercise.name_pl || nextExercise.name}`;
  } else if (canProgress && !nextExercise) {
    message = `Brawo! Ukończyłeś całą progresję ${chain?.name_pl || chain?.name}!`;
  } else {
    const setsNeeded = Math.max(0, SETS_TO_PROGRESS - newBestSets);
    const repsNeeded = Math.max(0, REPS_TO_PROGRESS - newBestReps);
    message = `Dobry trening! Do progresji: ${setsNeeded} serii, ${repsNeeded} powtórzeń.`;
  }

  return { canProgress, message, progress: updatedProgress };
}

export async function advanceProgress(
  userId: string,
  chainId: string
): Promise<{ success: boolean; message: string }> {
  const progress = await getUserProgress(userId, chainId);
  const canProgress = progress.best_sets >= SETS_TO_PROGRESS && progress.best_reps >= REPS_TO_PROGRESS;

  if (!canProgress) {
    return { success: false, message: 'Nie spełniono kryteriów progresji' };
  }

  const nextExercise = getExercise(chainId, progress.current_order + 1);
  if (!nextExercise) {
    return { success: false, message: 'Jesteś już na najwyższym poziomie' };
  }

  const currentExercise = getExercise(chainId, progress.current_order);
  const docRef = doc(db, COLLECTION, getDocId(userId, chainId));

  await updateDoc(docRef, {
    current_order: progress.current_order + 1,
    best_sets: 0,
    best_reps: 0,
    workouts_at_level: 0,
    updated_at: Date.now(),
  });

  return {
    success: true,
    message: `Przeszedłeś z ${currentExercise?.name_pl} do ${nextExercise.name_pl}!`,
  };
}

export async function regressProgress(
  userId: string,
  chainId: string
): Promise<{ success: boolean; message: string }> {
  const progress = await getUserProgress(userId, chainId);

  if (progress.current_order <= 0) {
    return { success: false, message: 'Jesteś już na najniższym poziomie' };
  }

  const currentExercise = getExercise(chainId, progress.current_order);
  const prevExercise = getExercise(chainId, progress.current_order - 1);
  const docRef = doc(db, COLLECTION, getDocId(userId, chainId));

  await updateDoc(docRef, {
    current_order: progress.current_order - 1,
    best_sets: 0,
    best_reps: 0,
    workouts_at_level: 0,
    updated_at: Date.now(),
  });

  return {
    success: true,
    message: `Wróciłeś z ${currentExercise?.name_pl} do ${prevExercise?.name_pl}`,
  };
}

export function getProgressionStatus(
  chain: typeof PROGRESSIONS[0],
  progress: UserProgress
): ProgressionStatus {
  const currentExercise = chain.exercises[progress.current_order];
  const nextExercise = chain.exercises[progress.current_order + 1];
  const canProgress = progress.best_sets >= SETS_TO_PROGRESS && progress.best_reps >= REPS_TO_PROGRESS;
  const progressPercentage = ((progress.current_order + 1) / chain.exercises.length) * 100;

  return {
    chain,
    progress,
    current_exercise: currentExercise,
    next_exercise: nextExercise,
    can_progress: canProgress,
    progress_percentage: progressPercentage,
  };
}

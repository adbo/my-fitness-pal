interface Props {
  difficulty: number;
  maxDifficulty?: number;
}

export default function DifficultyBar({ difficulty, maxDifficulty = 10 }: Props) {
  return (
    <div className="difficulty-bar">
      {Array.from({ length: maxDifficulty }).map((_, i) => {
        const filled = i < difficulty;
        let colorClass = '';

        if (filled) {
          if (difficulty <= 3) colorClass = 'filled';
          else if (difficulty <= 6) colorClass = 'filled medium';
          else colorClass = 'filled hard';
        }

        return (
          <div
            key={i}
            className={`difficulty-segment ${colorClass}`}
          />
        );
      })}
    </div>
  );
}

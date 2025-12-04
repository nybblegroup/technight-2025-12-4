import { useState } from 'react';

interface RatingStarsProps {
  onSelect: (rating: number) => void;
  disabled?: boolean;
}

export function RatingStars({ onSelect, disabled = false }: RatingStarsProps) {
  const [hoveredStar, setHoveredStar] = useState(0);
  const [selectedStar, setSelectedStar] = useState(0);

  const handleClick = (rating: number) => {
    if (disabled) return;
    setSelectedStar(rating);
    onSelect(rating);
  };

  return (
    <div className="rating-stars">
      {[1, 2, 3, 4, 5].map((star) => (
        <span
          key={star}
          className={`star ${(hoveredStar >= star || selectedStar >= star) ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
          onMouseEnter={() => !disabled && setHoveredStar(star)}
          onMouseLeave={() => setHoveredStar(0)}
          onClick={() => handleClick(star)}
          style={{ cursor: disabled ? 'not-allowed' : 'pointer', opacity: disabled ? 0.5 : 1 }}
        >
          ⭐
        </span>
      ))}
    </div>
  );
}


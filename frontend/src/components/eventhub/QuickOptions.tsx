interface QuickOptionsProps {
  options: string[];
  onSelect: (option: string) => void;
  disabled?: boolean;
}

export function QuickOptions({ options, onSelect, disabled = false }: QuickOptionsProps) {
  return (
    <div className="quick-options">
      {options.map((option, index) => (
        <button
          key={index}
          className="quick-option"
          onClick={() => onSelect(option)}
          disabled={disabled}
        >
          {option}
        </button>
      ))}
    </div>
  );
}


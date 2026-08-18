import React from "react";

interface BowArrowGLogoProps {
  className?: string;
  bowColor?: string;
  arrowColor?: string;
  glowColor?: string;
}

export const BowArrowGLogo: React.FC<BowArrowGLogoProps> = ({
  className = "w-8 h-8",
  bowColor = "currentColor",
  arrowColor = "currentColor",
  glowColor = "transparent",
}) => {
  return (
    <svg
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={{
        filter: glowColor !== "transparent" ? `drop-shadow(0 0 6px ${glowColor})` : "none",
      }}
    >
      {/* Outer Bow Curve forming the G spine */}
      <path
        d="M 68 25 C 50 12, 22 20, 18 50 C 14 80, 48 90, 68 76 C 76 70, 78 58, 70 54 L 52 54"
        stroke={bowColor}
        strokeWidth="7"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />

      {/* Ornate Bow Tips */}
      <path
        d="M 68 25 C 72 20, 76 22, 75 16 C 73 12, 66 16, 68 25 Z"
        fill={bowColor}
      />
      <path
        d="M 68 76 C 74 80, 78 78, 76 86 C 72 90, 66 84, 68 76 Z"
        fill={bowColor}
      />

      {/* Bowstring */}
      <path
        d="M 72 18 L 72 82"
        stroke={bowColor}
        strokeWidth="1.5"
        strokeDasharray="2 2"
        opacity="0.6"
      />

      {/* Arrow Shaft (Horizontal Crossbar of G) */}
      <line
        x1="26"
        y1="50"
        x2="84"
        y2="50"
        stroke={arrowColor}
        strokeWidth="5"
        strokeLinecap="round"
      />

      {/* Arrow Head (Pointing Right) */}
      <polygon
        points="84,43 96,50 84,57 87,50"
        fill={arrowColor}
      />

      {/* Arrow Fletching / Feather at Left */}
      <path
        d="M 26 50 L 18 42 M 26 50 L 18 58 M 30 50 L 22 42 M 30 50 L 22 58"
        stroke={arrowColor}
        strokeWidth="2.5"
        strokeLinecap="round"
      />
    </svg>
  );
};

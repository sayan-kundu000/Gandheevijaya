import React from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "./Button";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  totalItems?: number;
  itemsPerPage?: number;
}

export const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
  totalItems,
  itemsPerPage,
}) => {
  if (totalPages <= 1) return null;

  const startItem = (currentPage - 1) * (itemsPerPage || 10) + 1;
  const endItem = Math.min(currentPage * (itemsPerPage || 10), totalItems || 0);

  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 text-xs text-slate-400">
      <div>
        {totalItems ? (
          <span>
            Showing <strong className="text-slate-200">{startItem}</strong> to{" "}
            <strong className="text-slate-200">{endItem}</strong> of{" "}
            <strong className="text-slate-200">{totalItems}</strong> entries
          </span>
        ) : (
          <span>
            Page <strong className="text-slate-200">{currentPage}</strong> of{" "}
            <strong className="text-slate-200">{totalPages}</strong>
          </span>
        )}
      </div>

      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          disabled={currentPage <= 1}
          onClick={() => onPageChange(currentPage - 1)}
          leftIcon={<ChevronLeft className="w-3.5 h-3.5" />}
        >
          Previous
        </Button>
        <span className="px-2 font-semibold text-slate-200">
          {currentPage} / {totalPages}
        </span>
        <Button
          variant="outline"
          size="sm"
          disabled={currentPage >= totalPages}
          onClick={() => onPageChange(currentPage + 1)}
          rightIcon={<ChevronRight className="w-3.5 h-3.5" />}
        >
          Next
        </Button>
      </div>
    </div>
  );
};

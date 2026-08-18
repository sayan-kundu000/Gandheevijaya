import React from "react";
import { Skeleton } from "./Skeleton";
import { EmptyState } from "./EmptyState";
import { ChevronUp, ChevronDown } from "lucide-react";

export interface Column<T> {
  key: string;
  header: React.ReactNode;
  cell: (row: T, index: number) => React.ReactNode;
  sortable?: boolean;
  className?: string;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (row: T, index: number) => string | number;
  isLoading?: boolean;
  sortColumn?: string;
  sortDirection?: "asc" | "desc";
  onSort?: (columnKey: string) => void;
  emptyTitle?: string;
  emptyDescription?: string;
}

export function Table<T>({
  columns,
  data,
  keyExtractor,
  isLoading = false,
  sortColumn,
  sortDirection = "asc",
  onSort,
  emptyTitle = "No records found",
  emptyDescription = "There are no data items available to display.",
}: TableProps<T>) {
  return (
    <div className="w-full overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/60 shadow-lg">
      <table className="w-full text-left text-xs border-collapse">
        <thead className="bg-slate-900 border-b border-slate-800 text-slate-400 font-semibold uppercase tracking-wider">
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                className={`p-3.5 ${col.className || ""} ${
                  col.sortable ? "cursor-pointer select-none hover:text-slate-200" : ""
                }`}
                onClick={() => col.sortable && onSort && onSort(col.key)}
              >
                <div className="flex items-center gap-1.5">
                  <span>{col.header}</span>
                  {col.sortable && sortColumn === col.key && (
                    <span className="text-brand-400">
                      {sortDirection === "asc" ? (
                        <ChevronUp className="w-3.5 h-3.5" />
                      ) : (
                        <ChevronDown className="w-3.5 h-3.5" />
                      )}
                    </span>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/60 text-slate-300">
          {isLoading ? (
            Array.from({ length: 5 }).map((_, rIdx) => (
              <tr key={rIdx}>
                {columns.map((col) => (
                  <td key={col.key} className="p-3.5">
                    <Skeleton className="h-4 w-full" />
                  </td>
                ))}
              </tr>
            ))
          ) : data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="p-8">
                <EmptyState title={emptyTitle} description={emptyDescription} />
              </td>
            </tr>
          ) : (
            data.map((row, rIdx) => (
              <tr
                key={keyExtractor(row, rIdx)}
                className="hover:bg-slate-800/40 transition-colors"
              >
                {columns.map((col) => (
                  <td key={col.key} className={`p-3.5 ${col.className || ""}`}>
                    {col.cell(row, rIdx)}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

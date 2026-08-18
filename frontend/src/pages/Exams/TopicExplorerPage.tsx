import React from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "../../components/layout/AppShell";
import { TopicCard } from "../../features/topics/components/TopicCard";
import { Skeleton } from "../../components/ui/Skeleton";
import { ErrorState } from "../../components/ui/ErrorState";
import { taxonomyApi } from "../../services/taxonomyApi";
import { ArrowLeft, Layers } from "lucide-react";
import { Button } from "../../components/ui/Button";

export const TopicExplorerPage: React.FC = () => {
  const { subjectId } = useParams<{ subjectId: string }>();
  const parsedSubjectId = subjectId ? parseInt(subjectId, 10) : undefined;

  const {
    data: topics,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["topics", parsedSubjectId],
    queryFn: () => taxonomyApi.getTopics(parsedSubjectId),
  });

  if (error) {
    return (
      <AppShell title="Topics Explorer">
        <ErrorState message="Failed to load topics for subject." onRetry={refetch} />
      </AppShell>
    );
  }

  return (
    <AppShell title="Syllabus Topics Explorer">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link to="/exams">
              <Button variant="outline" size="sm" leftIcon={<ArrowLeft className="w-4 h-4" />}>
                Back to Subjects
              </Button>
            </Link>
            <div>
              <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <Layers className="w-5 h-5 text-brand-400" />
                Topic Breakdown
              </h3>
              <p className="text-xs text-slate-400">
                Select a specific topic to view available practice quizzes and assessments.
              </p>
            </div>
          </div>

          <span className="text-xs text-slate-400">{topics?.length || 0} Topics Available</span>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Skeleton className="h-36 w-full" />
            <Skeleton className="h-36 w-full" />
            <Skeleton className="h-36 w-full" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {topics?.map((topic) => (
              <TopicCard key={topic.id} topic={topic} />
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
};

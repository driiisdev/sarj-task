import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { analysisApi } from '@/actions/analyzeActions';
import { SentimentAnalysis, CharacterAnalysis, LanguageAnalysis, SummaryAnalysis } from '@/lib/types/analysis';
import { TabButton } from './TabButton';
import { AnalysisButton } from './AnalysisButton';
import { AnalysisError } from './AnalysisError';
import { CharacterResults } from './CharacterResults';
import { LanguageResults } from './LanguageResults';
import { SentimentResults } from './SentimentResults';
import { SummaryResults } from './SummaryResults';


interface AnalysisSectionProps {
  bookId?: string;
}

export function AnalysisSection({ bookId }: AnalysisSectionProps) {
  const [activeTab, setActiveTab] = useState<string>('characters');

  const charactersMutation = useMutation({
    mutationFn: () => analysisApi.analyzeCharacters(bookId!)
  });

  const languageMutation = useMutation({
    mutationFn: () => analysisApi.analyzeLanguage(bookId!)
  });

  const sentimentMutation = useMutation({
    mutationFn: () => analysisApi.analyzeSentiment(bookId!)
  });

  const summaryMutation = useMutation({
    mutationFn: () => analysisApi.analyzeSummary(bookId!)
  });

  const getMutationForType = (type: string) => {
    const mutations = {
      characters: charactersMutation,
      language: languageMutation,
      sentiment: sentimentMutation,
      summary: summaryMutation
    };
    return mutations[type as keyof typeof mutations];
  };

  return (
    <>
    <div className="h-full f">
      <div className="border-b flex flex-row justify-between mb-4">
        {['language', 'sentiment', 'summary','characters'].map((tab) => (
          <TabButton
            key={tab}
            active={activeTab === tab}
            onClick={() => setActiveTab(tab)}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </TabButton>
        ))}
      </div>
    </div>

    <div className="overflow-y-auto">
      <div className="space-y-4">
        <AnalysisButton
          onClick={() => getMutationForType(activeTab).mutate()}
          loading={getMutationForType(activeTab).isPending}
          disabled={!bookId}
        >
          {getMutationForType(activeTab).isPending 
            ? 'Analyzing...' 
            : `Run ${activeTab} Analysis`}
        </AnalysisButton>

        {getMutationForType(activeTab).isError && (
          <AnalysisError 
            message={getMutationForType(activeTab).error?.message || 'Error: Enter ebook number'}
          />
        )}

        {getMutationForType(activeTab).isSuccess && (
          <div className="p-4 bg-gray-50 text-black rounded-lg">
            {activeTab === 'sentiment' && (
              <SentimentResults data={getMutationForType(activeTab).data?.data as SentimentAnalysis} />
            )}
            {activeTab === 'language' && (
              <LanguageResults data={getMutationForType(activeTab).data?.data as LanguageAnalysis} />
            )}
            {activeTab === 'characters' && (
              <CharacterResults data={getMutationForType(activeTab).data?.data as CharacterAnalysis} />
            )}
            {activeTab === 'summary' && (
              <SummaryResults data={getMutationForType(activeTab).data?.data as SummaryAnalysis} />
            )}
          </div>
        )}
      </div>
    </div>
    </>
  );
}

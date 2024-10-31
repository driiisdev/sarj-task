import baseUrl  from "@/lib/config/config";
import { AnalysisResponse, CharacterAnalysis, LanguageAnalysis, SentimentAnalysis, SummaryAnalysis } from '@/lib/types/analysis';
import { ApiError } from '@/lib/types/error';

async function handleApiError(response: Response) {
  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.detail);
  }
}


class AnalysisApi {

  async fetchApi<T>(endpoint: string, book_id: string): Promise<AnalysisResponse<T>> {
    try {
      const response = await fetch(`${baseUrl}/${endpoint}?book_id=${book_id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      await handleApiError(response);

      const data = await response.json();
      return { success: true, ...data };
    } catch {
      throw new Error(`${endpoint} analysis failed`);
    }
  }

  async analyzeCharacters(book_id: string): Promise<AnalysisResponse<CharacterAnalysis>> {
    return this.fetchApi<CharacterAnalysis>('characters', book_id);
  }

  async analyzeLanguage(book_id: string): Promise<AnalysisResponse<LanguageAnalysis>> {
    return this.fetchApi<LanguageAnalysis>('language', book_id);
  }

  async analyzeSentiment(book_id: string): Promise<AnalysisResponse<SentimentAnalysis>> {
    const result = await this.fetchApi<SentimentAnalysis>('sentiment', book_id);
    return result;
  }

  async analyzeSummary(book_id: string): Promise<AnalysisResponse<SummaryAnalysis>> {
    return this.fetchApi<SummaryAnalysis>('summary', book_id);
  }
}

export const analysisApi = new AnalysisApi();

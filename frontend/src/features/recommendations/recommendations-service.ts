import { apiClient } from '../../lib/http/api-client';
import type { RecommendationRequest, RecommendationResponse } from './recommendations-types';

export function createRecommendation(payload: RecommendationRequest) {
  return apiClient.post<RecommendationResponse>('/recommendations', payload);
}

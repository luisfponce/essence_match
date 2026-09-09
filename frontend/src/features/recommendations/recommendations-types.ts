import type { Item } from '../items/items-types';

export type RecommendationRequest = {
  message: string;
  limit?: number;
};

export type RecommendedEssence = Item & {
  score: number;
  matched_symptoms: string[];
  reasons: string[];
};

export type RecommendationResponse = {
  reply: string;
  recommendations: RecommendedEssence[];
  detected_symptoms: string[];
};

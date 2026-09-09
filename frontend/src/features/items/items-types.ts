export type Item = {
  id: number;
  slug: string;
  name: string;
  description: string;
  symptoms: string[];
  uses: string[];
  safety_notes: string[];
  created_at: string;
};

export type ItemCreate = {
  slug: string;
  name: string;
  description: string;
  symptoms?: string[];
  uses?: string[];
  safety_notes?: string[];
};

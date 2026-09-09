import { Link } from 'react-router-dom';
import { FormEvent, useState } from 'react';

import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { createRecommendation } from '../features/recommendations/recommendations-service';
import type { RecommendationResponse } from '../features/recommendations/recommendations-types';
import { ApiError } from '../lib/http/api-error';

export const homeHeadline = 'EssenceMatch';

export function HomePage() {
  const [message, setMessage] = useState('I feel stressed and cannot sleep');
  const [result, setResult] = useState<RecommendationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      setResult(await createRecommendation({ message, limit: 3 }));
    } catch (caught: unknown) {
      setError(caught instanceof ApiError ? caught.message : 'Unable to create recommendations.');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="page-shell home-layout">
      <section className="stack hero-copy">
        <p className="eyebrow">Wellness matching</p>
        <h1>{homeHeadline}</h1>
        <p className="lede">Describe how you want to feel and get deterministic essence suggestions from the local catalog.</p>
        <Link to="/items">
          <Button>Browse catalog</Button>
        </Link>
      </section>
      <Card className="stack chat-card">
        <form className="stack" onSubmit={handleSubmit}>
          <label className="stack">
            <span className="eyebrow">Essence chat</span>
            <textarea
              className="input textarea"
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              placeholder="Example: I need help with focus and afternoon fatigue"
              rows={5}
            />
          </label>
          <Button disabled={isLoading || !message.trim()}>{isLoading ? 'Matching...' : 'Get recommendations'}</Button>
        </form>
        <p className="muted">Informational wellness guidance only. Not medical advice.</p>
        {error ? <p className="error">{error}</p> : null}
        {result ? (
          <section className="stack" aria-live="polite">
            <p>{result.reply}</p>
            <div className="recommendation-list">
              {result.recommendations.map((item) => (
                <article className="recommendation-card" key={item.id}>
                  <strong>{item.name}</strong>
                  <p>{item.description}</p>
                  <span className="muted">Matched: {item.matched_symptoms.join(', ')}</span>
                </article>
              ))}
            </div>
          </section>
        ) : null}
      </Card>
    </main>
  );
}

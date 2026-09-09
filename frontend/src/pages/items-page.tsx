import { useEffect, useState } from 'react';

import { Card } from '../components/ui/card';
import { ApiError } from '../lib/http/api-error';
import { listItems } from '../features/items/items-service';
import type { Item } from '../features/items/items-types';

export function ItemsPage() {
  const [items, setItems] = useState<Item[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    listItems()
      .then((data) => {
        if (active) setItems(data);
      })
      .catch((caught: unknown) => {
        if (active) setError(caught instanceof ApiError ? caught.message : 'Unable to load items.');
      });
    return () => {
      active = false;
    };
  }, []);

  return (
    <main className="page-shell stack">
      <h1>Items</h1>
      {error ? <p className="error">{error}</p> : null}
      <div className="card-grid">
        {items.map((item) => (
          <Card key={item.id} className="stack">
            <div>
              <p className="eyebrow">{item.slug}</p>
              <h2>{item.name}</h2>
            </div>
            <p>{item.description}</p>
            <p className="muted">Helpful for: {item.symptoms.join(', ')}</p>
            <ul className="compact-list">
              {item.uses.map((use) => (
                <li key={use}>{use}</li>
              ))}
            </ul>
          </Card>
        ))}
        {!items.length && !error ? <p className="muted">No catalog items yet.</p> : null}
      </div>
    </main>
  );
}

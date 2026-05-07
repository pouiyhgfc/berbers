# Supabase: woordsuggesties (`word_submissions`)

Geen **service role**- of **anon**-keys in git. Zet in **`assets/js/supabase-config.js`** (staat in `.gitignore`):

```js
window.TARIFIT_SUPABASE = {
  url: 'https://<project-ref>.supabase.co',
  anonKey: '<anon public key>',
};
```

Kopieer van `assets/js/supabase-config.example.js`. Optioneel mag ook `anon_key` i.p.v. `anonKey`.

**Vercel / andere hosting:** zorg dat `supabase-config.js` op de server staat (upload handmatig, of genereer in een build-stap uit geheimen — niet in de repo committen).

---

## 1. SQL — tabel en RLS (idempotent)

Voer het hele blok uit in **SQL Editor** (Supabase dashboard). Policy-namen worden eerst verwijderd zodat je opnieuw kunt draaien na aanpassingen.

```sql
-- Tabel
create table if not exists public.word_submissions (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  berber text not null,
  dutch text not null,
  notes text,
  status text not null default 'pending'
    check (status in ('pending', 'approved', 'rejected'))
);

alter table public.word_submissions enable row level security;

drop policy if exists "anon_insert_pending_only" on public.word_submissions;
drop policy if exists "authenticated_select_all" on public.word_submissions;
drop policy if exists "authenticated_update" on public.word_submissions;

-- Publiek formulier: alleen insert, alleen status pending (JWT-rol = anon)
create policy "anon_insert_pending_only"
  on public.word_submissions
  for insert
  to anon
  with check (status = 'pending');

-- Admin-pagina na login: lezen (JWT-rol = authenticated)
create policy "authenticated_select_all"
  on public.word_submissions
  for select
  to authenticated
  using (true);

-- Admin: status wijzigen
create policy "authenticated_update"
  on public.word_submissions
  for update
  to authenticated
  using (true)
  with check (true);
```

**Strakker (aanbevolen later):** vervang `authenticated_*` policies door bv. `auth.jwt() ->> 'email' in ('jij@example.com')` of een `admin_users`-tabel.

---

## 2. Auth (voor `woord-inzenden-admin.html`)

1. **Authentication → Providers → Email**: aan.
2. Maak een gebruiker: **Authentication → Users → Add user** (e-mail + wachtwoord), of nodig jezelf uit.
3. Als login **Email not confirmed** geeft: onder **Authentication → Providers → Email** tijdelijk **Confirm email** uit voor testen, of bevestig je e-mail.

---

## 3. Site

| Pagina | Doel |
|--------|------|
| `woord-inzenden.html` | Formulier, alleen **anon** key |
| `woord-inzenden-admin.html` | Lijst + goedkeuren/afwijzen na **signInWithPassword** |

De client wordt geladen via **ESM** (`assets/js/tarifit-supabase-client.js` + `esm.sh`); daardoor werkt `createClient` betrouwbaar in de browser.

---

## 4. Troubleshooting

| Symptoom | Mogelijke oorzaak |
|----------|-------------------|
| `relation "word_submissions" does not exist` | SQL-blok nog niet uitgevoerd |
| RLS / policy error bij versturen | Geen `insert`-policy voor `anon`, of `status` ≠ `pending` |
| Login lukt niet | Verkeerd wachtwoord, of e-mail nog niet bevestigd |
| Na login: geen rijen / RLS bij select | Geen `select`-policy voor `authenticated`, of verkeerde API key |
| Leeg scherm / module error | Netwerk blokkeert `esm.sh`; probeer andere browser of VPN |

**Als je per ongeluk een anon key in git had gezet:** draai in Supabase **Project Settings → API** de anon key opnieuw (rotate) en werk alleen `supabase-config.js` bij.

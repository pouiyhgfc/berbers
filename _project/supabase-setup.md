# Supabase: woordsuggesties (`word_submissions`)

Geen secrets in deze repo. Maak een Supabase-project aan en zet **project-URL** en **anon (public) key** in `assets/js/supabase-config.js` (kopieer van `supabase-config.example.js`).

## 1. SQL — tabel en RLS

Voer uit in de SQL-editor van Supabase:

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

-- Iedereen mag één rij indienen met status pending (publiek formulier)
create policy "anon_insert_pending_only"
  on public.word_submissions
  for insert
  to anon
  with check (status = 'pending');

-- Alleen ingelogde gebruikers mogen lezen (admin-pagina na login)
create policy "authenticated_select_all"
  on public.word_submissions
  for select
  to authenticated
  using (true);

-- Alleen ingelogde gebruikers mogen status bijwerken
create policy "authenticated_update"
  on public.word_submissions
  for update
  to authenticated
  using (true)
  with check (true);
```

**Strakker maken:** vervang `authenticated_select_all` / `update` door een check op een `admin_users`-tabel of op `auth.jwt() ->> 'email' in (...)` zodat niet elke geregistreerde gebruiker mee kan lezen.

## 2. Auth

Zet **Email** provider aan. Maak handmatig één admin-gebruiker (Authentication → Users) of nodig jezelf uit via registratie en pas daarna de RLS aan.

## 3. Site

- Publiek formulier: `woord-inzenden.html` (laadt `supabase-config.js` + Supabase JS client van CDN).
- Beheer: `woord-inzenden-admin.html` — log in met e-mail/wachtwoord van de admin-user.

Service role key **niet** in statische HTML gebruiken.

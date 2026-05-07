/**
 * Gedeelde Supabase-client voor statische pagina's (ES module).
 * Laadt vóór deze module: <script src="assets/js/supabase-config.js"></script>
 */
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.49.1';

export function getSupabaseConfig() {
  const c = window.TARIFIT_SUPABASE;
  if (!c) {
    return { ok: false, reason: 'missing' };
  }
  const url = String(c.url || c.supabaseUrl || '').trim();
  const anonKey = String(c.anonKey || c.anon_key || '').trim();
  if (!url || !anonKey) {
    return { ok: false, reason: 'empty' };
  }
  if (url.includes('YOUR_PROJECT') || anonKey.includes('YOUR_PUBLIC')) {
    return { ok: false, reason: 'placeholder' };
  }
  return { ok: true, url, anonKey };
}

export function createTarifitClient() {
  const cfg = getSupabaseConfig();
  if (!cfg.ok) {
    return { client: null, cfg };
  }
  return {
    client: createClient(cfg.url, cfg.anonKey),
    cfg,
  };
}

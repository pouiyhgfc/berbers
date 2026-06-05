// tweaks-app.jsx — Tarifit homepage variants (v2)

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "logo": "diamond",
  "theme": "rif",
  "patterns": "subtle",
  "tifinagh": true
}/*EDITMODE-END*/;

function applyTweaks(t) {
  const root = document.documentElement;
  root.classList.remove("logo-diamond", "logo-wordmark", "logo-tile");
  root.classList.add("logo-" + t.logo);
  root.classList.remove("theme-rif", "theme-clay", "theme-ink");
  root.classList.add("theme-" + t.theme);
  root.classList.remove("patterns-none", "patterns-subtle", "patterns-bold");
  root.classList.add("patterns-" + t.patterns);
  root.classList.toggle("no-tifi", !t.tifinagh);
}
applyTweaks(TWEAK_DEFAULTS);

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  React.useEffect(() => { applyTweaks(t); }, [t]);
  return (
    <TweaksPanel title="Tweaks · Tarifit">
      <TweakSection label="Logo" />
      <TweakRadio
        label="Mark"
        value={t.logo}
        options={[
          { value: "diamond",  label: "Diamant" },
          { value: "wordmark", label: "ⵣ los" },
          { value: "tile",     label: "Tegel" }
        ]}
        onChange={(v) => setTweak("logo", v)}
      />

      <TweakSection label="Palet" />
      <TweakRadio
        label="Toon"
        value={t.theme}
        options={[
          { value: "rif",  label: "Rif" },
          { value: "clay", label: "Klei" },
          { value: "ink",  label: "Inkt" }
        ]}
        onChange={(v) => setTweak("theme", v)}
      />

      <TweakSection label="Decoratie" />
      <TweakRadio
        label="Patronen"
        value={t.patterns}
        options={[
          { value: "none",   label: "Geen" },
          { value: "subtle", label: "Subtiel" },
          { value: "bold",   label: "Bold" }
        ]}
        onChange={(v) => setTweak("patterns", v)}
      />
      <TweakToggle
        label="Tifinagh"
        value={t.tifinagh}
        onChange={(v) => setTweak("tifinagh", v)}
      />
    </TweaksPanel>
  );
}

ReactDOM.createRoot(document.getElementById("tweaks-root")).render(<App />);

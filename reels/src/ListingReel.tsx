import React from "react";
import {
  AbsoluteFill, Audio, Img, continueRender, delayRender, interpolate,
  spring, staticFile, useCurrentFrame, useVideoConfig, Easing,
} from "remotion";
import { TransitionSeries, linearTiming, springTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import { fade } from "@remotion/transitions/fade";
import "@fontsource/plus-jakarta-sans/500.css";
import "@fontsource/plus-jakarta-sans/700.css";
import "@fontsource/plus-jakarta-sans/800.css";
import "@fontsource/outfit/700.css";
import "@fontsource/ibm-plex-sans-arabic/500.css";
import "@fontsource/ibm-plex-sans-arabic/700.css";

// ---------- brand (same as tools/brand.py) ----------
const RED = "#e0263b";
const INK = "#222222";
const WHITE = "#ffffff";
const EN = "'Plus Jakarta Sans', sans-serif";
const AR = "'IBM Plex Sans Arabic', sans-serif";
const LOGO = "'Outfit', sans-serif";

// Make the render wait until every brand font is in, so Arabic never shows as boxes.
const fontHandle = delayRender("Loading brand fonts");
Promise.all([
  "500 40px 'Plus Jakarta Sans'", "700 40px 'Plus Jakarta Sans'", "800 40px 'Plus Jakarta Sans'",
  "700 40px 'Outfit'", "500 40px 'IBM Plex Sans Arabic'", "700 40px 'IBM Plex Sans Arabic'",
].map((f) => document.fonts.load(f, f.includes("Arabic") ? "ويكند" : "weekend")))
  .then(() => continueRender(fontHandle))
  .catch(() => continueRender(fontHandle));

// ---------- data the template takes (one JSON per post) ----------
export type Move = "zoom_in" | "zoom_out" | "pan_left" | "pan_right" | "pan_up" | "pan_down";
export type ShotText =
  | { type: "hook"; en: string; ar: string }
  | { type: "title"; name: string; ar?: string; pill: string }
  | { type: "room"; name: string; en: string; ar: string; price?: string }
  | { type: "fact"; en: string; ar: string }
  | { type: "end"; name: string; price?: string; ar?: string };
export type Shot = {
  photo: string;          // file in public/ (e.g. "photos/majestic/23-03.webp") or an https URL
  seconds: number;
  move: Move;
  fx?: number; fy?: number; // point of interest, 0..1
  framed?: boolean;        // small photo: show as a card over a blurred copy
  text: ShotText;
};
export type ReelProps = { music?: string; musicStart?: number; shots: Shot[] };

const T = 9; // transition length in frames
export const reelDuration = (p: ReelProps, fps: number) =>
  p.shots.reduce((a, s) => a + Math.round(s.seconds * fps), 0) - T * (p.shots.length - 1);

const src = (p: string) => (/^https?:/.test(p) ? p : staticFile(p));

// ---------- camera move on a photo ----------
const Photo: React.FC<{ shot: Shot; frames: number }> = ({ shot, frames }) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, frames], [0, 1], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.sin) });
  const fx = shot.fx ?? 0.5, fy = shot.fy ?? 0.5;
  let scale = 1.12, x = 0, y = 0;
  switch (shot.move) {
    case "zoom_in": scale = 1.08 + 0.14 * t; break;
    case "zoom_out": scale = 1.22 - 0.14 * t; break;
    case "pan_left": x = 4 - 8 * t; scale = 1.16; break;
    case "pan_right": x = -4 + 8 * t; scale = 1.16; break;
    case "pan_up": y = 4 - 8 * t; scale = 1.16; break;
    case "pan_down": y = -4 + 8 * t; scale = 1.16; break;
  }
  const img = (
    <Img src={src(shot.photo)} style={{
      width: "100%", height: "100%", objectFit: "cover",
      objectPosition: `${fx * 100}% ${fy * 100}%`,
      transform: `scale(${scale}) translate(${x}%, ${y}%)`,
    }} />
  );
  if (!shot.framed) return <AbsoluteFill>{img}</AbsoluteFill>;
  // Framed card for low-resolution photos.
  return (
    <AbsoluteFill>
      <Img src={src(shot.photo)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "blur(40px) brightness(0.6)", transform: "scale(1.2)" }} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-start", paddingTop: 300 }}>
        <div style={{ width: 960, height: 720, borderRadius: 40, overflow: "hidden", boxShadow: "0 30px 80px rgba(0,0,0,.45)" }}>
          <Img src={src(shot.photo)} style={{ width: "100%", height: "100%", objectFit: "cover",
            transform: `scale(${1 + 0.08 * t})` }} />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- text pieces ----------
const useIn = (delay = 0) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const s = spring({ frame: f - delay, fps, config: { damping: 14, stiffness: 140 } });
  return { opacity: Math.min(1, s * 1.4), transform: `translateY(${(1 - s) * 60}px)` };
};

const Logo: React.FC<{ color?: string; accent?: string; size?: number }> = ({ color = WHITE, accent = RED, size = 50 }) => (
  <div style={{ display: "flex", alignItems: "baseline", fontFamily: LOGO, fontWeight: 700, fontSize: size, color }}>
    weekend<span style={{ fontFamily: AR, color: accent, marginLeft: 2, fontSize: size * 1.02 }}>نا</span>
  </div>
);

const Pill: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span style={{ background: RED, color: WHITE, fontFamily: EN, fontWeight: 700, fontSize: 30, letterSpacing: 2,
    padding: "12px 26px", borderRadius: 40, textTransform: "uppercase" }}>{children}</span>
);

const Ar: React.FC<{ children: string; size: number; weight?: number; color?: string; style?: React.CSSProperties }> =
  ({ children, size, weight = 700, color = WHITE, style }) => (
    <div dir="rtl" style={{ fontFamily: AR, fontWeight: weight, fontSize: size, color, lineHeight: 1.35, textAlign: "right", ...style }}>{children}</div>
  );

const shadow = "0 3px 18px rgba(0,0,0,.45)";

// Text sits in the band Instagram leaves free (above its caption area, clear of the right-hand buttons).
const Band: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ justifyContent: "flex-end", padding: "0 170px 430px 72px", textShadow: shadow }}>{children}</AbsoluteFill>
);

const Overlay: React.FC<{ text: ShotText }> = ({ text }) => {
  const a = useIn(4), b = useIn(10), c = useIn(16);
  switch (text.type) {
    case "hook":
      return (
        <Band>
          <div style={{ ...a, fontFamily: EN, fontWeight: 800, fontSize: 92, color: WHITE, lineHeight: 1.05 }}>{text.en}</div>
          <Ar size={62} style={{ ...b, marginTop: 26 }}>{text.ar}</Ar>
        </Band>
      );
    case "title":
      return (
        <Band>
          <div style={a}><Pill>{text.pill}</Pill></div>
          <div style={{ ...b, fontFamily: EN, fontWeight: 800, fontSize: 84, color: WHITE, lineHeight: 1.05, marginTop: 34 }}>{text.name}</div>
          {text.ar && <Ar size={52} weight={500} style={{ ...c, marginTop: 18 }}>{text.ar}</Ar>}
        </Band>
      );
    case "room":
      return (
        <Band>
          <div style={{ ...a, fontFamily: EN, fontWeight: 700, fontSize: 34, color: WHITE, letterSpacing: 3, textTransform: "uppercase", opacity: a.opacity * 0.9 }}>{text.name}</div>
          <div style={{ ...b, fontFamily: EN, fontWeight: 800, fontSize: 70, color: WHITE, lineHeight: 1.08, marginTop: 12 }}>{text.en}</div>
          <Ar size={48} weight={500} style={{ ...b, marginTop: 14 }}>{text.ar}</Ar>
          {text.price && (
            <div style={{ ...c, marginTop: 26 }}>
              <span style={{ background: WHITE, color: RED, fontFamily: EN, fontWeight: 800, fontSize: 46, padding: "10px 26px", borderRadius: 16, textShadow: "none" }}>{text.price}</span>
            </div>
          )}
        </Band>
      );
    case "fact":
      return (
        <Band>
          <div style={{ ...a, display: "flex", alignItems: "center", gap: 22 }}>
            <div style={{ width: 22, height: 22, borderRadius: 11, background: RED, flex: "none" }} />
            <div style={{ fontFamily: EN, fontWeight: 800, fontSize: 72, color: WHITE, lineHeight: 1.08 }}>{text.en}</div>
          </div>
          <Ar size={52} weight={500} style={{ ...b, marginTop: 18 }}>{text.ar}</Ar>
        </Band>
      );
    case "end":
      return null;
  }
};

const EndCard: React.FC<{ shot: Shot }> = ({ shot }) => {
  const t = shot.text as Extract<ShotText, { type: "end" }>;
  const a = useIn(2), b = useIn(8), c = useIn(14), d = useIn(22);
  return (
    <AbsoluteFill>
      <Img src={src(shot.photo)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "blur(30px) brightness(.55)", transform: "scale(1.2)" }} />
      <AbsoluteFill style={{ background: `linear-gradient(180deg, rgba(224,38,59,.82), rgba(224,38,59,.96))` }} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", textAlign: "center", padding: "0 90px 180px" }}>
        <div style={a}><Logo color={WHITE} accent={INK} size={86} /></div>
        <div style={{ ...b, fontFamily: EN, fontWeight: 800, fontSize: 78, color: WHITE, lineHeight: 1.08, marginTop: 80 }}>{t.name}</div>
        {t.price && <div style={{ ...c, fontFamily: EN, fontWeight: 600, fontSize: 48, color: WHITE, marginTop: 26 }}>{t.price}</div>}
        {t.ar && <Ar size={50} style={{ ...c, textAlign: "center", marginTop: 20 }}>{t.ar}</Ar>}
        <div style={{ ...d, marginTop: 70, background: WHITE, color: RED, fontFamily: EN, fontWeight: 800, fontSize: 44,
          padding: "26px 54px", borderRadius: 60, boxShadow: "0 16px 40px rgba(0,0,0,.25)" }}>
          weekendna.com · link in bio
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const ShotView: React.FC<{ shot: Shot; frames: number }> = ({ shot, frames }) => {
  if (shot.text.type === "end") return <EndCard shot={shot} />;
  return (
    <AbsoluteFill style={{ background: "#111" }}>
      <Photo shot={shot} frames={frames} />
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,.45) 0%, rgba(0,0,0,0) 18%, rgba(0,0,0,0) 42%, rgba(0,0,0,.78) 100%)" }} />
      <AbsoluteFill style={{ padding: "110px 72px" }}><Logo /></AbsoluteFill>
      <Overlay text={shot.text} />
    </AbsoluteFill>
  );
};

export const ListingReel: React.FC<ReelProps> = ({ shots, music, musicStart = 0 }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const f = useCurrentFrame();
  const volume = interpolate(f, [0, 15, durationInFrames - 30, durationInFrames], [0, 0.9, 0.9, 0], { extrapolateRight: "clamp" });
  const items: React.ReactNode[] = [];
  shots.forEach((s, i) => {
    const frames = Math.round(s.seconds * fps);
    if (i > 0) {
      const last = i === shots.length - 1;
      // Alternate a quick whip (slide) and a hard cut; crossfade into the end card.
      items.push(
        <TransitionSeries.Transition key={`t${i}`}
          presentation={last ? fade() : i % 2 ? slide({ direction: "from-right" }) : slide({ direction: "from-bottom" })}
          timing={last ? linearTiming({ durationInFrames: T }) : springTiming({ durationInFrames: T, config: { damping: 200 } })} />
      );
    }
    items.push(
      <TransitionSeries.Sequence key={`s${i}`} durationInFrames={frames}>
        <ShotView shot={s} frames={frames} />
      </TransitionSeries.Sequence>
    );
  });
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <TransitionSeries>{items}</TransitionSeries>
      {music && <Audio src={src(music)} startFrom={Math.round(musicStart * fps)} volume={volume} />}
    </AbsoluteFill>
  );
};

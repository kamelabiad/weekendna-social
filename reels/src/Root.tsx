import React from "react";
import { Composition } from "remotion";
import { ListingReel, reelDuration, ReelProps } from "./ListingReel";
import sample from "../../posts/2026-10-majestic-byblos/reel-remotion.json";

export const FPS = 30;

export const Root: React.FC = () => (
  <Composition
    id="ListingReel"
    component={ListingReel}
    width={1080}
    height={1920}
    fps={FPS}
    durationInFrames={reelDuration(sample as ReelProps, FPS)}
    defaultProps={sample as ReelProps}
    // Props passed with --props=<file> decide the length, so any listing works.
    calculateMetadata={({ props }) => ({ durationInFrames: reelDuration(props, FPS) })}
  />
);

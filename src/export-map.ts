// Map Components mock for use in environments without `document` / `window`, like ssr pre render
import type { FC } from 'react';

function MockMap() {
  return null;
}

import { type HeatMapProps } from './HeatMap';
import { type MapProps } from './Map';
import { type PathMapProps } from './PathMap';
import { type PinMapProps } from './PinMap';

export const Map: FC<MapProps> = MockMap;
export const HeatMap: FC<HeatMapProps> = MockMap;
export const PathMap: FC<PathMapProps> = MockMap;
export const PinMap: FC<PinMapProps> = MockMap;

export type { HeatMapProps, MapProps, PathMapProps, PinMapProps };

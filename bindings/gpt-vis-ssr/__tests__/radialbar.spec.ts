import { render } from '../src';
import './utils/matcher';

describe('SSR render', () => {
  it('radialbar', async () => {
    const vis = await render({
      width: 600,
      height: 400,
      type: 'radialbar',
      data: [
        { category: 'Sports', value: 275 },
        { category: 'Strategy', value: 115 },
        { category: 'Action', value: 120 },
        { category: 'Shooter', value: 350 },
        { category: 'Other', value: 150 },
      ],
      axisXTitle: 'Type',
      axisYTitle: 'Sold',
    });

    expect(vis.toBuffer()).toImageEqual('__tests__/snapshot', 'radialbar');
  });

  it('radialbar-required', async () => {
    const vis = await render({
      type: 'radialbar',
      data: [
        { category: 'Sports', value: 275 },
        { category: 'Strategy', value: 115 },
        { category: 'Action', value: 120 },
        { category: 'Shooter', value: 350 },
        { category: 'Other', value: 150 },
      ],
    });

    expect(vis.toBuffer()).toImageEqual('__tests__/snapshot', 'radialbar-required');
  });

  it('radialbar-grouped', async () => {
    const vis = await render({
      width: 600,
      height: 400,
      type: 'radialbar',
      data: [
        { group: 'London', category: 'Jan.', value: 18.9 },
        { group: 'London', category: 'Feb.', value: 28.8 },
        { group: 'London', category: 'Mar.', value: 39.3 },
        { group: 'London', category: 'Apr.', value: 81.4 },
        { group: 'London', category: 'May', value: 47 },
        { group: 'London', category: 'Jun.', value: 20.3 },
        { group: 'London', category: 'Jul.', value: 24 },
        { group: 'London', category: 'Aug.', value: 35.6 },
        { group: 'Berlin', category: 'Jan.', value: 12.4 },
        { group: 'Berlin', category: 'Feb.', value: 23.2 },
        { group: 'Berlin', category: 'Mar.', value: 34.5 },
        { group: 'Berlin', category: 'Apr.', value: 99.7 },
        { group: 'Berlin', category: 'May', value: 52.6 },
        { group: 'Berlin', category: 'Jun.', value: 35.5 },
        { group: 'Berlin', category: 'Jul.', value: 37.4 },
        { group: 'Berlin', category: 'Aug.', value: 42.4 },
      ],
      group: true,
      axisXTitle: 'Month',
      axisYTitle: 'Temperature',
    });

    expect(vis.toBuffer()).toImageEqual('__tests__/snapshot', 'radialbar-grouped');
  });

  it('radialbar-stacked', async () => {
    const vis = await render({
      width: 600,
      height: 400,
      type: 'radialbar',
      data: [
        { group: 'London', category: 'Jan.', value: 18.9 },
        { group: 'London', category: 'Feb.', value: 28.8 },
        { group: 'London', category: 'Mar.', value: 39.3 },
        { group: 'London', category: 'Apr.', value: 81.4 },
        { group: 'London', category: 'May', value: 47 },
        { group: 'London', category: 'Jun.', value: 20.3 },
        { group: 'London', category: 'Jul.', value: 24 },
        { group: 'London', category: 'Aug.', value: 35.6 },
        { group: 'Berlin', category: 'Jan.', value: 12.4 },
        { group: 'Berlin', category: 'Feb.', value: 23.2 },
        { group: 'Berlin', category: 'Mar.', value: 34.5 },
        { group: 'Berlin', category: 'Apr.', value: 99.7 },
        { group: 'Berlin', category: 'May', value: 52.6 },
        { group: 'Berlin', category: 'Jun.', value: 35.5 },
        { group: 'Berlin', category: 'Jul.', value: 37.4 },
        { group: 'Berlin', category: 'Aug.', value: 42.4 },
      ],
      stack: true,
      axisXTitle: 'Month',
      axisYTitle: 'Temperature',
    });

    expect(vis.toBuffer()).toImageEqual('__tests__/snapshot', 'radialbar-stacked');
  });

  it('radialbar-grouped', async () => {
    const vis = await render({
      theme: 'academy',
      width: 600,
      height: 400,
      type: 'radialbar',
      data: [
        { group: 'London', category: 'Jan.', value: 18.9 },
        { group: 'London', category: 'Feb.', value: 28.8 },
        { group: 'London', category: 'Mar.', value: 39.3 },
        { group: 'London', category: 'Apr.', value: 81.4 },
        { group: 'London', category: 'May', value: 47 },
        { group: 'London', category: 'Jun.', value: 20.3 },
        { group: 'London', category: 'Jul.', value: 24 },
        { group: 'London', category: 'Aug.', value: 35.6 },
        { group: 'Berlin', category: 'Jan.', value: 12.4 },
        { group: 'Berlin', category: 'Feb.', value: 23.2 },
        { group: 'Berlin', category: 'Mar.', value: 34.5 },
        { group: 'Berlin', category: 'Apr.', value: 99.7 },
        { group: 'Berlin', category: 'May', value: 52.6 },
        { group: 'Berlin', category: 'Jun.', value: 35.5 },
        { group: 'Berlin', category: 'Jul.', value: 37.4 },
        { group: 'Berlin', category: 'Aug.', value: 42.4 },
      ],
      group: true,
      axisXTitle: 'Month',
      axisYTitle: 'Temperature',
    });

    expect(vis.toBuffer()).toImageEqual('__tests__/snapshot', 'radialbar-group-academy');
  });

  it('radialbar-stacked-academy', async () => {
    const vis = await render({
      theme: 'academy',
      width: 600,
      height: 400,
      type: 'radialbar',
      data: [
        { group: 'London', category: 'Jan.', value: 18.9 },
        { group: 'London', category: 'Feb.', value: 28.8 },
        { group: 'London', category: 'Mar.', value: 39.3 },
        { group: 'London', category: 'Apr.', value: 81.4 },
        { group: 'London', category: 'May', value: 47 },
        { group: 'London', category: 'Jun.', value: 20.3 },
        { group: 'London', category: 'Jul.', value: 24 },
        { group: 'London', category: 'Aug.', value: 35.6 },
        { group: 'Berlin', category: 'Jan.', value: 12.4 },
        { group: 'Berlin', category: 'Feb.', value: 23.2 },
        { group: 'Berlin', category: 'Mar.', value: 34.5 },
        { group: 'Berlin', category: 'Apr.', value: 99.7 },
        { group: 'Berlin', category: 'May', value: 52.6 },
        { group: 'Berlin', category: 'Jun.', value: 35.5 },
        { group: 'Berlin', category: 'Jul.', value: 37.4 },
        { group: 'Berlin', category: 'Aug.', value: 42.4 },
      ],
      stack: true,
      axisXTitle: 'Month',
      axisYTitle: 'Temperature',
    });

    expect(vis.toBuffer()).toImageEqual('__tests__/snapshot', 'radialbar-stacked-academy');
  });
});

const React = require('react')

const createMockComponent = (name) => {
  const Mock = ({ children }) => React.createElement('div', { 'data-testid': name }, children)
  Mock.displayName = name
  return Mock
}

module.exports = {
  ResponsiveContainer: createMockComponent('ResponsiveContainer'),
  AreaChart: createMockComponent('AreaChart'),
  Area: () => null,
  BarChart: createMockComponent('BarChart'),
  Bar: () => null,
  LineChart: createMockComponent('LineChart'),
  Line: () => null,
  RadarChart: createMockComponent('RadarChart'),
  Radar: () => null,
  PolarGrid: () => null,
  PolarAngleAxis: () => null,
  PolarRadiusAxis: () => null,
  XAxis: () => null,
  YAxis: () => null,
  CartesianGrid: () => null,
  Tooltip: () => null,
  Legend: () => null,
  ReferenceLine: () => null,
  Cell: () => null,
  ComposedChart: createMockComponent('ComposedChart'),
  ScatterChart: createMockComponent('ScatterChart'),
  Scatter: () => null,
  PieChart: createMockComponent('PieChart'),
  Pie: () => null,
}

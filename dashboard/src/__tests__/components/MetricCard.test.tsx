import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import { MetricCard } from '@/components/ui/MetricCard'

describe('MetricCard', () => {
  const mockMetric = {
    label: 'Test Metric',
    value: '$100M',
    unit: 'USD',
    trend: 'up' as const,
    change: 5,
    changeLabel: 'YoY',
  }

  it('renders the metric label', () => {
    render(<MetricCard metric={mockMetric} />)
    expect(screen.getByText('Test Metric')).toBeInTheDocument()
  })

  it('renders the metric value', () => {
    render(<MetricCard metric={mockMetric} />)
    expect(screen.getByText('$100M')).toBeInTheDocument()
  })

  it('renders the unit', () => {
    render(<MetricCard metric={mockMetric} />)
    expect(screen.getByText('USD')).toBeInTheDocument()
  })

  it('renders trend indicator for upward trend', () => {
    render(<MetricCard metric={mockMetric} />)
    expect(screen.getByText(/↑/)).toBeInTheDocument()
  })

  it('renders trend indicator for downward trend', () => {
    render(<MetricCard metric={{ ...mockMetric, trend: 'down' }} />)
    expect(screen.getByText(/↓/)).toBeInTheDocument()
  })

  it('renders trend indicator for neutral trend', () => {
    render(<MetricCard metric={{ ...mockMetric, trend: 'neutral' }} />)
    expect(screen.getByText(/→/)).toBeInTheDocument()
  })

  it('renders without optional unit', () => {
    const { unit: _unit, ...metricWithoutUnit } = mockMetric
    render(<MetricCard metric={metricWithoutUnit} />)
    expect(screen.getByText('Test Metric')).toBeInTheDocument()
    expect(screen.queryByText('USD')).not.toBeInTheDocument()
  })

  it('renders without optional change', () => {
    const { change: _change, changeLabel: _changeLabel, ...metricWithoutChange } = mockMetric
    render(<MetricCard metric={metricWithoutChange} />)
    expect(screen.getByText('Test Metric')).toBeInTheDocument()
    expect(screen.queryByText(/YoY/)).not.toBeInTheDocument()
  })

  it('accepts additional className', () => {
    const { container } = render(<MetricCard metric={mockMetric} className="extra-class" />)
    expect(container.firstChild).toHaveClass('extra-class')
  })
})

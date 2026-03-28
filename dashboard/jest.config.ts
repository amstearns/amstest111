import type { Config } from 'jest'

const config: Config = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': '<rootDir>/__mocks__/styleMock.js',
    '^recharts$': '<rootDir>/__mocks__/recharts.js',
    '^next/navigation$': '<rootDir>/__mocks__/next-navigation.js',
    '^next/font/(.*)$': '<rootDir>/__mocks__/next-font.js',
  },
  transform: {
    '^.+\\.(ts|tsx)$': ['ts-jest', {
      tsconfig: {
        jsx: 'react-jsx',
      },
    }],
  },
  testMatch: ['**/__tests__/**/*.test.{ts,tsx}'],
}

export default config

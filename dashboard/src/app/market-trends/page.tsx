import { NavBar } from "@/components/layout/NavBar";
import { MarketTrendsClient } from "./MarketTrendsClient";
import { getMarketData } from "@/lib/api";

export default async function MarketTrendsPage() {
  const data = await getMarketData();

  return (
    <>
      <NavBar
        title="Market Trends"
        subtitle="Green building & clean energy adoption rates across North America"
      />
      <div className="flex-1 p-6 overflow-auto">
        <MarketTrendsClient data={data} />
      </div>
    </>
  );
}

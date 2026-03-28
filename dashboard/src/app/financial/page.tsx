import { NavBar } from "@/components/layout/NavBar";
import { FinancialClient } from "./FinancialClient";
import { getFinancialData } from "@/lib/api";

export default async function FinancialPage() {
  const data = await getFinancialData();

  return (
    <>
      <NavBar
        title="Financial Analysis"
        subtitle="ROI calculator, scenario modeling, and investment returns"
      />
      <div className="flex-1 p-6 overflow-auto">
        <FinancialClient data={data} />
      </div>
    </>
  );
}

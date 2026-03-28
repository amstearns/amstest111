import { NavBar } from "@/components/layout/NavBar";
import { RegulatoryClient } from "./RegulatoryClient";
import { getRegulatoryData } from "@/lib/api";

export default async function RegulatoryPage() {
  const data = await getRegulatoryData();

  return (
    <>
      <NavBar
        title="Regulatory Incentives"
        subtitle="Federal and state policies with financial impact quantification"
      />
      <div className="flex-1 p-6 overflow-auto">
        <RegulatoryClient data={data} />
      </div>
    </>
  );
}

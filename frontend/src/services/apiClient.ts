export interface MetricsResponse {
  total_revenue: number;
  mom_growth_rate: number;
  average_ticket: number;
  total_leads: number;
  monthly_revenue: Record<string, number>; // ex: {"2025-01": 1000, "2025-02": 1200}
}

export const uploadCsv = async (file: File): Promise<MetricsResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("/api/upload-csv", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.text();
    throw new Error(`Upload failed: ${errorData}`);
  }

  return response.json();
};

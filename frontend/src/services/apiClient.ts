export interface MetricsResponse {
  total_revenue: number;
  mom_growth_rate: number;
  average_ticket: number;
  total_leads: number;
  monthly_revenue: Record<string, number>;
}

export const uploadCsv = async (file: File): Promise<MetricsResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("/api/upload-csv", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      errorText || `Upload failed with status ${response.status}`
    );
  }

  return response.json();
};

export interface MetricsResponse {
  total_revenue: number;
  mom_growth_rate: number;
  average_ticket: number;
  total_leads: number;
  monthly_revenue: Record<string, number>;
  report_id: string;
}

const getApiBaseUrl = (): string => {
  const baseUrl = import.meta.env.VITE_API_BASE_URL;

  if (!baseUrl) {
    console.warn("VITE_API_BASE_URL is not defined. Using default /api.");
    return "/api";
  }

  return baseUrl.endsWith("/") ? baseUrl.slice(0, -1) : baseUrl;
};

export const uploadCsv = async (file: File): Promise<MetricsResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const apiUrl = `${getApiBaseUrl()}/upload-csv`;

  const response = await fetch(apiUrl, {
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

export const downloadExcel = (reportId: string): void => {
  window.location.href = `${getApiBaseUrl()}/export/excel/${reportId}`;
};

export const downloadPdf = (reportId: string): void => {
  window.location.href = `${getApiBaseUrl()}/export/pdf/${reportId}`;
};

import { createFileRoute } from "@tanstack/react-router";
import { useState, useRef, useCallback } from "react";
import {
  Upload,
  Activity,
  AlertTriangle,
  CheckCircle2,
  Info,
  FileText,
  Server,
  Loader2,
  ArrowRight,
  RefreshCw,
  Terminal,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

const API_BASE_URL = "http://127.0.0.1:8000";

interface AnalysisResult {
  status: string;
  severity: "alta" | "média" | "baixa" | "informativa";
  summary: string;
  recommendation: string;
  validation_errors: string[];
  report_path: string;
}

interface HealthResponse {
  status: string;
  service?: string;
}

const severityConfig = {
  alta: {
    label: "Alta",
    variant: "destructive" as const,
    icon: AlertTriangle,
    className: "severity-high",
  },
  média: {
    label: "Média",
    variant: "default" as const,
    icon: AlertTriangle,
    className: "severity-medium",
  },
  baixa: {
    label: "Baixa",
    variant: "default" as const,
    icon: Info,
    className: "severity-low",
  },
  informativa: {
    label: "Informativa",
    variant: "default" as const,
    icon: CheckCircle2,
    className: "severity-info",
  },
};

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isHealthChecking, setIsHealthChecking] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [healthStatus, setHealthStatus] = useState<{
    ok: boolean;
    message: string;
  } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile) {
      validateAndSetFile(droppedFile);
    }
  }, []);

  const validateAndSetFile = (selectedFile: File) => {
    const allowedExtensions = [".log", ".txt"];
    const fileExtension = selectedFile.name.slice(selectedFile.name.lastIndexOf("."));

    if (!allowedExtensions.includes(fileExtension.toLowerCase())) {
      setError("Por favor, selecione apenas arquivos .log ou .txt");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setError(null);
    setResult(null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      validateAndSetFile(selectedFile);
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Nenhum arquivo selecionado. Escolha um arquivo .log ou .txt para analisar.");
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `Erro na API: ${response.status} ${response.statusText}`,
        );
      }

      const data: AnalysisResult = await response.json();
      setResult(data);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Ocorreu um erro ao analisar o log. Verifique se a API está rodando em http://127.0.0.1:8000";
      setError(message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleHealthCheck = async () => {
    setIsHealthChecking(true);
    setHealthStatus(null);

    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error(`API respondeu com status ${response.status}`);
      }

      const data: HealthResponse = await response.json();
      setHealthStatus({
        ok: data.status === "ok",
        message:
          data.status === "ok"
            ? `API online — ${data.service || "logflow-agent"}`
            : `API respondeu com status: ${data.status}`,
      });
    } catch (err) {
      setHealthStatus({
        ok: false,
        message:
          err instanceof Error
            ? `API offline — ${err.message}`
            : "API offline. Verifique se o servidor FastAPI está rodando em http://127.0.0.1:8000",
      });
    } finally {
      setIsHealthChecking(false);
    }
  };

  const clearSelection = () => {
    setFile(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const getSeverityConfig = (severity: string) => {
    return severityConfig[severity as keyof typeof severityConfig] || severityConfig.informativa;
  };

  return (
    <main className="min-h-screen bg-background px-4 py-12 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-3xl space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="mb-4 inline-flex items-center justify-center rounded-2xl bg-primary/10 p-3 ring-1 ring-primary/20">
            <Terminal className="h-8 w-8 text-primary" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
            LogFlow Agent
          </h1>
          <p className="mt-3 text-lg text-muted-foreground">
            Analise logs de pipeline com um agente LangGraph
          </p>
        </div>

        {/* Health check */}
        <Card className="border-border/60 bg-card/50 backdrop-blur">
          <CardContent className="flex flex-col items-center justify-between gap-4 p-6 sm:flex-row">
            <div className="flex items-center gap-3">
              <Server className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium text-foreground">Status da API</p>
                <p className="text-xs text-muted-foreground">{API_BASE_URL}</p>
              </div>
            </div>
            <div className="flex w-full flex-col items-center gap-3 sm:w-auto sm:flex-row">
              {healthStatus && (
                <Badge
                  variant={healthStatus.ok ? "default" : "destructive"}
                  className={healthStatus.ok ? "severity-low border-transparent" : undefined}
                >
                  {healthStatus.message}
                </Badge>
              )}
              <Button
                variant="outline"
                size="sm"
                onClick={handleHealthCheck}
                disabled={isHealthChecking}
                className="w-full sm:w-auto"
              >
                {isHealthChecking ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <RefreshCw className="mr-2 h-4 w-4" />
                )}
                Testar conexão
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Upload area */}
        <Card className="overflow-hidden border-border/60">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-xl">
              <Upload className="h-5 w-5 text-primary" />
              Upload do log
            </CardTitle>
            <CardDescription>
              Arraste um arquivo ou clique para selecionar. Apenas .log e .txt são aceitos.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`group relative cursor-pointer rounded-xl border-2 border-dashed p-8 text-center transition-all ${
                isDragging
                  ? "border-primary bg-primary/5"
                  : "border-border bg-secondary/30 hover:border-primary/50 hover:bg-secondary/50"
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".log,.txt"
                onChange={handleFileChange}
                className="sr-only"
              />
              <div className="flex flex-col items-center gap-3">
                <div className="rounded-full bg-primary/10 p-3 ring-1 ring-primary/20 transition-transform group-hover:scale-105">
                  <FileText className="h-6 w-6 text-primary" />
                </div>
                {file ? (
                  <div className="space-y-1">
                    <p className="font-medium text-foreground">{file.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                ) : (
                  <div className="space-y-1">
                    <p className="font-medium text-foreground">Clique ou arraste o arquivo aqui</p>
                    <p className="text-xs text-muted-foreground">Suporta arquivos .log e .txt</p>
                  </div>
                )}
              </div>
            </div>

            {file && (
              <div className="flex items-center justify-between rounded-lg bg-secondary/50 p-3">
                <div className="flex items-center gap-2 overflow-hidden">
                  <FileText className="h-4 w-4 shrink-0 text-primary" />
                  <span className="truncate text-sm text-foreground">{file.name}</span>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearSelection}
                  className="shrink-0 text-muted-foreground hover:text-foreground"
                >
                  Remover
                </Button>
              </div>
            )}

            <Button onClick={handleAnalyze} disabled={isAnalyzing} className="w-full" size="lg">
              {isAnalyzing ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analisando log...
                </>
              ) : (
                <>
                  <Activity className="mr-2 h-4 w-4" />
                  Analisar log
                </>
              )}
            </Button>

            {error && (
              <Alert variant="destructive">
                <AlertTriangle className="h-4 w-4" />
                <AlertTitle>Erro</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Results */}
        {result && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-foreground">Resultado da análise</h2>

            <div className="grid gap-4 sm:grid-cols-2">
              <Card className="border-border/60">
                <CardHeader className="pb-3">
                  <CardDescription>Status</CardDescription>
                  <CardTitle className="flex items-center gap-2 text-base font-medium capitalize">
                    <CheckCircle2 className="h-4 w-4 text-primary" />
                    {result.status}
                  </CardTitle>
                </CardHeader>
              </Card>

              <Card className="border-border/60">
                <CardHeader className="pb-3">
                  <CardDescription>Severidade</CardDescription>
                  <CardTitle className="text-base font-medium">
                    {(() => {
                      const config = getSeverityConfig(result.severity);
                      const Icon = config.icon;
                      return (
                        <Badge variant={config.variant} className={config.className}>
                          <Icon className="mr-1 h-3 w-3" />
                          {config.label}
                        </Badge>
                      );
                    })()}
                  </CardTitle>
                </CardHeader>
              </Card>
            </div>

            <Card className="border-border/60">
              <CardHeader>
                <CardTitle className="text-base">Resumo</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-relaxed text-foreground">{result.summary}</p>
              </CardContent>
            </Card>

            <Card className="border-l-4 border-l-primary border-border/60">
              <CardHeader>
                <CardTitle className="text-base">Recomendação</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-relaxed text-foreground">{result.recommendation}</p>
              </CardContent>
            </Card>

            <Card className="border-border/60">
              <CardHeader>
                <CardTitle className="text-base">Relatório gerado</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2 rounded-lg bg-secondary/50 p-3 font-mono text-sm text-foreground">
                  <FileText className="h-4 w-4 text-primary" />
                  {result.report_path}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Flow explanation */}
        <Card className="border-border/60 bg-card/50">
          <CardHeader>
            <CardTitle className="text-base">Como funciona o fluxo</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
              <span className="rounded-md bg-secondary px-2 py-1 text-foreground">
                Upload do log
              </span>
              <ArrowRight className="h-4 w-4" />
              <span className="rounded-md bg-secondary px-2 py-1 text-foreground">API FastAPI</span>
              <ArrowRight className="h-4 w-4" />
              <span className="rounded-md bg-secondary px-2 py-1 text-foreground">
                Agente LangGraph
              </span>
              <ArrowRight className="h-4 w-4" />
              <span className="rounded-md bg-secondary px-2 py-1 text-foreground">Relatório</span>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}

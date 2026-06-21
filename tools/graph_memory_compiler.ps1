$ROOT = "."
$GRAPH_OUTPUT = "graph_memory.json"

function Extract-Links($text) {
    $matches = [regex]::Matches($text, '\[\[(.*?)\]\]')
    $matches | ForEach-Object { $_.Groups[1].Value }
}

function Extract-Concepts($text) {
    $words = [regex]::Matches($text.ToLower(), '[a-zA-Z]{6,}')
    $words | ForEach-Object { $_.Value } | Select-Object -Unique
}

$nodes = @{}
Get-ChildItem -Path $ROOT -Recurse -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    if ($content) {
        $relPath = $_.FullName.Substring((Get-Location).Path.Length + 1)
        $nodes[$relPath] = @{
            links = @(Extract-Links $content)
            concepts = @(Extract-Concepts $content)
            size = $content.Length
        }
    }
}

$graph = @{
    nodes = @{}
    edges = @()
}

foreach ($path in $nodes.Keys) {
    $graph.nodes[$path] = $nodes[$path]
    foreach ($link in $nodes[$path].links) {
        foreach ($target in $nodes.Keys) {
            if ($target.ToLower().Contains($link.ToLower())) {
                $graph.edges += @{
                    source = $path
                    target = $target
                    type = "explicit_link"
                }
            }
        }
    }
}

Write-Host "Semantic edges disabled: keyword-overlap heuristic produces 47K noisy edges."
Write-Host "  Use: python tools/graph_memory_compiler.py --semantic (not recommended)"
Write-Host "  ML-based: python tools/semantic_graph.py (requires sentence-transformers)"
Write-Host "Writing graph JSON..."

$graphJson = $graph | ConvertTo-Json -Depth 5
Set-Content -Path $GRAPH_OUTPUT -Value $graphJson
Write-Host "Graph compiled: $($nodes.Count) nodes, $($graph.edges.Count) edges"

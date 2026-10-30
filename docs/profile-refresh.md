# Profile refresh runbook

The public page is a dated analysis of public repository evidence. A new site
design, successful Pages deployment or new software release does not by itself
refresh that evidence. Check `generated_at` in `docs/4alvit_profile.json` and the
visible generated date in the page.

## Normal operation

`Update IoT Developer Profile` runs weekly at 06:00 UTC on Monday. Scheduled jobs
can be delayed by GitHub. It scans the user and configured public organizations,
then asks the configured model to generate the narrative. The stages are:

1. Create a new temporary output directory and record the refresh start time.
2. Verify model access from the selected runner with one small synthetic request
   and a three-minute deadline. Then fetch public repository evidence and run ESPHome/D-Bus analysis with
   `--strict-scan`, then require a valid structured model response.
3. Require three nonempty output files for the requested user, zero scan errors,
   repository evidence and scan/generation timestamps from this run. Model-mode
   runs also require model-generation provenance in the JSON.
4. Stage the selected HTML/Markdown/JSON in `profile/` and `docs/`; set
   `docs/index.html` to that user's exact HTML. Unrelated maintained files remain
   untouched. Store the three validated outputs as a seven-day Actions artifact.
5. Open a signed update PR with the `automerge` label. Required checks, review and
   signed-commit rules must pass before it merges.
6. GitHub Pages publishes the merged `main` branch's `/docs` directory.

`--max-repos 100` limits enumeration for each owner. Strict scanning rejects a
listing that exceeds that limit; increase it and rerun instead of publishing a
partial inventory. Deep analysis prioritizes up to 25 repositories per analyzer
and 80 eligible files per repository, with at most 15 ESPHome or 10 D-Bus matches
per repository. These sampling limits are recorded in
`github_stats.analysis_scope` in the JSON; the profile is not an exhaustive
firmware or service inventory.

The public repository total comes from the scan inventory; the IoT repository
count is the subset retained for this profile. Complexity counts analysis records
from those IoT repositories, individual ESPHome configurations and D-Bus analyses,
so its total is not a repository count. The JSON field `total_repos_analyzed`
retains its existing name but now reports the scanned repository count.

The refresh job has a 45-minute execution limit. Concurrent refreshes queue
rather than canceling the current generation. Output from previous runs is never
used as a fallback. A failed run must not be repaired by changing only its date.

## Run a refresh now

In Actions, choose **Update IoT Developer Profile**, then **Run workflow** on
`main`. Keep `use-llm` enabled for the normal model-generated report. Equivalent CLI:

```sh
gh workflow run update-profile.yml --repo 4alvit/iot-project-builder-profile \
  --ref main -f username=4alvit -f use-llm=true
gh run list --repo 4alvit/iot-project-builder-profile --workflow update-profile.yml
```

Follow the resulting run, its generated PR and the subsequent
`pages-build-deployment` run. Compare the public page date with the merged JSON;
an Actions artifact alone is not proof of deployment.

## ARC runner routing

The trusted refresh job checks out only the default branch and receives
`BOT_PAT` only during signed publication. It therefore uses the **automation**
pool when self-hosted routing is enabled, not a pool that runs arbitrary PR code.

- `CI_RUNNER_MODE=github` or an unset variable uses GitHub-hosted Linux.
- Optional `PROFILE_RUNNER_MODE` overrides that mode for this trusted refresh
  job only. Leave it unset to inherit the shared mode. This allows a qualified
  public automation pool to reach inference from its network while all ordinary
  repository CI jobs retain their existing runner selection.
- `CI_RUNNER_MODE=self-hosted` or `k3s` selects `CI_RUNNER_AUTOMATION_LABELS`, a
  JSON array containing the registered ARC scale-set name or configured alias.
- `k3s` is a compatibility routing value, not a request for a static runner;
  there is no separate `arc` mode in this shared contract.
- Empty/malformed enabled pool labels fail admission rather than guessing a
  private pool. The workflow does not change these variables.

Verify the scale set's GitHub owner/repository scope, registration, listener and
allowed workload before switching modes. Zero idle workers can be normal for
ARC; zero workers alone does not prove a missing pool. Configured Actions
variables alone do not prove a pool exists. Do not reuse a private-repository
scale set to satisfy this public repository's queue.

For inventory and recovery procedures, use the shared
[runner documentation](https://github.com/victron-venus/venus-os-ci-toolkit/blob/main/docs/RUNNERS.md)
and [ARC recovery index](https://github.com/victron-venus/venus-os-ci-toolkit/blob/main/docs/ARC_RECOVERY.md).

## Language-model access

Set `ANTHROPIC_BASE_URL` as an Actions secret and `PROFILE_LLM_MODEL` as an
Actions variable. Set `PROFILE_INFERENCE_HOSTNAME` as a separate Actions secret
containing only that URL's hostname. The runner hardening pre-hook needs it for
the outbound allowlist and automatic masking before regular steps run. Network
telemetry upload is disabled; endpoint blocking stays enabled. Use the model ID accepted by the endpoint's Messages API,
which may differ from aliases advertised for other clients. Credentials belong
in Actions secrets: `ANTHROPIC_API_KEY` for a direct compatible API, or the pair
`PROFILE_ACCESS_CLIENT_ID` / `PROFILE_ACCESS_CLIENT_SECRET` for Cloudflare Access.
If the origin also requires an API key, configure that separately. The workflow
maps the optional `ANTHROPIC_API_KEY` secret to `PROFILE_LLM_API_KEY` for this
explicit origin credential; local Access-mode commands use `PROFILE_LLM_API_KEY`
and ignore ambient Anthropic credentials.

The endpoint must be reachable from the selected runner. GitHub-hosted runners
cannot resolve Kubernetes `*.svc.cluster.local` addresses. An ARC runner does not
automatically have permission to reach them either: respect its egress policy.
A machine-authenticated HTTPS route can keep both runner modes on the same
contract without exposing Kubernetes credentials. Such a route should accept
only `POST /v1/messages`, validate Access tokens at the origin, bound request
size and concurrency, and preserve streaming. Administrative API paths must
remain inaccessible.

The context sent to the model is derived only from the public repositories being
analyzed. Never put real keys, internal hostnames or installation identifiers in
YAML, committed commands or diagnostic artifacts. A healthy proxy or successful
model listing is not proof of inference: verify a small request using the exact
configured model, then the actual refresh. Strict model mode rejects transport
errors and malformed responses instead of silently falling back to heuristics.
The JSON records generation mode and requested model without endpoint credentials.

For an explicitly requested heuristic refresh, disable `use-llm` on a manual
run. Scheduled generation always requires the model. Rotate endpoint credentials
before their issuer's expiry and retain them in the operator's encrypted recovery
system; GitHub cannot return an existing secret value.

## Diagnose a missing update

- **Queued with no steps:** inspect the requested runner selection and ARC
  registration/listener. A job that expires while waiting for a runner never
  scanned the repositories. Check the shared routing configuration before
  retrying; recreating an old static runner is not the recovery path.
- **Timed out during generation:** inspect the last completed stage and API
  errors/rate limits. Strict scanning exits on incomplete evidence. Retry after
  the upstream problem is resolved; do not publish a partial profile.
- **Model request returns 401/403/404:** check the scoped service credentials,
  Access policy, exact Messages model ID and provider availability. Do not
  replace an unavailable model with an unreviewed paid fallback. An upstream
  model can be retired while the proxy's health check remains green.
  The preflight reports only the HTTP status, validated Cloudflare request ID
  and recognized numeric edge error, never a response body or private hostname.
  A working request from a developer's computer does not prove runner access:
  Cloudflare Bot Fight Mode can challenge datacenter addresses independently of
  Access authentication. Standard Bot Fight Mode has no per-path skip; do not
  disable zone-wide protection to repair one consumer.
- **Staging rejected a date, username or empty output:** keep the prior site.
  Inspect the fresh directory and generator error. No old `*_profile.html` is
  selected by a glob.
- **Signed publication failed:** inspect any branch created by that run before
  retrying. `BOT_PAT` needs repository content/PR permissions. If `main` moved
  during generation, regenerate from its new head; do not force-push over it.
- **PR open but page old:** review required CI, independent approval and merge
  status, then the Pages deployment. A successful generation does not bypass
  those gates.
- **Pages green but generated date old:** inspect the merged JSON. Deploying
  unchanged data only republishes the existing snapshot.

In October 2026, two refreshes exceeded the former 30-minute generation limit;
the next two waited 24 hours for the retired static `fcc` runner selection.
Pages remained healthy and continued publishing September's snapshot. Variable
based ARC-compatible routing, fresh staging and strict evidence checks address
those separate failure modes.

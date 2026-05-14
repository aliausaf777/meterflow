import { useState, useEffect, useCallback } from "react";

const API_BASE = "http://127.0.0.1:8000";

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Syne:wght@400;500;600&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Syne', sans-serif; background: #0a0a0f; color: #e8e6f0; min-height: 100vh; }
  :root {
    --bg: #0a0a0f;
    --surface: #13131a;
    --surface2: #1a1a24;
    --border: rgba(255,255,255,0.07);
    --border2: rgba(255,255,255,0.12);
    --accent: #7c6dfa;
    --accent2: #a78bfa;
    --green: #34d399;
    --red: #f87171;
    --amber: #fbbf24;
    --text: #e8e6f0;
    --muted: #6b6880;
    --mono: 'JetBrains Mono', monospace;
  }
  .app { display: flex; min-height: 100vh; }
  .sidebar {
    width: 220px; min-height: 100vh; background: var(--surface);
    border-right: 1px solid var(--border); padding: 24px 16px;
    display: flex; flex-direction: column; gap: 8px; position: fixed;
  }
  .logo { font-size: 18px; font-weight: 600; color: var(--accent2);
    padding: 0 8px 20px; border-bottom: 1px solid var(--border); margin-bottom: 8px;
    font-family: var(--mono); letter-spacing: -0.5px;
  }
  .logo span { color: var(--muted); }
  .nav-item {
    padding: 9px 12px; border-radius: 8px; cursor: pointer; font-size: 14px;
    color: var(--muted); transition: all 0.15s; display: flex; align-items: center; gap: 10px;
  }
  .nav-item:hover { background: var(--surface2); color: var(--text); }
  .nav-item.active { background: rgba(124,109,250,0.15); color: var(--accent2); }
  .nav-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; opacity: 0.6; }
  .main { margin-left: 220px; flex: 1; padding: 32px; }
  .page-title { font-size: 22px; font-weight: 600; margin-bottom: 24px; }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
  .card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px;
  }
  .stat-label { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
  .stat-value { font-size: 28px; font-weight: 600; font-family: var(--mono); }
  .stat-sub { font-size: 12px; color: var(--muted); margin-top: 4px; }
  .green { color: var(--green); }
  .red { color: var(--red); }
  .amber { color: var(--amber); }
  .accent { color: var(--accent2); }
  .section-title { font-size: 14px; font-weight: 500; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 16px;
  }
  .bar-chart { display: flex; align-items: flex-end; gap: 4px; height: 120px; }
  .bar-col { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; height: 100%; justify-content: flex-end; }
  .bar { width: 100%; border-radius: 4px 4px 0 0; background: var(--accent); opacity: 0.7; transition: opacity 0.15s; min-height: 4px; }
  .bar:hover { opacity: 1; }
  .bar-label { font-size: 9px; color: var(--muted); font-family: var(--mono); }
  .key-list { display: flex; flex-direction: column; gap: 10px; }
  .key-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px; background: var(--surface2); border-radius: 8px;
    border: 1px solid var(--border); font-size: 13px;
  }
  .key-val { font-family: var(--mono); font-size: 11px; color: var(--accent2);
    background: rgba(124,109,250,0.1); padding: 3px 8px; border-radius: 4px;
    max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .badge {
    font-size: 11px; padding: 2px 8px; border-radius: 20px; font-family: var(--mono);
  }
  .badge-green { background: rgba(52,211,153,0.15); color: var(--green); }
  .badge-red { background: rgba(248,113,113,0.15); color: var(--red); }
  .badge-amber { background: rgba(251,191,36,0.15); color: var(--amber); }
  .input {
    background: var(--surface2); border: 1px solid var(--border2);
    color: var(--text); padding: 10px 14px; border-radius: 8px;
    font-size: 14px; font-family: 'Syne', sans-serif; width: 100%; outline: none;
  }
  .input:focus { border-color: var(--accent); }
  .btn {
    background: var(--accent); color: white; border: none;
    padding: 10px 20px; border-radius: 8px; font-size: 14px;
    font-family: 'Syne', sans-serif; cursor: pointer; font-weight: 500;
    transition: opacity 0.15s;
  }
  .btn:hover { opacity: 0.85; }
  .btn-outline {
    background: transparent; color: var(--accent2);
    border: 1px solid var(--border2); padding: 8px 16px;
    border-radius: 8px; font-size: 13px; cursor: pointer;
    font-family: 'Syne', sans-serif; transition: all 0.15s;
  }
  .btn-outline:hover { border-color: var(--accent); background: rgba(124,109,250,0.08); }
  .form-group { margin-bottom: 16px; }
  .form-label { font-size: 13px; color: var(--muted); margin-bottom: 6px; display: block; }
  .alert { padding: 12px 16px; border-radius: 8px; font-size: 13px; margin-bottom: 16px; }
  .alert-err { background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.3); color: var(--red); }
  .alert-ok { background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.3); color: var(--green); }
  .log-item { padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 13px; display: flex; gap: 12px; align-items: center; }
  .log-method { font-family: var(--mono); font-size: 11px; padding: 2px 6px; border-radius: 4px; background: rgba(124,109,250,0.15); color: var(--accent2); }
  .log-path { font-family: var(--mono); font-size: 12px; color: var(--text); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .log-ms { font-family: var(--mono); font-size: 11px; color: var(--muted); }
  .plan-card { border: 1px solid var(--border); border-radius: 12px; padding: 20px; background: var(--surface); }
  .plan-card.featured { border-color: var(--accent); background: rgba(124,109,250,0.05); }
  .plan-name { font-size: 16px; font-weight: 600; margin-bottom: 4px; }
  .plan-price { font-size: 28px; font-weight: 600; font-family: var(--mono); margin: 12px 0; }
  .plan-feature { font-size: 13px; color: var(--muted); padding: 4px 0; display: flex; gap: 8px; align-items: center; }
  .plan-feature::before { content: ''; width: 5px; height: 5px; border-radius: 50%; background: var(--green); flex-shrink: 0; }
  .divider { height: 1px; background: var(--border); margin: 20px 0; }
  .gateway-url { font-family: var(--mono); font-size: 12px; background: var(--surface2);
    padding: 12px 16px; border-radius: 8px; border: 1px solid var(--border);
    word-break: break-all; color: var(--accent2); margin-top: 12px;
  }
  .row { display: flex; gap: 12px; align-items: center; }
  .flex1 { flex: 1; }
  .loading { color: var(--muted); font-size: 14px; padding: 40px 0; text-align: center; }
`;

export default function App() {
  const [page, setPage] = useState("login");
  const [token, setToken] = useState(null);
  const [, setUser] = useState(null);
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState(null);

  const api = useCallback(async (method, path, body = null, auth = true) => {
    const headers = { "Content-Type": "application/json" };
    if (auth && token) headers["Authorization"] = `Bearer ${token}`;
    const res = await fetch(`${API_BASE}${path}`, {
      method, headers,
      body: body ? JSON.stringify(body) : null
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || "Request failed");
    return json;
  }, [token]);

  const load = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    try {
      const [invoice, usage, apis] = await Promise.all([
  api("GET", "/billing/invoice?plan=free"),
  api("GET", "/billing/usage?days=7"),
  api("GET", "/apis/")
]);

let allKeys = [];

for (const apiItem of apis) {
  try {
    const apiKeys = await api("GET", `/apis/${apiItem.id}/keys`);
    allKeys = [...allKeys, ...apiKeys];
  } catch (err) {
    console.error(err);
  }
}

const gateway = await api("GET", "/gateway/my-usage");

setData({
  invoice,
  usage,
  apis,
  keys: allKeys,
  gateway
});
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  }, [token, api]);

useEffect(() => { if (token) { load(); setPage("dashboard"); } }, [token, load]);

  // ── Auth ─────────────────────────────────────────────────────
  const AuthPage = ({ mode }) => {
    const [form, setForm] = useState({ name: "", email: "", password: "" });
    const [err, setErr] = useState(null);

    const submit = async () => {
      setErr(null);
      try {
        if (mode === "register") {
          await api("POST", "/auth/register", form, false);
          setMsg("Registered! Please login.");
          setPage("login");
        } else {
          const res = await api("POST", "/auth/login", { email: form.email, password: form.password }, false);
          setToken(res.access_token);
          setUser({ email: form.email });
        }
      } catch (e) { setErr(e.message); }
    };

    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", minHeight: "100vh" }}>
        <div style={{ width: 360 }}>
          <div style={{ fontFamily: "var(--mono)", fontSize: 22, color: "var(--accent2)", marginBottom: 32, textAlign: "center" }}>
            Meter<span style={{ color: "var(--muted)" }}>Flow</span>
          </div>
          <div className="card">
            <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 20 }}>
              {mode === "login" ? "Sign in" : "Create account"}
            </div>
            {err && <div className="alert alert-err">{err}</div>}
            {msg && <div className="alert alert-ok">{msg}</div>}
            {mode === "register" && (
              <div className="form-group">
                <label className="form-label">Name</label>
                <input className="input" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
              </div>
            )}
            <div className="form-group">
              <label className="form-label">Email</label>
              <input className="input" type="email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Password</label>
              <input className="input" type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} />
            </div>
            <button className="btn" style={{ width: "100%", marginTop: 8 }} onClick={submit}>
              {mode === "login" ? "Sign in" : "Create account"}
            </button>
            <div style={{ textAlign: "center", marginTop: 16, fontSize: 13, color: "var(--muted)" }}>
              {mode === "login" ? "No account? " : "Have an account? "}
              <span style={{ color: "var(--accent2)", cursor: "pointer" }}
                onClick={() => { setPage(mode === "login" ? "register" : "login"); setMsg(null); }}>
                {mode === "login" ? "Register" : "Sign in"}
              </span>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // ── Dashboard ─────────────────────────────────────────────────
  const Dashboard = () => {
    const { invoice, usage, gateway } = data;
    const chartData = usage?.chart_data || [];
    const max = Math.max(...chartData.map(d => d.total), 1);

    return (
      <>
        <div className="page-title">Overview</div>
        <div className="grid-4">
          {[
            { label: "Total Requests", value: invoice?.usage?.total_requests ?? 0, color: "accent" },
            { label: "Billable", value: invoice?.usage?.billable_requests ?? 0, color: "" },
            { label: "Amount Due", value: `₹${invoice?.cost?.total_amount ?? 0}`, color: "green" },
            { label: "Success Rate", value: gateway?.success_rate ?? "—", color: "green" },
          ].map(s => (
            <div className="card" key={s.label}>
              <div className="stat-label">{s.label}</div>
              <div className={`stat-value ${s.color}`}>{s.value}</div>
            </div>
          ))}
        </div>

        <div className="grid-2">
          <div className="card">
            <div className="section-title">Requests — last 7 days</div>
            {chartData.length === 0 ? (
              <div style={{ color: "var(--muted)", fontSize: 13, padding: "20px 0" }}>
                Hit the gateway URL to generate data
              </div>
            ) : (
              <div className="bar-chart">
                {chartData.map((d, i) => (
                  <div className="bar-col" key={i}>
                    <div className="bar" style={{ height: `${Math.max((d.total / max) * 100, 4)}%` }} title={`${d.total} requests`} />
                    <div className="bar-label">{d.date.slice(5)}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="card">
            <div className="section-title">Recent Requests</div>
            {gateway?.recent_requests?.length > 0 ? (
              gateway.recent_requests.map((r, i) => (
                <div className="log-item" key={i}>
                  <span className="log-method">{r.method}</span>
                  <span className="log-path">{r.endpoint}</span>
                  <span className={`badge ${r.success ? "badge-green" : "badge-red"}`}>{r.status_code}</span>
                  <span className="log-ms">{r.latency_ms}ms</span>
                </div>
              ))
            ) : (
              <div style={{ color: "var(--muted)", fontSize: 13 }}>No requests yet</div>
            )}
          </div>
        </div>

        <div className="card">
          <div className="section-title">Gateway URL</div>
          <div style={{ fontSize: 13, color: "var(--muted)" }}>
            Use this URL to route API calls through MeterFlow:
          </div>
          <div className="gateway-url">
  {data.keys?.find(k => k.status === "active")
    ? `http://127.0.0.1:8000/gateway/${
        data.keys.find(k => k.status === "active").key_value
      }/your-endpoint`
    : "Generate an API key first in the APIs section"}
</div>
        </div>
      </>
    );
  };

  // ── APIs Page ────────────────────────────────────────────────
  const APIsPage = () => {
    const [form, setForm] = useState({ name: "", description: "", base_url: "" });
    const [err, setErr] = useState(null);
    const [ok, setOk] = useState(null);

    const createAPI = async () => {
      setErr(null); setOk(null);
      try {
        await api("POST", "/apis/", form);
        setOk("API created!");
        setForm({ name: "", description: "", base_url: "" });
        load();
      } catch (e) { setErr(e.message); }
    };

    const genKey = async (apiId) => {
      try {
        await api("POST", `/apis/${apiId}/keys`, { name: "Key " + Date.now() });
        setOk("Key generated!"); load();
      } catch (e) { setErr(e.message); }
    };

    const revokeKey = async (keyId) => {
      try {
        await api("PATCH", `/apis/keys/${keyId}/revoke`);
        setOk("Key revoked!"); load();
      } catch (e) { setErr(e.message); }
    };

    return (
      <>
        <div className="page-title">API Management</div>
        {err && <div className="alert alert-err">{err}</div>}
        {ok && <div className="alert alert-ok">{ok}</div>}

        <div className="grid-2">
          <div className="card">
            <div className="section-title">Register New API</div>
            <div className="form-group">
              <label className="form-label">Name</label>
              <input className="input" value={form.name} placeholder="Pokemon API"
                onChange={e => setForm({ ...form, name: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Base URL</label>
              <input className="input" value={form.base_url} placeholder="https://pokeapi.co/api/v2"
                onChange={e => setForm({ ...form, base_url: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Description</label>
              <input className="input" value={form.description} placeholder="Optional"
                onChange={e => setForm({ ...form, description: e.target.value })} />
            </div>
            <button className="btn" onClick={createAPI}>Register API</button>
          </div>

          <div className="card">
            <div className="section-title">Your APIs</div>
            {data.apis?.length === 0 && <div style={{ color: "var(--muted)", fontSize: 13 }}>No APIs yet</div>}
            {data.apis?.map(a => (
              <div key={a.id} style={{ marginBottom: 16 }}>
                <div className="row" style={{ marginBottom: 8 }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 500, fontSize: 14 }}>{a.name}</div>
                    <div style={{ fontSize: 12, color: "var(--muted)", fontFamily: "var(--mono)" }}>{a.base_url}</div>
                  </div>
                  <button className="btn-outline" onClick={() => genKey(a.id)}>+ Key</button>
                </div>
                <div className="key-list">
                  {data.keys?.filter(k => k.api_id === a.id).map(k => (
                    <div className="key-item" key={k.id}>
                      <div>
                        <div style={{ fontSize: 12, color: "var(--muted)", marginBottom: 4 }}>{k.name}</div>
                        <div className="key-val">{k.key_value}</div>
                      </div>
                      <div className="row" style={{ gap: 8 }}>
                        <span className={`badge ${k.status === "active" ? "badge-green" : "badge-red"}`}>{k.status}</span>
                        {k.status === "active" && (
                          <button className="btn-outline" style={{ fontSize: 11, padding: "4px 10px", color: "var(--red)" }}
                            onClick={() => revokeKey(k.id)}>Revoke</button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </>
    );
  };

  // ── Billing Page ──────────────────────────────────────────────
 const BillingPage = () => {
  const { invoice } = data;
  const [paying, setPaying] = useState(null);

  const handlePayment = async (planId, amount) => {
    if (amount === 0) return;
    setPaying(planId);
    try {
      const order = await api("POST", "/payments/create-order", { plan: planId });
      
      const options = {
        key: order.key_id,
        amount: order.amount * 100,
        currency: "INR",
        name: "MeterFlow",
        description: `${planId} Plan`,
        order_id: order.order_id,
        handler: async (response) => {
          const verify = await api("POST", "/payments/verify", {
            razorpay_order_id: response.razorpay_order_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_signature: response.razorpay_signature,
            plan: planId
          });
          if (verify.success) alert(`✅ ${verify.message}`);
        },
        prefill: { email: "ausaf@test.com" },
        theme: { color: "#7c6dfa" }
      };

      const rzp = new window.Razorpay(options);
      rzp.open();
    } catch (e) { alert("Payment failed: " + e.message); }
    setPaying(null);
  };

  const plans = [
    { id: "free", name: "Free", price: "₹0", amount: 0, requests: "1,000", per100: "₹0" },
    { id: "pro", name: "Pro", price: "₹499", amount: 499, requests: "5,000", per100: "₹0.50", featured: true },
    { id: "enterprise", name: "Enterprise", price: "₹2,999", amount: 2999, requests: "50,000", per100: "₹0.20" },
  ];

  return (
    <>
      <div className="page-title">Billing</div>
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="section-title">Current Invoice — {invoice?.billing_period?.start} to {invoice?.billing_period?.end}</div>
        <div className="grid-4">
          {[
            { label: "Total Requests", value: invoice?.usage?.total_requests ?? 0 },
            { label: "Free Tier", value: invoice?.usage?.free_requests ?? 0 },
            { label: "Billable", value: invoice?.usage?.billable_requests ?? 0 },
            { label: "Amount Due", value: `₹${invoice?.cost?.total_amount ?? 0}`, color: "green" },
          ].map(s => (
            <div key={s.label} style={{ padding: "12px", background: "var(--surface2)", borderRadius: 8 }}>
              <div className="stat-label">{s.label}</div>
              <div className={`stat-value ${s.color || ""}`} style={{ fontSize: 22 }}>{s.value}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="section-title">Upgrade Plan</div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
        {plans.map(p => (
          <div className={`plan-card ${p.featured ? "featured" : ""}`} key={p.id}>
            {p.featured && <div className="badge badge-amber" style={{ marginBottom: 12, display: "inline-block" }}>Most Popular</div>}
            <div className="plan-name">{p.name}</div>
            <div className="plan-price" style={{ color: p.featured ? "var(--accent2)" : "var(--text)" }}>
              {p.price}<span style={{ fontSize: 14, color: "var(--muted)", fontWeight: 400 }}>/mo</span>
            </div>
            <div className="divider" />
            <div className="plan-feature">{p.requests} free requests/month</div>
            <div className="plan-feature">{p.per100} per 100 after free tier</div>
            <div className="plan-feature">API key management</div>
            <div className="plan-feature">Usage analytics</div>
            {p.featured && <div className="plan-feature">Priority support</div>}
            <button
              className="btn"
              style={{ width: "100%", marginTop: 16, opacity: p.amount === 0 ? 0.5 : 1 }}
              onClick={() => handlePayment(p.id, p.amount)}
              disabled={p.amount === 0 || paying === p.id}
            >
              {p.amount === 0 ? "Current Plan" : paying === p.id ? "Processing..." : `Upgrade to ${p.name}`}
            </button>
          </div>
        ))}
      </div>
    </>
  );
};

  // ── Layout ────────────────────────────────────────────────────
  if (page === "login" || page === "register") {
    return (
      <>
        <style>{styles}</style>
        <AuthPage mode={page} />
      </>
    );
  }

  const navItems = [
    { id: "dashboard", label: "Dashboard" },
    { id: "apis", label: "APIs" },
    { id: "billing", label: "Billing" },
  ];

  return (
    <>
      <style>{styles}</style>
      <div className="app">
        <div className="sidebar">
          <div className="logo">Meter<span>Flow</span></div>
          {navItems.map(n => (
            <div key={n.id} className={`nav-item ${page === n.id ? "active" : ""}`}
              onClick={() => setPage(n.id)}>
              <span className="nav-dot" />
              {n.label}
            </div>
          ))}
          <div style={{ flex: 1 }} />
          <div className="nav-item" style={{ color: "var(--red)" }}
            onClick={() => { setToken(null); setUser(null); setPage("login"); }}>
            <span className="nav-dot" />
            Sign out
          </div>
        </div>
        <div className="main">
          {loading ? <div className="loading">Loading...</div> : (
            page === "dashboard" ? <Dashboard /> :
            page === "apis" ? <APIsPage /> :
            page === "billing" ? <BillingPage /> : null
          )}
        </div>
      </div>
    </>
  );
}
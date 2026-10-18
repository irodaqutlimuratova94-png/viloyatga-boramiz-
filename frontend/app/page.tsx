"use client";

import { useEffect, useState } from "react";

type Trip = {
  id: number; driver_user_id: number; origin_region: string; destination_region: string;
  origin_address: string; destination_address: string; departure_at: string; seats_available: number;
  price_uzs: string; car_make_model: string; note?: string | null; return_trip: boolean; status: string;
};
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [regions, setRegions] = useState<string[]>([]);
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [trips, setTrips] = useState<Trip[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API}/api/regions`).then(r => r.json()).then(d => setRegions(d.regions ?? [])).catch(() => setError("API bilan bog‘lanib bo‘lmadi."));
    fetchTrips();
  }, []);

  async function fetchTrips() {
    setLoading(true); setError("");
    try {
      const params = new URLSearchParams();
      if (origin) params.set("origin", origin);
      if (destination) params.set("destination", destination);
      const response = await fetch(`${API}/api/trips?${params.toString()}`);
      if (!response.ok) throw new Error("Safarlarni yuklab bo‘lmadi.");
      setTrips(await response.json());
    } catch (e) { setError(e instanceof Error ? e.message : "Noma’lum xatolik."); }
    finally { setLoading(false); }
  }

  return (
    <main className="min-h-screen">
      <header className="border-b border-emerald-950/10 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <a className="flex items-center gap-3 font-bold text-xl tracking-tight text-emerald-950" href="#">
            <span className="grid h-10 w-10 place-items-center rounded-2xl bg-emerald-800 text-white">VB</span>
            Viloyatga Boramiz
          </a>
          <a href="#joylash" className="rounded-xl bg-emerald-800 px-4 py-3 text-sm font-semibold text-white hover:bg-emerald-900">Safar joylash</a>
        </div>
      </header>

      <section className="bg-emerald-950 text-white">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-14 md:grid-cols-[1.1fr_.9fr] md:py-20">
          <div className="flex flex-col justify-center">
            <p className="mb-4 inline-flex w-fit rounded-full border border-white/20 px-3 py-1 text-sm text-emerald-100">O‘zbekiston bo‘ylab safarlar</p>
            <h1 className="max-w-2xl text-4xl font-bold leading-tight md:text-6xl">Manzilingiz bir,<br/>yo‘lingiz bir.</h1>
            <p className="mt-5 max-w-xl text-lg leading-8 text-emerald-100">Viloyatlararo safaringizni toping yoki bo‘sh o‘rinlaringizni yo‘lovchilar bilan ulashing.</p>
          </div>
          <div className="rounded-3xl bg-white p-5 text-slate-900 shadow-2xl md:p-7">
            <h2 className="text-xl font-bold">Safar qidirish</h2>
            <p className="mt-1 text-sm text-slate-500">Yo‘nalishni tanlang va mavjud safarlarni ko‘ring.</p>
            <label className="mt-5 block text-sm font-semibold">Qayerdan yo‘lga chiqasiz?</label>
            <select value={origin} onChange={e => setOrigin(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-3 outline-none focus:border-emerald-700">
              <option value="">Barcha hududlar</option>{regions.map(r => <option key={r}>{r}</option>)}
            </select>
            <label className="mt-4 block text-sm font-semibold">Qayerga borasiz?</label>
            <select value={destination} onChange={e => setDestination(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-3 outline-none focus:border-emerald-700">
              <option value="">Barcha hududlar</option>{regions.filter(r => r !== origin).map(r => <option key={r}>{r}</option>)}
            </select>
            <button onClick={fetchTrips} className="mt-5 w-full rounded-xl bg-emerald-800 px-4 py-3.5 font-bold text-white hover:bg-emerald-900 disabled:opacity-60" disabled={loading}>
              {loading ? "Qidirilmoqda..." : "Safar topish"}
            </button>
            <a id="joylash" href="#safarlar" className="mt-3 block rounded-xl border border-emerald-800 px-4 py-3 text-center font-semibold text-emerald-900 hover:bg-emerald-50">Safarlar ro‘yxatini ko‘rish</a>
          </div>
        </div>
      </section>

      <section id="safarlar" className="mx-auto max-w-6xl px-4 py-12">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div><p className="text-sm font-bold uppercase tracking-widest text-emerald-800">Yo‘nalishlar</p><h2 className="mt-2 text-3xl font-bold">Yaqinlashayotgan safarlar</h2></div>
          <span className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-900">{trips.length} ta safar</span>
        </div>
        {error && <p role="alert" className="mt-5 rounded-xl bg-red-50 p-4 text-red-800">{error}</p>}
        {!loading && trips.length === 0 && <div className="mt-6 rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center"><p className="font-semibold">Hozircha mos safar topilmadi</p><p className="mt-2 text-sm text-slate-500">Boshqa yo‘nalishni tanlang yoki keyinroq qayta urinib ko‘ring.</p></div>}
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          {trips.map(t => <article key={t.id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-start justify-between gap-3"><div><p className="font-bold">{t.origin_region} <span className="text-emerald-700">→</span> {t.destination_region}</p><p className="mt-2 text-sm text-slate-500">{new Date(t.departure_at).toLocaleString("uz-UZ")}</p></div><p className="whitespace-nowrap text-lg font-bold text-emerald-900">{Number(t.price_uzs).toLocaleString("uz-UZ")} so‘m</p></div>
            <div className="mt-4 grid gap-2 text-sm text-slate-700"><p>📍 {t.origin_address} → {t.destination_address}</p><p>🚘 {t.car_make_model}</p><p>💺 {t.seats_available} ta bo‘sh o‘rin {t.return_trip ? "· Qaytish safari bor" : ""}</p>{t.note && <p className="text-slate-500">{t.note}</p>}</div>
            <p className="mt-4 rounded-lg bg-amber-50 px-3 py-2 text-xs text-amber-900">Haydovchi bilan aloqa funksiyasi autentifikatsiya va rozilik moduli ulangach faollashtiriladi.</p>
          </article>)}
        </div>
      </section>

      <section className="border-y border-slate-200 bg-white">
        <div className="mx-auto grid max-w-6xl gap-8 px-4 py-12 md:grid-cols-3">
          {[["01","Yo‘nalishni tanlang","Kerakli hudud va safar sanasini belgilang."],["02","Takliflarni solishtiring","Narx, vaqt va bo‘sh o‘rinlarni ko‘rib chiqing."],["03","Safarni kelishing","Haydovchi bilan bog‘lanib, uchrashuv joyini aniqlashtiring."]].map(x => <div key={x[0]}><p className="text-sm font-bold text-emerald-700">{x[0]}</p><h3 className="mt-2 text-lg font-bold">{x[1]}</h3><p className="mt-2 leading-6 text-slate-600">{x[2]}</p></div>)}
        </div>
      </section>
      <footer className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-8 text-sm text-slate-500 sm:flex-row sm:justify-between"><span>© 2026 Viloyatga Boramiz</span><span>Manzilingiz bir, yo‘lingiz bir.</span></footer>
    </main>
  );
}

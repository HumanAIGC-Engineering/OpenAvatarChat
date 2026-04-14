;(function () {
  const t = document.createElement('link').relList
  if (t && t.supports && t.supports('modulepreload')) return
  for (const o of document.querySelectorAll('link[rel="modulepreload"]')) r(o)
  new MutationObserver((o) => {
    for (const i of o)
      if (i.type === 'childList')
        for (const s of i.addedNodes) s.tagName === 'LINK' && s.rel === 'modulepreload' && r(s)
  }).observe(document, { childList: !0, subtree: !0 })
  function n(o) {
    const i = {}
    return (
      o.integrity && (i.integrity = o.integrity),
      o.referrerPolicy && (i.referrerPolicy = o.referrerPolicy),
      o.crossOrigin === 'use-credentials'
        ? (i.credentials = 'include')
        : o.crossOrigin === 'anonymous'
          ? (i.credentials = 'omit')
          : (i.credentials = 'same-origin'),
      i
    )
  }
  function r(o) {
    if (o.ep) return
    o.ep = !0
    const i = n(o)
    fetch(o.href, i)
  }
})()
/**
 * @vue/shared v3.5.22
 * (c) 2018-present Yuxi (Evan) You and Vue contributors
 * @license MIT
 **/ function Ri(e) {
  const t = Object.create(null)
  for (const n of e.split(',')) t[n] = 1
  return (n) => n in t
}
const re = {},
  dn = [],
  lt = () => {},
  ul = () => !1,
  oo = (e) =>
    e.charCodeAt(0) === 111 &&
    e.charCodeAt(1) === 110 &&
    (e.charCodeAt(2) > 122 || e.charCodeAt(2) < 97),
  Li = (e) => e.startsWith('onUpdate:'),
  de = Object.assign,
  Hi = (e, t) => {
    const n = e.indexOf(t)
    n > -1 && e.splice(n, 1)
  },
  Sf = Object.prototype.hasOwnProperty,
  te = (e, t) => Sf.call(e, t),
  K = Array.isArray,
  pn = (e) => io(e) === '[object Map]',
  fl = (e) => io(e) === '[object Set]',
  X = (e) => typeof e == 'function',
  ce = (e) => typeof e == 'string',
  _t = (e) => typeof e == 'symbol',
  oe = (e) => e !== null && typeof e == 'object',
  dl = (e) => (oe(e) || X(e)) && X(e.then) && X(e.catch),
  pl = Object.prototype.toString,
  io = (e) => pl.call(e),
  _f = (e) => io(e).slice(8, -1),
  hl = (e) => io(e) === '[object Object]',
  Fi = (e) => ce(e) && e !== 'NaN' && e[0] !== '-' && '' + parseInt(e, 10) === e,
  Un = Ri(
    ',key,ref,ref_for,ref_key,onVnodeBeforeMount,onVnodeMounted,onVnodeBeforeUpdate,onVnodeUpdated,onVnodeBeforeUnmount,onVnodeUnmounted'
  ),
  so = (e) => {
    const t = Object.create(null)
    return (n) => t[n] || (t[n] = e(n))
  },
  wf = /-\w/g,
  Ve = so((e) => e.replace(wf, (t) => t.slice(1).toUpperCase())),
  Of = /\B([A-Z])/g,
  nn = so((e) => e.replace(Of, '-$1').toLowerCase()),
  ao = so((e) => e.charAt(0).toUpperCase() + e.slice(1)),
  Mo = so((e) => (e ? `on${ao(e)}` : '')),
  bt = (e, t) => !Object.is(e, t),
  Io = (e, ...t) => {
    for (let n = 0; n < e.length; n++) e[n](...t)
  },
  gl = (e, t, n, r = !1) => {
    Object.defineProperty(e, t, { configurable: !0, enumerable: !1, writable: r, value: n })
  },
  Tf = (e) => {
    const t = parseFloat(e)
    return isNaN(t) ? e : t
  },
  $f = (e) => {
    const t = ce(e) ? Number(e) : NaN
    return isNaN(t) ? e : t
  }
let Ps
const lo = () =>
  Ps ||
  (Ps =
    typeof globalThis < 'u'
      ? globalThis
      : typeof self < 'u'
        ? self
        : typeof window < 'u'
          ? window
          : typeof global < 'u'
            ? global
            : {})
function ki(e) {
  if (K(e)) {
    const t = {}
    for (let n = 0; n < e.length; n++) {
      const r = e[n],
        o = ce(r) ? Mf(r) : ki(r)
      if (o) for (const i in o) t[i] = o[i]
    }
    return t
  } else if (ce(e) || oe(e)) return e
}
const Pf = /;(?![^(]*\))/g,
  Ef = /:([^]+)/,
  Af = /\/\*[^]*?\*\//g
function Mf(e) {
  const t = {}
  return (
    e
      .replace(Af, '')
      .split(Pf)
      .forEach((n) => {
        if (n) {
          const r = n.split(Ef)
          r.length > 1 && (t[r[0].trim()] = r[1].trim())
        }
      }),
    t
  )
}
function Ni(e) {
  let t = ''
  if (ce(e)) t = e
  else if (K(e))
    for (let n = 0; n < e.length; n++) {
      const r = Ni(e[n])
      r && (t += r + ' ')
    }
  else if (oe(e)) for (const n in e) e[n] && (t += n + ' ')
  return t.trim()
}
const If = 'itemscope,allowfullscreen,formnovalidate,ismap,nomodule,novalidate,readonly',
  jf = Ri(If)
function ml(e) {
  return !!e || e === ''
}
const vl = (e) => !!(e && e.__v_isRef === !0),
  Rf = (e) =>
    ce(e)
      ? e
      : e == null
        ? ''
        : K(e) || (oe(e) && (e.toString === pl || !X(e.toString)))
          ? vl(e)
            ? Rf(e.value)
            : JSON.stringify(e, yl, 2)
          : String(e),
  yl = (e, t) =>
    vl(t)
      ? yl(e, t.value)
      : pn(t)
        ? {
            [`Map(${t.size})`]: [...t.entries()].reduce(
              (n, [r, o], i) => ((n[jo(r, i) + ' =>'] = o), n),
              {}
            ),
          }
        : fl(t)
          ? { [`Set(${t.size})`]: [...t.values()].map((n) => jo(n)) }
          : _t(t)
            ? jo(t)
            : oe(t) && !K(t) && !hl(t)
              ? String(t)
              : t,
  jo = (e, t = '') => {
    var n
    return _t(e) ? `Symbol(${(n = e.description) != null ? n : t})` : e
  }
/**
 * @vue/reactivity v3.5.22
 * (c) 2018-present Yuxi (Evan) You and Vue contributors
 * @license MIT
 **/ let Ce
class bl {
  constructor(t = !1) {
    ;((this.detached = t),
      (this._active = !0),
      (this._on = 0),
      (this.effects = []),
      (this.cleanups = []),
      (this._isPaused = !1),
      (this.parent = Ce),
      !t && Ce && (this.index = (Ce.scopes || (Ce.scopes = [])).push(this) - 1))
  }
  get active() {
    return this._active
  }
  pause() {
    if (this._active) {
      this._isPaused = !0
      let t, n
      if (this.scopes) for (t = 0, n = this.scopes.length; t < n; t++) this.scopes[t].pause()
      for (t = 0, n = this.effects.length; t < n; t++) this.effects[t].pause()
    }
  }
  resume() {
    if (this._active && this._isPaused) {
      this._isPaused = !1
      let t, n
      if (this.scopes) for (t = 0, n = this.scopes.length; t < n; t++) this.scopes[t].resume()
      for (t = 0, n = this.effects.length; t < n; t++) this.effects[t].resume()
    }
  }
  run(t) {
    if (this._active) {
      const n = Ce
      try {
        return ((Ce = this), t())
      } finally {
        Ce = n
      }
    }
  }
  on() {
    ++this._on === 1 && ((this.prevScope = Ce), (Ce = this))
  }
  off() {
    this._on > 0 && --this._on === 0 && ((Ce = this.prevScope), (this.prevScope = void 0))
  }
  stop(t) {
    if (this._active) {
      this._active = !1
      let n, r
      for (n = 0, r = this.effects.length; n < r; n++) this.effects[n].stop()
      for (this.effects.length = 0, n = 0, r = this.cleanups.length; n < r; n++) this.cleanups[n]()
      if (((this.cleanups.length = 0), this.scopes)) {
        for (n = 0, r = this.scopes.length; n < r; n++) this.scopes[n].stop(!0)
        this.scopes.length = 0
      }
      if (!this.detached && this.parent && !t) {
        const o = this.parent.scopes.pop()
        o && o !== this && ((this.parent.scopes[this.index] = o), (o.index = this.index))
      }
      this.parent = void 0
    }
  }
}
function Cl(e) {
  return new bl(e)
}
function xl() {
  return Ce
}
function Lf(e, t = !1) {
  Ce && Ce.cleanups.push(e)
}
let se
const Ro = new WeakSet()
class Sl {
  constructor(t) {
    ;((this.fn = t),
      (this.deps = void 0),
      (this.depsTail = void 0),
      (this.flags = 5),
      (this.next = void 0),
      (this.cleanup = void 0),
      (this.scheduler = void 0),
      Ce && Ce.active && Ce.effects.push(this))
  }
  pause() {
    this.flags |= 64
  }
  resume() {
    this.flags & 64 && ((this.flags &= -65), Ro.has(this) && (Ro.delete(this), this.trigger()))
  }
  notify() {
    ;(this.flags & 2 && !(this.flags & 32)) || this.flags & 8 || wl(this)
  }
  run() {
    if (!(this.flags & 1)) return this.fn()
    ;((this.flags |= 2), Es(this), Ol(this))
    const t = se,
      n = Xe
    ;((se = this), (Xe = !0))
    try {
      return this.fn()
    } finally {
      ;(Tl(this), (se = t), (Xe = n), (this.flags &= -3))
    }
  }
  stop() {
    if (this.flags & 1) {
      for (let t = this.deps; t; t = t.nextDep) zi(t)
      ;((this.deps = this.depsTail = void 0),
        Es(this),
        this.onStop && this.onStop(),
        (this.flags &= -2))
    }
  }
  trigger() {
    this.flags & 64 ? Ro.add(this) : this.scheduler ? this.scheduler() : this.runIfDirty()
  }
  runIfDirty() {
    ni(this) && this.run()
  }
  get dirty() {
    return ni(this)
  }
}
let _l = 0,
  Gn,
  Kn
function wl(e, t = !1) {
  if (((e.flags |= 8), t)) {
    ;((e.next = Kn), (Kn = e))
    return
  }
  ;((e.next = Gn), (Gn = e))
}
function Di() {
  _l++
}
function Bi() {
  if (--_l > 0) return
  if (Kn) {
    let t = Kn
    for (Kn = void 0; t; ) {
      const n = t.next
      ;((t.next = void 0), (t.flags &= -9), (t = n))
    }
  }
  let e
  for (; Gn; ) {
    let t = Gn
    for (Gn = void 0; t; ) {
      const n = t.next
      if (((t.next = void 0), (t.flags &= -9), t.flags & 1))
        try {
          t.trigger()
        } catch (r) {
          e || (e = r)
        }
      t = n
    }
  }
  if (e) throw e
}
function Ol(e) {
  for (let t = e.deps; t; t = t.nextDep)
    ((t.version = -1), (t.prevActiveLink = t.dep.activeLink), (t.dep.activeLink = t))
}
function Tl(e) {
  let t,
    n = e.depsTail,
    r = n
  for (; r; ) {
    const o = r.prevDep
    ;(r.version === -1 ? (r === n && (n = o), zi(r), Hf(r)) : (t = r),
      (r.dep.activeLink = r.prevActiveLink),
      (r.prevActiveLink = void 0),
      (r = o))
  }
  ;((e.deps = t), (e.depsTail = n))
}
function ni(e) {
  for (let t = e.deps; t; t = t.nextDep)
    if (
      t.dep.version !== t.version ||
      (t.dep.computed && ($l(t.dep.computed) || t.dep.version !== t.version))
    )
      return !0
  return !!e._dirty
}
function $l(e) {
  if (
    (e.flags & 4 && !(e.flags & 16)) ||
    ((e.flags &= -17), e.globalVersion === nr) ||
    ((e.globalVersion = nr), !e.isSSR && e.flags & 128 && ((!e.deps && !e._dirty) || !ni(e)))
  )
    return
  e.flags |= 2
  const t = e.dep,
    n = se,
    r = Xe
  ;((se = e), (Xe = !0))
  try {
    Ol(e)
    const o = e.fn(e._value)
    ;(t.version === 0 || bt(o, e._value)) && ((e.flags |= 128), (e._value = o), t.version++)
  } catch (o) {
    throw (t.version++, o)
  } finally {
    ;((se = n), (Xe = r), Tl(e), (e.flags &= -3))
  }
}
function zi(e, t = !1) {
  const { dep: n, prevSub: r, nextSub: o } = e
  if (
    (r && ((r.nextSub = o), (e.prevSub = void 0)),
    o && ((o.prevSub = r), (e.nextSub = void 0)),
    n.subs === e && ((n.subs = r), !r && n.computed))
  ) {
    n.computed.flags &= -5
    for (let i = n.computed.deps; i; i = i.nextDep) zi(i, !0)
  }
  !t && !--n.sc && n.map && n.map.delete(n.key)
}
function Hf(e) {
  const { prevDep: t, nextDep: n } = e
  ;(t && ((t.nextDep = n), (e.prevDep = void 0)), n && ((n.prevDep = t), (e.nextDep = void 0)))
}
let Xe = !0
const Pl = []
function xt() {
  ;(Pl.push(Xe), (Xe = !1))
}
function St() {
  const e = Pl.pop()
  Xe = e === void 0 ? !0 : e
}
function Es(e) {
  const { cleanup: t } = e
  if (((e.cleanup = void 0), t)) {
    const n = se
    se = void 0
    try {
      t()
    } finally {
      se = n
    }
  }
}
let nr = 0
class Ff {
  constructor(t, n) {
    ;((this.sub = t),
      (this.dep = n),
      (this.version = n.version),
      (this.nextDep = this.prevDep = this.nextSub = this.prevSub = this.prevActiveLink = void 0))
  }
}
class co {
  constructor(t) {
    ;((this.computed = t),
      (this.version = 0),
      (this.activeLink = void 0),
      (this.subs = void 0),
      (this.map = void 0),
      (this.key = void 0),
      (this.sc = 0),
      (this.__v_skip = !0))
  }
  track(t) {
    if (!se || !Xe || se === this.computed) return
    let n = this.activeLink
    if (n === void 0 || n.sub !== se)
      ((n = this.activeLink = new Ff(se, this)),
        se.deps
          ? ((n.prevDep = se.depsTail), (se.depsTail.nextDep = n), (se.depsTail = n))
          : (se.deps = se.depsTail = n),
        El(n))
    else if (n.version === -1 && ((n.version = this.version), n.nextDep)) {
      const r = n.nextDep
      ;((r.prevDep = n.prevDep),
        n.prevDep && (n.prevDep.nextDep = r),
        (n.prevDep = se.depsTail),
        (n.nextDep = void 0),
        (se.depsTail.nextDep = n),
        (se.depsTail = n),
        se.deps === n && (se.deps = r))
    }
    return n
  }
  trigger(t) {
    ;(this.version++, nr++, this.notify(t))
  }
  notify(t) {
    Di()
    try {
      for (let n = this.subs; n; n = n.prevSub) n.sub.notify() && n.sub.dep.notify()
    } finally {
      Bi()
    }
  }
}
function El(e) {
  if ((e.dep.sc++, e.sub.flags & 4)) {
    const t = e.dep.computed
    if (t && !e.dep.subs) {
      t.flags |= 20
      for (let r = t.deps; r; r = r.nextDep) El(r)
    }
    const n = e.dep.subs
    ;(n !== e && ((e.prevSub = n), n && (n.nextSub = e)), (e.dep.subs = e))
  }
}
const Wr = new WeakMap(),
  Gt = Symbol(''),
  ri = Symbol(''),
  rr = Symbol('')
function Se(e, t, n) {
  if (Xe && se) {
    let r = Wr.get(e)
    r || Wr.set(e, (r = new Map()))
    let o = r.get(n)
    ;(o || (r.set(n, (o = new co())), (o.map = r), (o.key = n)), o.track())
  }
}
function vt(e, t, n, r, o, i) {
  const s = Wr.get(e)
  if (!s) {
    nr++
    return
  }
  const a = (l) => {
    l && l.trigger()
  }
  if ((Di(), t === 'clear')) s.forEach(a)
  else {
    const l = K(e),
      u = l && Fi(n)
    if (l && n === 'length') {
      const c = Number(r)
      s.forEach((f, d) => {
        ;(d === 'length' || d === rr || (!_t(d) && d >= c)) && a(f)
      })
    } else
      switch (((n !== void 0 || s.has(void 0)) && a(s.get(n)), u && a(s.get(rr)), t)) {
        case 'add':
          l ? u && a(s.get('length')) : (a(s.get(Gt)), pn(e) && a(s.get(ri)))
          break
        case 'delete':
          l || (a(s.get(Gt)), pn(e) && a(s.get(ri)))
          break
        case 'set':
          pn(e) && a(s.get(Gt))
          break
      }
  }
  Bi()
}
function kf(e, t) {
  const n = Wr.get(e)
  return n && n.get(t)
}
function on(e) {
  const t = J(e)
  return t === e ? t : (Se(t, 'iterate', rr), ze(e) ? t : t.map(pe))
}
function uo(e) {
  return (Se((e = J(e)), 'iterate', rr), e)
}
const Nf = {
  __proto__: null,
  [Symbol.iterator]() {
    return Lo(this, Symbol.iterator, pe)
  },
  concat(...e) {
    return on(this).concat(...e.map((t) => (K(t) ? on(t) : t)))
  },
  entries() {
    return Lo(this, 'entries', (e) => ((e[1] = pe(e[1])), e))
  },
  every(e, t) {
    return dt(this, 'every', e, t, void 0, arguments)
  },
  filter(e, t) {
    return dt(this, 'filter', e, t, (n) => n.map(pe), arguments)
  },
  find(e, t) {
    return dt(this, 'find', e, t, pe, arguments)
  },
  findIndex(e, t) {
    return dt(this, 'findIndex', e, t, void 0, arguments)
  },
  findLast(e, t) {
    return dt(this, 'findLast', e, t, pe, arguments)
  },
  findLastIndex(e, t) {
    return dt(this, 'findLastIndex', e, t, void 0, arguments)
  },
  forEach(e, t) {
    return dt(this, 'forEach', e, t, void 0, arguments)
  },
  includes(...e) {
    return Ho(this, 'includes', e)
  },
  indexOf(...e) {
    return Ho(this, 'indexOf', e)
  },
  join(e) {
    return on(this).join(e)
  },
  lastIndexOf(...e) {
    return Ho(this, 'lastIndexOf', e)
  },
  map(e, t) {
    return dt(this, 'map', e, t, void 0, arguments)
  },
  pop() {
    return kn(this, 'pop')
  },
  push(...e) {
    return kn(this, 'push', e)
  },
  reduce(e, ...t) {
    return As(this, 'reduce', e, t)
  },
  reduceRight(e, ...t) {
    return As(this, 'reduceRight', e, t)
  },
  shift() {
    return kn(this, 'shift')
  },
  some(e, t) {
    return dt(this, 'some', e, t, void 0, arguments)
  },
  splice(...e) {
    return kn(this, 'splice', e)
  },
  toReversed() {
    return on(this).toReversed()
  },
  toSorted(e) {
    return on(this).toSorted(e)
  },
  toSpliced(...e) {
    return on(this).toSpliced(...e)
  },
  unshift(...e) {
    return kn(this, 'unshift', e)
  },
  values() {
    return Lo(this, 'values', pe)
  },
}
function Lo(e, t, n) {
  const r = uo(e),
    o = r[t]()
  return (
    r !== e &&
      !ze(e) &&
      ((o._next = o.next),
      (o.next = () => {
        const i = o._next()
        return (i.done || (i.value = n(i.value)), i)
      })),
    o
  )
}
const Df = Array.prototype
function dt(e, t, n, r, o, i) {
  const s = uo(e),
    a = s !== e && !ze(e),
    l = s[t]
  if (l !== Df[t]) {
    const f = l.apply(e, i)
    return a ? pe(f) : f
  }
  let u = n
  s !== e &&
    (a
      ? (u = function (f, d) {
          return n.call(this, pe(f), d, e)
        })
      : n.length > 2 &&
        (u = function (f, d) {
          return n.call(this, f, d, e)
        }))
  const c = l.call(s, u, r)
  return a && o ? o(c) : c
}
function As(e, t, n, r) {
  const o = uo(e)
  let i = n
  return (
    o !== e &&
      (ze(e)
        ? n.length > 3 &&
          (i = function (s, a, l) {
            return n.call(this, s, a, l, e)
          })
        : (i = function (s, a, l) {
            return n.call(this, s, pe(a), l, e)
          })),
    o[t](i, ...r)
  )
}
function Ho(e, t, n) {
  const r = J(e)
  Se(r, 'iterate', rr)
  const o = r[t](...n)
  return (o === -1 || o === !1) && Ui(n[0]) ? ((n[0] = J(n[0])), r[t](...n)) : o
}
function kn(e, t, n = []) {
  ;(xt(), Di())
  const r = J(e)[t].apply(e, n)
  return (Bi(), St(), r)
}
const Bf = Ri('__proto__,__v_isRef,__isVue'),
  Al = new Set(
    Object.getOwnPropertyNames(Symbol)
      .filter((e) => e !== 'arguments' && e !== 'caller')
      .map((e) => Symbol[e])
      .filter(_t)
  )
function zf(e) {
  _t(e) || (e = String(e))
  const t = J(this)
  return (Se(t, 'has', e), t.hasOwnProperty(e))
}
class Ml {
  constructor(t = !1, n = !1) {
    ;((this._isReadonly = t), (this._isShallow = n))
  }
  get(t, n, r) {
    if (n === '__v_skip') return t.__v_skip
    const o = this._isReadonly,
      i = this._isShallow
    if (n === '__v_isReactive') return !o
    if (n === '__v_isReadonly') return o
    if (n === '__v_isShallow') return i
    if (n === '__v_raw')
      return r === (o ? (i ? Qf : Ll) : i ? Rl : jl).get(t) ||
        Object.getPrototypeOf(t) === Object.getPrototypeOf(r)
        ? t
        : void 0
    const s = K(t)
    if (!o) {
      let l
      if (s && (l = Nf[n])) return l
      if (n === 'hasOwnProperty') return zf
    }
    const a = Reflect.get(t, n, le(t) ? t : r)
    if ((_t(n) ? Al.has(n) : Bf(n)) || (o || Se(t, 'get', n), i)) return a
    if (le(a)) {
      const l = s && Fi(n) ? a : a.value
      return o && oe(l) ? ii(l) : l
    }
    return oe(a) ? (o ? ii(a) : ct(a)) : a
  }
}
class Il extends Ml {
  constructor(t = !1) {
    super(!1, t)
  }
  set(t, n, r, o) {
    let i = t[n]
    if (!this._isShallow) {
      const l = jt(i)
      if ((!ze(r) && !jt(r) && ((i = J(i)), (r = J(r))), !K(t) && le(i) && !le(r)))
        return (l || (i.value = r), !0)
    }
    const s = K(t) && Fi(n) ? Number(n) < t.length : te(t, n),
      a = Reflect.set(t, n, r, le(t) ? t : o)
    return (t === J(o) && (s ? bt(r, i) && vt(t, 'set', n, r) : vt(t, 'add', n, r)), a)
  }
  deleteProperty(t, n) {
    const r = te(t, n)
    t[n]
    const o = Reflect.deleteProperty(t, n)
    return (o && r && vt(t, 'delete', n, void 0), o)
  }
  has(t, n) {
    const r = Reflect.has(t, n)
    return ((!_t(n) || !Al.has(n)) && Se(t, 'has', n), r)
  }
  ownKeys(t) {
    return (Se(t, 'iterate', K(t) ? 'length' : Gt), Reflect.ownKeys(t))
  }
}
class Wf extends Ml {
  constructor(t = !1) {
    super(!0, t)
  }
  set(t, n) {
    return !0
  }
  deleteProperty(t, n) {
    return !0
  }
}
const Vf = new Il(),
  Uf = new Wf(),
  Gf = new Il(!0)
const oi = (e) => e,
  Cr = (e) => Reflect.getPrototypeOf(e)
function Kf(e, t, n) {
  return function (...r) {
    const o = this.__v_raw,
      i = J(o),
      s = pn(i),
      a = e === 'entries' || (e === Symbol.iterator && s),
      l = e === 'keys' && s,
      u = o[e](...r),
      c = n ? oi : t ? Vr : pe
    return (
      !t && Se(i, 'iterate', l ? ri : Gt),
      {
        next() {
          const { value: f, done: d } = u.next()
          return d ? { value: f, done: d } : { value: a ? [c(f[0]), c(f[1])] : c(f), done: d }
        },
        [Symbol.iterator]() {
          return this
        },
      }
    )
  }
}
function xr(e) {
  return function (...t) {
    return e === 'delete' ? !1 : e === 'clear' ? void 0 : this
  }
}
function Xf(e, t) {
  const n = {
    get(o) {
      const i = this.__v_raw,
        s = J(i),
        a = J(o)
      e || (bt(o, a) && Se(s, 'get', o), Se(s, 'get', a))
      const { has: l } = Cr(s),
        u = t ? oi : e ? Vr : pe
      if (l.call(s, o)) return u(i.get(o))
      if (l.call(s, a)) return u(i.get(a))
      i !== s && i.get(o)
    },
    get size() {
      const o = this.__v_raw
      return (!e && Se(J(o), 'iterate', Gt), o.size)
    },
    has(o) {
      const i = this.__v_raw,
        s = J(i),
        a = J(o)
      return (
        e || (bt(o, a) && Se(s, 'has', o), Se(s, 'has', a)),
        o === a ? i.has(o) : i.has(o) || i.has(a)
      )
    },
    forEach(o, i) {
      const s = this,
        a = s.__v_raw,
        l = J(a),
        u = t ? oi : e ? Vr : pe
      return (!e && Se(l, 'iterate', Gt), a.forEach((c, f) => o.call(i, u(c), u(f), s)))
    },
  }
  return (
    de(
      n,
      e
        ? { add: xr('add'), set: xr('set'), delete: xr('delete'), clear: xr('clear') }
        : {
            add(o) {
              !t && !ze(o) && !jt(o) && (o = J(o))
              const i = J(this)
              return (Cr(i).has.call(i, o) || (i.add(o), vt(i, 'add', o, o)), this)
            },
            set(o, i) {
              !t && !ze(i) && !jt(i) && (i = J(i))
              const s = J(this),
                { has: a, get: l } = Cr(s)
              let u = a.call(s, o)
              u || ((o = J(o)), (u = a.call(s, o)))
              const c = l.call(s, o)
              return (s.set(o, i), u ? bt(i, c) && vt(s, 'set', o, i) : vt(s, 'add', o, i), this)
            },
            delete(o) {
              const i = J(this),
                { has: s, get: a } = Cr(i)
              let l = s.call(i, o)
              ;(l || ((o = J(o)), (l = s.call(i, o))), a && a.call(i, o))
              const u = i.delete(o)
              return (l && vt(i, 'delete', o, void 0), u)
            },
            clear() {
              const o = J(this),
                i = o.size !== 0,
                s = o.clear()
              return (i && vt(o, 'clear', void 0, void 0), s)
            },
          }
    ),
    ['keys', 'values', 'entries', Symbol.iterator].forEach((o) => {
      n[o] = Kf(o, e, t)
    }),
    n
  )
}
function Wi(e, t) {
  const n = Xf(e, t)
  return (r, o, i) =>
    o === '__v_isReactive'
      ? !e
      : o === '__v_isReadonly'
        ? e
        : o === '__v_raw'
          ? r
          : Reflect.get(te(n, o) && o in r ? n : r, o, i)
}
const qf = { get: Wi(!1, !1) },
  Yf = { get: Wi(!1, !0) },
  Jf = { get: Wi(!0, !1) }
const jl = new WeakMap(),
  Rl = new WeakMap(),
  Ll = new WeakMap(),
  Qf = new WeakMap()
function Zf(e) {
  switch (e) {
    case 'Object':
    case 'Array':
      return 1
    case 'Map':
    case 'Set':
    case 'WeakMap':
    case 'WeakSet':
      return 2
    default:
      return 0
  }
}
function ed(e) {
  return e.__v_skip || !Object.isExtensible(e) ? 0 : Zf(_f(e))
}
function ct(e) {
  return jt(e) ? e : Vi(e, !1, Vf, qf, jl)
}
function td(e) {
  return Vi(e, !1, Gf, Yf, Rl)
}
function ii(e) {
  return Vi(e, !0, Uf, Jf, Ll)
}
function Vi(e, t, n, r, o) {
  if (!oe(e) || (e.__v_raw && !(t && e.__v_isReactive))) return e
  const i = ed(e)
  if (i === 0) return e
  const s = o.get(e)
  if (s) return s
  const a = new Proxy(e, i === 2 ? r : n)
  return (o.set(e, a), a)
}
function Ct(e) {
  return jt(e) ? Ct(e.__v_raw) : !!(e && e.__v_isReactive)
}
function jt(e) {
  return !!(e && e.__v_isReadonly)
}
function ze(e) {
  return !!(e && e.__v_isShallow)
}
function Ui(e) {
  return e ? !!e.__v_raw : !1
}
function J(e) {
  const t = e && e.__v_raw
  return t ? J(t) : e
}
function Gi(e) {
  return (!te(e, '__v_skip') && Object.isExtensible(e) && gl(e, '__v_skip', !0), e)
}
const pe = (e) => (oe(e) ? ct(e) : e),
  Vr = (e) => (oe(e) ? ii(e) : e)
function le(e) {
  return e ? e.__v_isRef === !0 : !1
}
function qe(e) {
  return Hl(e, !1)
}
function We(e) {
  return Hl(e, !0)
}
function Hl(e, t) {
  return le(e) ? e : new nd(e, t)
}
class nd {
  constructor(t, n) {
    ;((this.dep = new co()),
      (this.__v_isRef = !0),
      (this.__v_isShallow = !1),
      (this._rawValue = n ? t : J(t)),
      (this._value = n ? t : pe(t)),
      (this.__v_isShallow = n))
  }
  get value() {
    return (this.dep.track(), this._value)
  }
  set value(t) {
    const n = this._rawValue,
      r = this.__v_isShallow || ze(t) || jt(t)
    ;((t = r ? t : J(t)),
      bt(t, n) && ((this._rawValue = t), (this._value = r ? t : pe(t)), this.dep.trigger()))
  }
}
function rd(e) {
  e.dep && e.dep.trigger()
}
function Jt(e) {
  return le(e) ? e.value : e
}
function Kv(e) {
  return X(e) ? e() : Jt(e)
}
const od = {
  get: (e, t, n) => (t === '__v_raw' ? e : Jt(Reflect.get(e, t, n))),
  set: (e, t, n, r) => {
    const o = e[t]
    return le(o) && !le(n) ? ((o.value = n), !0) : Reflect.set(e, t, n, r)
  },
}
function Fl(e) {
  return Ct(e) ? e : new Proxy(e, od)
}
class id {
  constructor(t) {
    ;((this.__v_isRef = !0), (this._value = void 0))
    const n = (this.dep = new co()),
      { get: r, set: o } = t(n.track.bind(n), n.trigger.bind(n))
    ;((this._get = r), (this._set = o))
  }
  get value() {
    return (this._value = this._get())
  }
  set value(t) {
    this._set(t)
  }
}
function Xv(e) {
  return new id(e)
}
function sd(e) {
  const t = K(e) ? new Array(e.length) : {}
  for (const n in e) t[n] = kl(e, n)
  return t
}
class ad {
  constructor(t, n, r) {
    ;((this._object = t),
      (this._key = n),
      (this._defaultValue = r),
      (this.__v_isRef = !0),
      (this._value = void 0))
  }
  get value() {
    const t = this._object[this._key]
    return (this._value = t === void 0 ? this._defaultValue : t)
  }
  set value(t) {
    this._object[this._key] = t
  }
  get dep() {
    return kf(J(this._object), this._key)
  }
}
class ld {
  constructor(t) {
    ;((this._getter = t), (this.__v_isRef = !0), (this.__v_isReadonly = !0), (this._value = void 0))
  }
  get value() {
    return (this._value = this._getter())
  }
}
function cd(e, t, n) {
  return le(e) ? e : X(e) ? new ld(e) : oe(e) && arguments.length > 1 ? kl(e, t, n) : qe(e)
}
function kl(e, t, n) {
  const r = e[t]
  return le(r) ? r : new ad(e, t, n)
}
class ud {
  constructor(t, n, r) {
    ;((this.fn = t),
      (this.setter = n),
      (this._value = void 0),
      (this.dep = new co(this)),
      (this.__v_isRef = !0),
      (this.deps = void 0),
      (this.depsTail = void 0),
      (this.flags = 16),
      (this.globalVersion = nr - 1),
      (this.next = void 0),
      (this.effect = this),
      (this.__v_isReadonly = !n),
      (this.isSSR = r))
  }
  notify() {
    if (((this.flags |= 16), !(this.flags & 8) && se !== this)) return (wl(this, !0), !0)
  }
  get value() {
    const t = this.dep.track()
    return ($l(this), t && (t.version = this.dep.version), this._value)
  }
  set value(t) {
    this.setter && this.setter(t)
  }
}
function fd(e, t, n = !1) {
  let r, o
  return (X(e) ? (r = e) : ((r = e.get), (o = e.set)), new ud(r, o, n))
}
const Sr = {},
  Ur = new WeakMap()
let Bt
function dd(e, t = !1, n = Bt) {
  if (n) {
    let r = Ur.get(n)
    ;(r || Ur.set(n, (r = [])), r.push(e))
  }
}
function pd(e, t, n = re) {
  const { immediate: r, deep: o, once: i, scheduler: s, augmentJob: a, call: l } = n,
    u = (x) => (o ? x : ze(x) || o === !1 || o === 0 ? yt(x, 1) : yt(x))
  let c,
    f,
    d,
    p,
    m = !1,
    v = !1
  if (
    (le(e)
      ? ((f = () => e.value), (m = ze(e)))
      : Ct(e)
        ? ((f = () => u(e)), (m = !0))
        : K(e)
          ? ((v = !0),
            (m = e.some((x) => Ct(x) || ze(x))),
            (f = () =>
              e.map((x) => {
                if (le(x)) return x.value
                if (Ct(x)) return u(x)
                if (X(x)) return l ? l(x, 2) : x()
              })))
          : X(e)
            ? t
              ? (f = l ? () => l(e, 2) : e)
              : (f = () => {
                  if (d) {
                    xt()
                    try {
                      d()
                    } finally {
                      St()
                    }
                  }
                  const x = Bt
                  Bt = c
                  try {
                    return l ? l(e, 3, [p]) : e(p)
                  } finally {
                    Bt = x
                  }
                })
            : (f = lt),
    t && o)
  ) {
    const x = f,
      _ = o === !0 ? 1 / 0 : o
    f = () => yt(x(), _)
  }
  const b = xl(),
    C = () => {
      ;(c.stop(), b && b.active && Hi(b.effects, c))
    }
  if (i && t) {
    const x = t
    t = (..._) => {
      ;(x(..._), C())
    }
  }
  let O = v ? new Array(e.length).fill(Sr) : Sr
  const P = (x) => {
    if (!(!(c.flags & 1) || (!c.dirty && !x)))
      if (t) {
        const _ = c.run()
        if (o || m || (v ? _.some((H, y) => bt(H, O[y])) : bt(_, O))) {
          d && d()
          const H = Bt
          Bt = c
          try {
            const y = [_, O === Sr ? void 0 : v && O[0] === Sr ? [] : O, p]
            ;((O = _), l ? l(t, 3, y) : t(...y))
          } finally {
            Bt = H
          }
        }
      } else c.run()
  }
  return (
    a && a(P),
    (c = new Sl(f)),
    (c.scheduler = s ? () => s(P, !1) : P),
    (p = (x) => dd(x, !1, c)),
    (d = c.onStop =
      () => {
        const x = Ur.get(c)
        if (x) {
          if (l) l(x, 4)
          else for (const _ of x) _()
          Ur.delete(c)
        }
      }),
    t ? (r ? P(!0) : (O = c.run())) : s ? s(P.bind(null, !0), !0) : c.run(),
    (C.pause = c.pause.bind(c)),
    (C.resume = c.resume.bind(c)),
    (C.stop = C),
    C
  )
}
function yt(e, t = 1 / 0, n) {
  if (t <= 0 || !oe(e) || e.__v_skip || ((n = n || new Map()), (n.get(e) || 0) >= t)) return e
  if ((n.set(e, t), t--, le(e))) yt(e.value, t, n)
  else if (K(e)) for (let r = 0; r < e.length; r++) yt(e[r], t, n)
  else if (fl(e) || pn(e))
    e.forEach((r) => {
      yt(r, t, n)
    })
  else if (hl(e)) {
    for (const r in e) yt(e[r], t, n)
    for (const r of Object.getOwnPropertySymbols(e))
      Object.prototype.propertyIsEnumerable.call(e, r) && yt(e[r], t, n)
  }
  return e
}
/**
 * @vue/runtime-core v3.5.22
 * (c) 2018-present Yuxi (Evan) You and Vue contributors
 * @license MIT
 **/ function dr(e, t, n, r) {
  try {
    return r ? e(...r) : e()
  } catch (o) {
    fo(o, t, n)
  }
}
function Je(e, t, n, r) {
  if (X(e)) {
    const o = dr(e, t, n, r)
    return (
      o &&
        dl(o) &&
        o.catch((i) => {
          fo(i, t, n)
        }),
      o
    )
  }
  if (K(e)) {
    const o = []
    for (let i = 0; i < e.length; i++) o.push(Je(e[i], t, n, r))
    return o
  }
}
function fo(e, t, n, r = !0) {
  const o = t ? t.vnode : null,
    { errorHandler: i, throwUnhandledErrorInProduction: s } = (t && t.appContext.config) || re
  if (t) {
    let a = t.parent
    const l = t.proxy,
      u = `https://vuejs.org/error-reference/#runtime-${n}`
    for (; a; ) {
      const c = a.ec
      if (c) {
        for (let f = 0; f < c.length; f++) if (c[f](e, l, u) === !1) return
      }
      a = a.parent
    }
    if (i) {
      ;(xt(), dr(i, null, 10, [e, l, u]), St())
      return
    }
  }
  hd(e, n, o, r, s)
}
function hd(e, t, n, r = !0, o = !1) {
  if (o) throw e
  console.error(e)
}
const Te = []
let it = -1
const hn = []
let Et = null,
  an = 0
const Nl = Promise.resolve()
let Gr = null
function po(e) {
  const t = Gr || Nl
  return e ? t.then(this ? e.bind(this) : e) : t
}
function gd(e) {
  let t = it + 1,
    n = Te.length
  for (; t < n; ) {
    const r = (t + n) >>> 1,
      o = Te[r],
      i = or(o)
    i < e || (i === e && o.flags & 2) ? (t = r + 1) : (n = r)
  }
  return t
}
function Ki(e) {
  if (!(e.flags & 1)) {
    const t = or(e),
      n = Te[Te.length - 1]
    ;(!n || (!(e.flags & 2) && t >= or(n)) ? Te.push(e) : Te.splice(gd(t), 0, e),
      (e.flags |= 1),
      Dl())
  }
}
function Dl() {
  Gr || (Gr = Nl.then(zl))
}
function md(e) {
  ;(K(e)
    ? hn.push(...e)
    : Et && e.id === -1
      ? Et.splice(an + 1, 0, e)
      : e.flags & 1 || (hn.push(e), (e.flags |= 1)),
    Dl())
}
function Ms(e, t, n = it + 1) {
  for (; n < Te.length; n++) {
    const r = Te[n]
    if (r && r.flags & 2) {
      if (e && r.id !== e.uid) continue
      ;(Te.splice(n, 1), n--, r.flags & 4 && (r.flags &= -2), r(), r.flags & 4 || (r.flags &= -2))
    }
  }
}
function Bl(e) {
  if (hn.length) {
    const t = [...new Set(hn)].sort((n, r) => or(n) - or(r))
    if (((hn.length = 0), Et)) {
      Et.push(...t)
      return
    }
    for (Et = t, an = 0; an < Et.length; an++) {
      const n = Et[an]
      ;(n.flags & 4 && (n.flags &= -2), n.flags & 8 || n(), (n.flags &= -2))
    }
    ;((Et = null), (an = 0))
  }
}
const or = (e) => (e.id == null ? (e.flags & 2 ? -1 : 1 / 0) : e.id)
function zl(e) {
  try {
    for (it = 0; it < Te.length; it++) {
      const t = Te[it]
      t &&
        !(t.flags & 8) &&
        (t.flags & 4 && (t.flags &= -2), dr(t, t.i, t.i ? 15 : 14), t.flags & 4 || (t.flags &= -2))
    }
  } finally {
    for (; it < Te.length; it++) {
      const t = Te[it]
      t && (t.flags &= -2)
    }
    ;((it = -1), (Te.length = 0), Bl(), (Gr = null), (Te.length || hn.length) && zl())
  }
}
let ge = null,
  Wl = null
function Kr(e) {
  const t = ge
  return ((ge = e), (Wl = (e && e.type.__scopeId) || null), t)
}
function vd(e, t = ge, n) {
  if (!t || e._n) return e
  const r = (...o) => {
    r._d && Yr(-1)
    const i = Kr(t)
    let s
    try {
      s = e(...o)
    } finally {
      ;(Kr(i), r._d && Yr(1))
    }
    return s
  }
  return ((r._n = !0), (r._c = !0), (r._d = !0), r)
}
function qv(e, t) {
  if (ge === null) return e
  const n = yo(ge),
    r = e.dirs || (e.dirs = [])
  for (let o = 0; o < t.length; o++) {
    let [i, s, a, l = re] = t[o]
    i &&
      (X(i) && (i = { mounted: i, updated: i }),
      i.deep && yt(s),
      r.push({ dir: i, instance: n, value: s, oldValue: void 0, arg: a, modifiers: l }))
  }
  return e
}
function kt(e, t, n, r) {
  const o = e.dirs,
    i = t && t.dirs
  for (let s = 0; s < o.length; s++) {
    const a = o[s]
    i && (a.oldValue = i[s].value)
    let l = a.dir[r]
    l && (xt(), Je(l, n, 8, [e.el, a, e, t]), St())
  }
}
const Vl = Symbol('_vte'),
  Ul = (e) => e.__isTeleport,
  Xn = (e) => e && (e.disabled || e.disabled === ''),
  Is = (e) => e && (e.defer || e.defer === ''),
  js = (e) => typeof SVGElement < 'u' && e instanceof SVGElement,
  Rs = (e) => typeof MathMLElement == 'function' && e instanceof MathMLElement,
  si = (e, t) => {
    const n = e && e.to
    return ce(n) ? (t ? t(n) : null) : n
  },
  Gl = {
    name: 'Teleport',
    __isTeleport: !0,
    process(e, t, n, r, o, i, s, a, l, u) {
      const {
          mc: c,
          pc: f,
          pbc: d,
          o: { insert: p, querySelector: m, createText: v, createComment: b },
        } = u,
        C = Xn(t.props)
      let { shapeFlag: O, children: P, dynamicChildren: x } = t
      if (e == null) {
        const _ = (t.el = v('')),
          H = (t.anchor = v(''))
        ;(p(_, n, r), p(H, n, r))
        const y = ($, W) => {
            O & 16 && c(P, $, W, o, i, s, a, l)
          },
          E = () => {
            const $ = (t.target = si(t.props, m)),
              W = Xl($, t, v, p)
            $ &&
              (s !== 'svg' && js($) ? (s = 'svg') : s !== 'mathml' && Rs($) && (s = 'mathml'),
              o && o.isCE && (o.ce._teleportTargets || (o.ce._teleportTargets = new Set())).add($),
              C || (y($, W), Mr(t, !1)))
          }
        ;(C && (y(n, H), Mr(t, !0)),
          Is(t.props)
            ? ((t.el.__isMounted = !1),
              Oe(() => {
                ;(E(), delete t.el.__isMounted)
              }, i))
            : E())
      } else {
        if (Is(t.props) && e.el.__isMounted === !1) {
          Oe(() => {
            Gl.process(e, t, n, r, o, i, s, a, l, u)
          }, i)
          return
        }
        ;((t.el = e.el), (t.targetStart = e.targetStart))
        const _ = (t.anchor = e.anchor),
          H = (t.target = e.target),
          y = (t.targetAnchor = e.targetAnchor),
          E = Xn(e.props),
          $ = E ? n : H,
          W = E ? _ : y
        if (
          (s === 'svg' || js(H) ? (s = 'svg') : (s === 'mathml' || Rs(H)) && (s = 'mathml'),
          x
            ? (d(e.dynamicChildren, x, $, o, i, s, a), ns(e, t, !0))
            : l || f(e, t, $, W, o, i, s, a, !1),
          C)
        )
          E
            ? t.props && e.props && t.props.to !== e.props.to && (t.props.to = e.props.to)
            : _r(t, n, _, u, 1)
        else if ((t.props && t.props.to) !== (e.props && e.props.to)) {
          const Y = (t.target = si(t.props, m))
          Y && _r(t, Y, null, u, 0)
        } else E && _r(t, H, y, u, 1)
        Mr(t, C)
      }
    },
    remove(e, t, n, { um: r, o: { remove: o } }, i) {
      const {
        shapeFlag: s,
        children: a,
        anchor: l,
        targetStart: u,
        targetAnchor: c,
        target: f,
        props: d,
      } = e
      if ((f && (o(u), o(c)), i && o(l), s & 16)) {
        const p = i || !Xn(d)
        for (let m = 0; m < a.length; m++) {
          const v = a[m]
          r(v, t, n, p, !!v.dynamicChildren)
        }
      }
    },
    move: _r,
    hydrate: yd,
  }
function _r(e, t, n, { o: { insert: r }, m: o }, i = 2) {
  i === 0 && r(e.targetAnchor, t, n)
  const { el: s, anchor: a, shapeFlag: l, children: u, props: c } = e,
    f = i === 2
  if ((f && r(s, t, n), (!f || Xn(c)) && l & 16))
    for (let d = 0; d < u.length; d++) o(u[d], t, n, 2)
  f && r(a, t, n)
}
function yd(
  e,
  t,
  n,
  r,
  o,
  i,
  { o: { nextSibling: s, parentNode: a, querySelector: l, insert: u, createText: c } },
  f
) {
  function d(v, b, C, O) {
    ;((b.anchor = f(s(v), b, a(v), n, r, o, i)), (b.targetStart = C), (b.targetAnchor = O))
  }
  const p = (t.target = si(t.props, l)),
    m = Xn(t.props)
  if (p) {
    const v = p._lpa || p.firstChild
    if (t.shapeFlag & 16)
      if (m) d(e, t, v, v && s(v))
      else {
        t.anchor = s(e)
        let b = v
        for (; b; ) {
          if (b && b.nodeType === 8) {
            if (b.data === 'teleport start anchor') t.targetStart = b
            else if (b.data === 'teleport anchor') {
              ;((t.targetAnchor = b), (p._lpa = t.targetAnchor && s(t.targetAnchor)))
              break
            }
          }
          b = s(b)
        }
        ;(t.targetAnchor || Xl(p, t, c, u), f(v && s(v), t, p, n, r, o, i))
      }
    Mr(t, m)
  } else m && t.shapeFlag & 16 && d(e, t, e, s(e))
  return t.anchor && s(t.anchor)
}
const Kl = Gl
function Mr(e, t) {
  const n = e.ctx
  if (n && n.ut) {
    let r, o
    for (
      t ? ((r = e.el), (o = e.anchor)) : ((r = e.targetStart), (o = e.targetAnchor));
      r && r !== o;

    )
      (r.nodeType === 1 && r.setAttribute('data-v-owner', n.uid), (r = r.nextSibling))
    n.ut()
  }
}
function Xl(e, t, n, r) {
  const o = (t.targetStart = n('')),
    i = (t.targetAnchor = n(''))
  return ((o[Vl] = i), e && (r(o, e), r(i, e)), i)
}
const mt = Symbol('_leaveCb'),
  wr = Symbol('_enterCb')
function ql() {
  const e = { isMounted: !1, isLeaving: !1, isUnmounting: !1, leavingVNodes: new Map() }
  return (
    pr(() => {
      e.isMounted = !0
    }),
    Yi(() => {
      e.isUnmounting = !0
    }),
    e
  )
}
const Be = [Function, Array],
  Yl = {
    mode: String,
    appear: Boolean,
    persisted: Boolean,
    onBeforeEnter: Be,
    onEnter: Be,
    onAfterEnter: Be,
    onEnterCancelled: Be,
    onBeforeLeave: Be,
    onLeave: Be,
    onAfterLeave: Be,
    onLeaveCancelled: Be,
    onBeforeAppear: Be,
    onAppear: Be,
    onAfterAppear: Be,
    onAppearCancelled: Be,
  },
  Jl = (e) => {
    const t = e.subTree
    return t.component ? Jl(t.component) : t
  },
  bd = {
    name: 'BaseTransition',
    props: Yl,
    setup(e, { slots: t }) {
      const n = Lt(),
        r = ql()
      return () => {
        const o = t.default && Xi(t.default(), !0)
        if (!o || !o.length) return
        const i = Ql(o),
          s = J(e),
          { mode: a } = s
        if (r.isLeaving) return Fo(i)
        const l = Ls(i)
        if (!l) return Fo(i)
        let u = ir(l, s, r, n, (f) => (u = f))
        l.type !== he && Qt(l, u)
        let c = n.subTree && Ls(n.subTree)
        if (c && c.type !== he && !zt(c, l) && Jl(n).type !== he) {
          let f = ir(c, s, r, n)
          if ((Qt(c, f), a === 'out-in' && l.type !== he))
            return (
              (r.isLeaving = !0),
              (f.afterLeave = () => {
                ;((r.isLeaving = !1),
                  n.job.flags & 8 || n.update(),
                  delete f.afterLeave,
                  (c = void 0))
              }),
              Fo(i)
            )
          a === 'in-out' && l.type !== he
            ? (f.delayLeave = (d, p, m) => {
                const v = Zl(r, c)
                ;((v[String(c.key)] = c),
                  (d[mt] = () => {
                    ;(p(), (d[mt] = void 0), delete u.delayedLeave, (c = void 0))
                  }),
                  (u.delayedLeave = () => {
                    ;(m(), delete u.delayedLeave, (c = void 0))
                  }))
              })
            : (c = void 0)
        } else c && (c = void 0)
        return i
      }
    },
  }
function Ql(e) {
  let t = e[0]
  if (e.length > 1) {
    for (const n of e)
      if (n.type !== he) {
        t = n
        break
      }
  }
  return t
}
const Cd = bd
function Zl(e, t) {
  const { leavingVNodes: n } = e
  let r = n.get(t.type)
  return (r || ((r = Object.create(null)), n.set(t.type, r)), r)
}
function ir(e, t, n, r, o) {
  const {
      appear: i,
      mode: s,
      persisted: a = !1,
      onBeforeEnter: l,
      onEnter: u,
      onAfterEnter: c,
      onEnterCancelled: f,
      onBeforeLeave: d,
      onLeave: p,
      onAfterLeave: m,
      onLeaveCancelled: v,
      onBeforeAppear: b,
      onAppear: C,
      onAfterAppear: O,
      onAppearCancelled: P,
    } = t,
    x = String(e.key),
    _ = Zl(n, e),
    H = ($, W) => {
      $ && Je($, r, 9, W)
    },
    y = ($, W) => {
      const Y = W[1]
      ;(H($, W), K($) ? $.every((k) => k.length <= 1) && Y() : $.length <= 1 && Y())
    },
    E = {
      mode: s,
      persisted: a,
      beforeEnter($) {
        let W = l
        if (!n.isMounted)
          if (i) W = b || l
          else return
        $[mt] && $[mt](!0)
        const Y = _[x]
        ;(Y && zt(e, Y) && Y.el[mt] && Y.el[mt](), H(W, [$]))
      },
      enter($) {
        let W = u,
          Y = c,
          k = f
        if (!n.isMounted)
          if (i) ((W = C || u), (Y = O || c), (k = P || f))
          else return
        let ee = !1
        const ae = ($[wr] = (M) => {
          ee ||
            ((ee = !0),
            M ? H(k, [$]) : H(Y, [$]),
            E.delayedLeave && E.delayedLeave(),
            ($[wr] = void 0))
        })
        W ? y(W, [$, ae]) : ae()
      },
      leave($, W) {
        const Y = String(e.key)
        if (($[wr] && $[wr](!0), n.isUnmounting)) return W()
        H(d, [$])
        let k = !1
        const ee = ($[mt] = (ae) => {
          k ||
            ((k = !0), W(), ae ? H(v, [$]) : H(m, [$]), ($[mt] = void 0), _[Y] === e && delete _[Y])
        })
        ;((_[Y] = e), p ? y(p, [$, ee]) : ee())
      },
      clone($) {
        const W = ir($, t, n, r, o)
        return (o && o(W), W)
      },
    }
  return E
}
function Fo(e) {
  if (ho(e)) return ((e = Rt(e)), (e.children = null), e)
}
function Ls(e) {
  if (!ho(e)) return Ul(e.type) && e.children ? Ql(e.children) : e
  if (e.component) return e.component.subTree
  const { shapeFlag: t, children: n } = e
  if (n) {
    if (t & 16) return n[0]
    if (t & 32 && X(n.default)) return n.default()
  }
}
function Qt(e, t) {
  e.shapeFlag & 6 && e.component
    ? ((e.transition = t), Qt(e.component.subTree, t))
    : e.shapeFlag & 128
      ? ((e.ssContent.transition = t.clone(e.ssContent)),
        (e.ssFallback.transition = t.clone(e.ssFallback)))
      : (e.transition = t)
}
function Xi(e, t = !1, n) {
  let r = [],
    o = 0
  for (let i = 0; i < e.length; i++) {
    let s = e[i]
    const a = n == null ? s.key : String(n) + String(s.key != null ? s.key : i)
    s.type === ue
      ? (s.patchFlag & 128 && o++, (r = r.concat(Xi(s.children, t, a))))
      : (t || s.type !== he) && r.push(a != null ? Rt(s, { key: a }) : s)
  }
  if (o > 1) for (let i = 0; i < r.length; i++) r[i].patchFlag = -2
  return r
}
function be(e, t) {
  return X(e) ? de({ name: e.name }, t, { setup: e }) : e
}
function ec(e) {
  e.ids = [e.ids[0] + e.ids[2]++ + '-', 0, 0]
}
function Yv(e) {
  const t = Lt(),
    n = We(null)
  if (t) {
    const o = t.refs === re ? (t.refs = {}) : t.refs
    Object.defineProperty(o, e, { enumerable: !0, get: () => n.value, set: (i) => (n.value = i) })
  }
  return n
}
const Xr = new WeakMap()
function qn(e, t, n, r, o = !1) {
  if (K(e)) {
    e.forEach((m, v) => qn(m, t && (K(t) ? t[v] : t), n, r, o))
    return
  }
  if (gn(r) && !o) {
    r.shapeFlag & 512 &&
      r.type.__asyncResolved &&
      r.component.subTree.component &&
      qn(e, t, n, r.component.subTree)
    return
  }
  const i = r.shapeFlag & 4 ? yo(r.component) : r.el,
    s = o ? null : i,
    { i: a, r: l } = e,
    u = t && t.r,
    c = a.refs === re ? (a.refs = {}) : a.refs,
    f = a.setupState,
    d = J(f),
    p = f === re ? ul : (m) => te(d, m)
  if (u != null && u !== l) {
    if ((Hs(t), ce(u))) ((c[u] = null), p(u) && (f[u] = null))
    else if (le(u)) {
      u.value = null
      const m = t
      m.k && (c[m.k] = null)
    }
  }
  if (X(l)) dr(l, a, 12, [s, c])
  else {
    const m = ce(l),
      v = le(l)
    if (m || v) {
      const b = () => {
        if (e.f) {
          const C = m ? (p(l) ? f[l] : c[l]) : l.value
          if (o) K(C) && Hi(C, i)
          else if (K(C)) C.includes(i) || C.push(i)
          else if (m) ((c[l] = [i]), p(l) && (f[l] = c[l]))
          else {
            const O = [i]
            ;((l.value = O), e.k && (c[e.k] = O))
          }
        } else m ? ((c[l] = s), p(l) && (f[l] = s)) : v && ((l.value = s), e.k && (c[e.k] = s))
      }
      if (s) {
        const C = () => {
          ;(b(), Xr.delete(e))
        }
        ;((C.id = -1), Xr.set(e, C), Oe(C, n))
      } else (Hs(e), b())
    }
  }
}
function Hs(e) {
  const t = Xr.get(e)
  t && ((t.flags |= 8), Xr.delete(e))
}
lo().requestIdleCallback
lo().cancelIdleCallback
const gn = (e) => !!e.type.__asyncLoader,
  ho = (e) => e.type.__isKeepAlive
function xd(e, t) {
  tc(e, 'a', t)
}
function Sd(e, t) {
  tc(e, 'da', t)
}
function tc(e, t, n = _e) {
  const r =
    e.__wdc ||
    (e.__wdc = () => {
      let o = n
      for (; o; ) {
        if (o.isDeactivated) return
        o = o.parent
      }
      return e()
    })
  if ((go(t, r, n), n)) {
    let o = n.parent
    for (; o && o.parent; ) (ho(o.parent.vnode) && _d(r, t, n, o), (o = o.parent))
  }
}
function _d(e, t, n, r) {
  const o = go(t, e, r, !0)
  Ji(() => {
    Hi(r[t], o)
  }, n)
}
function go(e, t, n = _e, r = !1) {
  if (n) {
    const o = n[e] || (n[e] = []),
      i =
        t.__weh ||
        (t.__weh = (...s) => {
          xt()
          const a = gr(n),
            l = Je(t, n, e, s)
          return (a(), St(), l)
        })
    return (r ? o.unshift(i) : o.push(i), i)
  }
}
const wt =
    (e) =>
    (t, n = _e) => {
      ;(!sr || e === 'sp') && go(e, (...r) => t(...r), n)
    },
  nc = wt('bm'),
  pr = wt('m'),
  wd = wt('bu'),
  qi = wt('u'),
  Yi = wt('bum'),
  Ji = wt('um'),
  Od = wt('sp'),
  Td = wt('rtg'),
  $d = wt('rtc')
function Pd(e, t = _e) {
  go('ec', e, t)
}
const Qi = 'components',
  Ed = 'directives'
function Jv(e, t) {
  return Zi(Qi, e, !0, t) || e
}
const rc = Symbol.for('v-ndc')
function Qv(e) {
  return ce(e) ? Zi(Qi, e, !1) || e : e || rc
}
function Zv(e) {
  return Zi(Ed, e)
}
function Zi(e, t, n = !0, r = !1) {
  const o = ge || _e
  if (o) {
    const i = o.type
    if (e === Qi) {
      const a = vp(i, !1)
      if (a && (a === t || a === Ve(t) || a === ao(Ve(t)))) return i
    }
    const s = Fs(o[e] || i[e], t) || Fs(o.appContext[e], t)
    return !s && r ? i : s
  }
}
function Fs(e, t) {
  return e && (e[t] || e[Ve(t)] || e[ao(Ve(t))])
}
function ey(e, t, n, r) {
  let o
  const i = n && n[r],
    s = K(e)
  if (s || ce(e)) {
    const a = s && Ct(e)
    let l = !1,
      u = !1
    ;(a && ((l = !ze(e)), (u = jt(e)), (e = uo(e))), (o = new Array(e.length)))
    for (let c = 0, f = e.length; c < f; c++)
      o[c] = t(l ? (u ? Vr(pe(e[c])) : pe(e[c])) : e[c], c, void 0, i && i[c])
  } else if (typeof e == 'number') {
    o = new Array(e)
    for (let a = 0; a < e; a++) o[a] = t(a + 1, a, void 0, i && i[a])
  } else if (oe(e))
    if (e[Symbol.iterator]) o = Array.from(e, (a, l) => t(a, l, void 0, i && i[l]))
    else {
      const a = Object.keys(e)
      o = new Array(a.length)
      for (let l = 0, u = a.length; l < u; l++) {
        const c = a[l]
        o[l] = t(e[c], c, l, i && i[l])
      }
    }
  else o = []
  return (n && (n[r] = o), o)
}
function ty(e, t, n = {}, r, o) {
  if (ge.ce || (ge.parent && gn(ge.parent) && ge.parent.ce)) {
    const u = Object.keys(n).length > 0
    return (
      t !== 'default' && (n.name = t),
      fi(),
      di(ue, null, [w('slot', n, r && r())], u ? -2 : 64)
    )
  }
  let i = e[t]
  ;(i && i._c && (i._d = !1), fi())
  const s = i && oc(i(n)),
    a = n.key || (s && s.key),
    l = di(
      ue,
      { key: (a && !_t(a) ? a : `_${t}`) + (!s && r ? '_fb' : '') },
      s || (r ? r() : []),
      s && e._ === 1 ? 64 : -2
    )
  return (l.scopeId && (l.slotScopeIds = [l.scopeId + '-s']), i && i._c && (i._d = !0), l)
}
function oc(e) {
  return e.some((t) => (ut(t) ? !(t.type === he || (t.type === ue && !oc(t.children))) : !0))
    ? e
    : null
}
const ai = (e) => (e ? (wc(e) ? yo(e) : ai(e.parent)) : null),
  Yn = de(Object.create(null), {
    $: (e) => e,
    $el: (e) => e.vnode.el,
    $data: (e) => e.data,
    $props: (e) => e.props,
    $attrs: (e) => e.attrs,
    $slots: (e) => e.slots,
    $refs: (e) => e.refs,
    $parent: (e) => ai(e.parent),
    $root: (e) => ai(e.root),
    $host: (e) => e.ce,
    $emit: (e) => e.emit,
    $options: (e) => ac(e),
    $forceUpdate: (e) =>
      e.f ||
      (e.f = () => {
        Ki(e.update)
      }),
    $nextTick: (e) => e.n || (e.n = po.bind(e.proxy)),
    $watch: (e) => Jd.bind(e),
  }),
  ko = (e, t) => e !== re && !e.__isScriptSetup && te(e, t),
  Ad = {
    get({ _: e }, t) {
      if (t === '__v_skip') return !0
      const { ctx: n, setupState: r, data: o, props: i, accessCache: s, type: a, appContext: l } = e
      let u
      if (t[0] !== '$') {
        const p = s[t]
        if (p !== void 0)
          switch (p) {
            case 1:
              return r[t]
            case 2:
              return o[t]
            case 4:
              return n[t]
            case 3:
              return i[t]
          }
        else {
          if (ko(r, t)) return ((s[t] = 1), r[t])
          if (o !== re && te(o, t)) return ((s[t] = 2), o[t])
          if ((u = e.propsOptions[0]) && te(u, t)) return ((s[t] = 3), i[t])
          if (n !== re && te(n, t)) return ((s[t] = 4), n[t])
          li && (s[t] = 0)
        }
      }
      const c = Yn[t]
      let f, d
      if (c) return (t === '$attrs' && Se(e.attrs, 'get', ''), c(e))
      if ((f = a.__cssModules) && (f = f[t])) return f
      if (n !== re && te(n, t)) return ((s[t] = 4), n[t])
      if (((d = l.config.globalProperties), te(d, t))) return d[t]
    },
    set({ _: e }, t, n) {
      const { data: r, setupState: o, ctx: i } = e
      return ko(o, t)
        ? ((o[t] = n), !0)
        : r !== re && te(r, t)
          ? ((r[t] = n), !0)
          : te(e.props, t) || (t[0] === '$' && t.slice(1) in e)
            ? !1
            : ((i[t] = n), !0)
    },
    has(
      {
        _: {
          data: e,
          setupState: t,
          accessCache: n,
          ctx: r,
          appContext: o,
          propsOptions: i,
          type: s,
        },
      },
      a
    ) {
      let l, u
      return !!(
        n[a] ||
        (e !== re && a[0] !== '$' && te(e, a)) ||
        ko(t, a) ||
        ((l = i[0]) && te(l, a)) ||
        te(r, a) ||
        te(Yn, a) ||
        te(o.config.globalProperties, a) ||
        ((u = s.__cssModules) && u[a])
      )
    },
    defineProperty(e, t, n) {
      return (
        n.get != null ? (e._.accessCache[t] = 0) : te(n, 'value') && this.set(e, t, n.value, null),
        Reflect.defineProperty(e, t, n)
      )
    },
  }
function ny() {
  return ic().slots
}
function ry() {
  return ic().attrs
}
function ic(e) {
  const t = Lt()
  return t.setupContext || (t.setupContext = Tc(t))
}
function ks(e) {
  return K(e) ? e.reduce((t, n) => ((t[n] = null), t), {}) : e
}
function oy(e, t) {
  const n = {}
  for (const r in e)
    t.includes(r) || Object.defineProperty(n, r, { enumerable: !0, get: () => e[r] })
  return n
}
let li = !0
function Md(e) {
  const t = ac(e),
    n = e.proxy,
    r = e.ctx
  ;((li = !1), t.beforeCreate && Ns(t.beforeCreate, e, 'bc'))
  const {
    data: o,
    computed: i,
    methods: s,
    watch: a,
    provide: l,
    inject: u,
    created: c,
    beforeMount: f,
    mounted: d,
    beforeUpdate: p,
    updated: m,
    activated: v,
    deactivated: b,
    beforeDestroy: C,
    beforeUnmount: O,
    destroyed: P,
    unmounted: x,
    render: _,
    renderTracked: H,
    renderTriggered: y,
    errorCaptured: E,
    serverPrefetch: $,
    expose: W,
    inheritAttrs: Y,
    components: k,
    directives: ee,
    filters: ae,
  } = t
  if ((u && Id(u, r, null), s))
    for (const V in s) {
      const Q = s[V]
      X(Q) && (r[V] = Q.bind(n))
    }
  if (o) {
    const V = o.call(n, n)
    oe(V) && (e.data = ct(V))
  }
  if (((li = !0), i))
    for (const V in i) {
      const Q = i[V],
        Ge = X(Q) ? Q.bind(n, n) : X(Q.get) ? Q.get.bind(n, n) : lt,
        yr = !X(Q) && X(Q.set) ? Q.set.bind(n) : lt,
        Ft = L({ get: Ge, set: yr })
      Object.defineProperty(r, V, {
        enumerable: !0,
        configurable: !0,
        get: () => Ft.value,
        set: (Qe) => (Ft.value = Qe),
      })
    }
  if (a) for (const V in a) sc(a[V], r, n, V)
  if (l) {
    const V = X(l) ? l.call(n) : l
    Reflect.ownKeys(V).forEach((Q) => {
      Ot(Q, V[Q])
    })
  }
  c && Ns(c, e, 'c')
  function B(V, Q) {
    K(Q) ? Q.forEach((Ge) => V(Ge.bind(n))) : Q && V(Q.bind(n))
  }
  if (
    (B(nc, f),
    B(pr, d),
    B(wd, p),
    B(qi, m),
    B(xd, v),
    B(Sd, b),
    B(Pd, E),
    B($d, H),
    B(Td, y),
    B(Yi, O),
    B(Ji, x),
    B(Od, $),
    K(W))
  )
    if (W.length) {
      const V = e.exposed || (e.exposed = {})
      W.forEach((Q) => {
        Object.defineProperty(V, Q, { get: () => n[Q], set: (Ge) => (n[Q] = Ge), enumerable: !0 })
      })
    } else e.exposed || (e.exposed = {})
  ;(_ && e.render === lt && (e.render = _),
    Y != null && (e.inheritAttrs = Y),
    k && (e.components = k),
    ee && (e.directives = ee),
    $ && ec(e))
}
function Id(e, t, n = lt) {
  K(e) && (e = ci(e))
  for (const r in e) {
    const o = e[r]
    let i
    ;(oe(o)
      ? 'default' in o
        ? (i = Ee(o.from || r, o.default, !0))
        : (i = Ee(o.from || r))
      : (i = Ee(o)),
      le(i)
        ? Object.defineProperty(t, r, {
            enumerable: !0,
            configurable: !0,
            get: () => i.value,
            set: (s) => (i.value = s),
          })
        : (t[r] = i))
  }
}
function Ns(e, t, n) {
  Je(K(e) ? e.map((r) => r.bind(t.proxy)) : e.bind(t.proxy), t, n)
}
function sc(e, t, n, r) {
  let o = r.includes('.') ? yc(n, r) : () => n[r]
  if (ce(e)) {
    const i = t[e]
    X(i) && Fe(o, i)
  } else if (X(e)) Fe(o, e.bind(n))
  else if (oe(e))
    if (K(e)) e.forEach((i) => sc(i, t, n, r))
    else {
      const i = X(e.handler) ? e.handler.bind(n) : t[e.handler]
      X(i) && Fe(o, i, e)
    }
}
function ac(e) {
  const t = e.type,
    { mixins: n, extends: r } = t,
    {
      mixins: o,
      optionsCache: i,
      config: { optionMergeStrategies: s },
    } = e.appContext,
    a = i.get(t)
  let l
  return (
    a
      ? (l = a)
      : !o.length && !n && !r
        ? (l = t)
        : ((l = {}), o.length && o.forEach((u) => qr(l, u, s, !0)), qr(l, t, s)),
    oe(t) && i.set(t, l),
    l
  )
}
function qr(e, t, n, r = !1) {
  const { mixins: o, extends: i } = t
  ;(i && qr(e, i, n, !0), o && o.forEach((s) => qr(e, s, n, !0)))
  for (const s in t)
    if (!(r && s === 'expose')) {
      const a = jd[s] || (n && n[s])
      e[s] = a ? a(e[s], t[s]) : t[s]
    }
  return e
}
const jd = {
  data: Ds,
  props: Bs,
  emits: Bs,
  methods: Wn,
  computed: Wn,
  beforeCreate: we,
  created: we,
  beforeMount: we,
  mounted: we,
  beforeUpdate: we,
  updated: we,
  beforeDestroy: we,
  beforeUnmount: we,
  destroyed: we,
  unmounted: we,
  activated: we,
  deactivated: we,
  errorCaptured: we,
  serverPrefetch: we,
  components: Wn,
  directives: Wn,
  watch: Ld,
  provide: Ds,
  inject: Rd,
}
function Ds(e, t) {
  return t
    ? e
      ? function () {
          return de(X(e) ? e.call(this, this) : e, X(t) ? t.call(this, this) : t)
        }
      : t
    : e
}
function Rd(e, t) {
  return Wn(ci(e), ci(t))
}
function ci(e) {
  if (K(e)) {
    const t = {}
    for (let n = 0; n < e.length; n++) t[e[n]] = e[n]
    return t
  }
  return e
}
function we(e, t) {
  return e ? [...new Set([].concat(e, t))] : t
}
function Wn(e, t) {
  return e ? de(Object.create(null), e, t) : t
}
function Bs(e, t) {
  return e
    ? K(e) && K(t)
      ? [...new Set([...e, ...t])]
      : de(Object.create(null), ks(e), ks(t ?? {}))
    : t
}
function Ld(e, t) {
  if (!e) return t
  if (!t) return e
  const n = de(Object.create(null), e)
  for (const r in t) n[r] = we(e[r], t[r])
  return n
}
function lc() {
  return {
    app: null,
    config: {
      isNativeTag: ul,
      performance: !1,
      globalProperties: {},
      optionMergeStrategies: {},
      errorHandler: void 0,
      warnHandler: void 0,
      compilerOptions: {},
    },
    mixins: [],
    components: {},
    directives: {},
    provides: Object.create(null),
    optionsCache: new WeakMap(),
    propsCache: new WeakMap(),
    emitsCache: new WeakMap(),
  }
}
let Hd = 0
function Fd(e, t) {
  return function (r, o = null) {
    ;(X(r) || (r = de({}, r)), o != null && !oe(o) && (o = null))
    const i = lc(),
      s = new WeakSet(),
      a = []
    let l = !1
    const u = (i.app = {
      _uid: Hd++,
      _component: r,
      _props: o,
      _container: null,
      _context: i,
      _instance: null,
      version: bp,
      get config() {
        return i.config
      },
      set config(c) {},
      use(c, ...f) {
        return (
          s.has(c) ||
            (c && X(c.install) ? (s.add(c), c.install(u, ...f)) : X(c) && (s.add(c), c(u, ...f))),
          u
        )
      },
      mixin(c) {
        return (i.mixins.includes(c) || i.mixins.push(c), u)
      },
      component(c, f) {
        return f ? ((i.components[c] = f), u) : i.components[c]
      },
      directive(c, f) {
        return f ? ((i.directives[c] = f), u) : i.directives[c]
      },
      mount(c, f, d) {
        if (!l) {
          const p = u._ceVNode || w(r, o)
          return (
            (p.appContext = i),
            d === !0 ? (d = 'svg') : d === !1 && (d = void 0),
            e(p, c, d),
            (l = !0),
            (u._container = c),
            (c.__vue_app__ = u),
            yo(p.component)
          )
        }
      },
      onUnmount(c) {
        a.push(c)
      },
      unmount() {
        l && (Je(a, u._instance, 16), e(null, u._container), delete u._container.__vue_app__)
      },
      provide(c, f) {
        return ((i.provides[c] = f), u)
      },
      runWithContext(c) {
        const f = Kt
        Kt = u
        try {
          return c()
        } finally {
          Kt = f
        }
      },
    })
    return u
  }
}
let Kt = null
function Ot(e, t) {
  if (_e) {
    let n = _e.provides
    const r = _e.parent && _e.parent.provides
    ;(r === n && (n = _e.provides = Object.create(r)), (n[e] = t))
  }
}
function Ee(e, t, n = !1) {
  const r = Lt()
  if (r || Kt) {
    let o = Kt
      ? Kt._context.provides
      : r
        ? r.parent == null || r.ce
          ? r.vnode.appContext && r.vnode.appContext.provides
          : r.parent.provides
        : void 0
    if (o && e in o) return o[e]
    if (arguments.length > 1) return n && X(t) ? t.call(r && r.proxy) : t
  }
}
function kd() {
  return !!(Lt() || Kt)
}
const cc = {},
  uc = () => Object.create(cc),
  fc = (e) => Object.getPrototypeOf(e) === cc
function Nd(e, t, n, r = !1) {
  const o = {},
    i = uc()
  ;((e.propsDefaults = Object.create(null)), dc(e, t, o, i))
  for (const s in e.propsOptions[0]) s in o || (o[s] = void 0)
  ;(n ? (e.props = r ? o : td(o)) : e.type.props ? (e.props = o) : (e.props = i), (e.attrs = i))
}
function Dd(e, t, n, r) {
  const {
      props: o,
      attrs: i,
      vnode: { patchFlag: s },
    } = e,
    a = J(o),
    [l] = e.propsOptions
  let u = !1
  if ((r || s > 0) && !(s & 16)) {
    if (s & 8) {
      const c = e.vnode.dynamicProps
      for (let f = 0; f < c.length; f++) {
        let d = c[f]
        if (vo(e.emitsOptions, d)) continue
        const p = t[d]
        if (l)
          if (te(i, d)) p !== i[d] && ((i[d] = p), (u = !0))
          else {
            const m = Ve(d)
            o[m] = ui(l, a, m, p, e, !1)
          }
        else p !== i[d] && ((i[d] = p), (u = !0))
      }
    }
  } else {
    dc(e, t, o, i) && (u = !0)
    let c
    for (const f in a)
      (!t || (!te(t, f) && ((c = nn(f)) === f || !te(t, c)))) &&
        (l
          ? n && (n[f] !== void 0 || n[c] !== void 0) && (o[f] = ui(l, a, f, void 0, e, !0))
          : delete o[f])
    if (i !== a) for (const f in i) (!t || !te(t, f)) && (delete i[f], (u = !0))
  }
  u && vt(e.attrs, 'set', '')
}
function dc(e, t, n, r) {
  const [o, i] = e.propsOptions
  let s = !1,
    a
  if (t)
    for (let l in t) {
      if (Un(l)) continue
      const u = t[l]
      let c
      o && te(o, (c = Ve(l)))
        ? !i || !i.includes(c)
          ? (n[c] = u)
          : ((a || (a = {}))[c] = u)
        : vo(e.emitsOptions, l) || ((!(l in r) || u !== r[l]) && ((r[l] = u), (s = !0)))
    }
  if (i) {
    const l = J(n),
      u = a || re
    for (let c = 0; c < i.length; c++) {
      const f = i[c]
      n[f] = ui(o, l, f, u[f], e, !te(u, f))
    }
  }
  return s
}
function ui(e, t, n, r, o, i) {
  const s = e[n]
  if (s != null) {
    const a = te(s, 'default')
    if (a && r === void 0) {
      const l = s.default
      if (s.type !== Function && !s.skipFactory && X(l)) {
        const { propsDefaults: u } = o
        if (n in u) r = u[n]
        else {
          const c = gr(o)
          ;((r = u[n] = l.call(null, t)), c())
        }
      } else r = l
      o.ce && o.ce._setProp(n, r)
    }
    s[0] && (i && !a ? (r = !1) : s[1] && (r === '' || r === nn(n)) && (r = !0))
  }
  return r
}
const Bd = new WeakMap()
function pc(e, t, n = !1) {
  const r = n ? Bd : t.propsCache,
    o = r.get(e)
  if (o) return o
  const i = e.props,
    s = {},
    a = []
  let l = !1
  if (!X(e)) {
    const c = (f) => {
      l = !0
      const [d, p] = pc(f, t, !0)
      ;(de(s, d), p && a.push(...p))
    }
    ;(!n && t.mixins.length && t.mixins.forEach(c),
      e.extends && c(e.extends),
      e.mixins && e.mixins.forEach(c))
  }
  if (!i && !l) return (oe(e) && r.set(e, dn), dn)
  if (K(i))
    for (let c = 0; c < i.length; c++) {
      const f = Ve(i[c])
      zs(f) && (s[f] = re)
    }
  else if (i)
    for (const c in i) {
      const f = Ve(c)
      if (zs(f)) {
        const d = i[c],
          p = (s[f] = K(d) || X(d) ? { type: d } : de({}, d)),
          m = p.type
        let v = !1,
          b = !0
        if (K(m))
          for (let C = 0; C < m.length; ++C) {
            const O = m[C],
              P = X(O) && O.name
            if (P === 'Boolean') {
              v = !0
              break
            } else P === 'String' && (b = !1)
          }
        else v = X(m) && m.name === 'Boolean'
        ;((p[0] = v), (p[1] = b), (v || te(p, 'default')) && a.push(f))
      }
    }
  const u = [s, a]
  return (oe(e) && r.set(e, u), u)
}
function zs(e) {
  return e[0] !== '$' && !Un(e)
}
const es = (e) => e === '_' || e === '_ctx' || e === '$stable',
  ts = (e) => (K(e) ? e.map(at) : [at(e)]),
  zd = (e, t, n) => {
    if (t._n) return t
    const r = vd((...o) => ts(t(...o)), n)
    return ((r._c = !1), r)
  },
  hc = (e, t, n) => {
    const r = e._ctx
    for (const o in e) {
      if (es(o)) continue
      const i = e[o]
      if (X(i)) t[o] = zd(o, i, r)
      else if (i != null) {
        const s = ts(i)
        t[o] = () => s
      }
    }
  },
  gc = (e, t) => {
    const n = ts(t)
    e.slots.default = () => n
  },
  mc = (e, t, n) => {
    for (const r in t) (n || !es(r)) && (e[r] = t[r])
  },
  Wd = (e, t, n) => {
    const r = (e.slots = uc())
    if (e.vnode.shapeFlag & 32) {
      const o = t._
      o ? (mc(r, t, n), n && gl(r, '_', o, !0)) : hc(t, r)
    } else t && gc(e, t)
  },
  Vd = (e, t, n) => {
    const { vnode: r, slots: o } = e
    let i = !0,
      s = re
    if (r.shapeFlag & 32) {
      const a = t._
      ;(a ? (n && a === 1 ? (i = !1) : mc(o, t, n)) : ((i = !t.$stable), hc(t, o)), (s = t))
    } else t && (gc(e, t), (s = { default: 1 }))
    if (i) for (const a in o) !es(a) && s[a] == null && delete o[a]
  },
  Oe = ip
function Ud(e) {
  return Gd(e)
}
function Gd(e, t) {
  const n = lo()
  n.__VUE__ = !0
  const {
      insert: r,
      remove: o,
      patchProp: i,
      createElement: s,
      createText: a,
      createComment: l,
      setText: u,
      setElementText: c,
      parentNode: f,
      nextSibling: d,
      setScopeId: p = lt,
      insertStaticContent: m,
    } = e,
    v = (h, g, S, j = null, A = null, I = null, D = void 0, N = null, F = !!g.dynamicChildren) => {
      if (h === g) return
      ;(h && !zt(h, g) && ((j = br(h)), Qe(h, A, I, !0), (h = null)),
        g.patchFlag === -2 && ((F = !1), (g.dynamicChildren = null)))
      const { type: R, ref: G, shapeFlag: z } = g
      switch (R) {
        case hr:
          b(h, g, S, j)
          break
        case he:
          C(h, g, S, j)
          break
        case Ir:
          h == null && O(g, S, j, D)
          break
        case ue:
          k(h, g, S, j, A, I, D, N, F)
          break
        default:
          z & 1
            ? _(h, g, S, j, A, I, D, N, F)
            : z & 6
              ? ee(h, g, S, j, A, I, D, N, F)
              : (z & 64 || z & 128) && R.process(h, g, S, j, A, I, D, N, F, Hn)
      }
      G != null && A
        ? qn(G, h && h.ref, I, g || h, !g)
        : G == null && h && h.ref != null && qn(h.ref, null, I, h, !0)
    },
    b = (h, g, S, j) => {
      if (h == null) r((g.el = a(g.children)), S, j)
      else {
        const A = (g.el = h.el)
        g.children !== h.children && u(A, g.children)
      }
    },
    C = (h, g, S, j) => {
      h == null ? r((g.el = l(g.children || '')), S, j) : (g.el = h.el)
    },
    O = (h, g, S, j) => {
      ;[h.el, h.anchor] = m(h.children, g, S, j, h.el, h.anchor)
    },
    P = ({ el: h, anchor: g }, S, j) => {
      let A
      for (; h && h !== g; ) ((A = d(h)), r(h, S, j), (h = A))
      r(g, S, j)
    },
    x = ({ el: h, anchor: g }) => {
      let S
      for (; h && h !== g; ) ((S = d(h)), o(h), (h = S))
      o(g)
    },
    _ = (h, g, S, j, A, I, D, N, F) => {
      ;(g.type === 'svg' ? (D = 'svg') : g.type === 'math' && (D = 'mathml'),
        h == null ? H(g, S, j, A, I, D, N, F) : $(h, g, A, I, D, N, F))
    },
    H = (h, g, S, j, A, I, D, N) => {
      let F, R
      const { props: G, shapeFlag: z, transition: U, dirs: q } = h
      if (
        ((F = h.el = s(h.type, I, G && G.is, G)),
        z & 8 ? c(F, h.children) : z & 16 && E(h.children, F, null, j, A, No(h, I), D, N),
        q && kt(h, null, j, 'created'),
        y(F, h, h.scopeId, D, j),
        G)
      ) {
        for (const ie in G) ie !== 'value' && !Un(ie) && i(F, ie, null, G[ie], I, j)
        ;('value' in G && i(F, 'value', null, G.value, I),
          (R = G.onVnodeBeforeMount) && nt(R, j, h))
      }
      q && kt(h, null, j, 'beforeMount')
      const Z = Kd(A, U)
      ;(Z && U.beforeEnter(F),
        r(F, g, S),
        ((R = G && G.onVnodeMounted) || Z || q) &&
          Oe(() => {
            ;(R && nt(R, j, h), Z && U.enter(F), q && kt(h, null, j, 'mounted'))
          }, A))
    },
    y = (h, g, S, j, A) => {
      if ((S && p(h, S), j)) for (let I = 0; I < j.length; I++) p(h, j[I])
      if (A) {
        let I = A.subTree
        if (g === I || (Cc(I.type) && (I.ssContent === g || I.ssFallback === g))) {
          const D = A.vnode
          y(h, D, D.scopeId, D.slotScopeIds, A.parent)
        }
      }
    },
    E = (h, g, S, j, A, I, D, N, F = 0) => {
      for (let R = F; R < h.length; R++) {
        const G = (h[R] = N ? At(h[R]) : at(h[R]))
        v(null, G, g, S, j, A, I, D, N)
      }
    },
    $ = (h, g, S, j, A, I, D) => {
      const N = (g.el = h.el)
      let { patchFlag: F, dynamicChildren: R, dirs: G } = g
      F |= h.patchFlag & 16
      const z = h.props || re,
        U = g.props || re
      let q
      if (
        (S && Nt(S, !1),
        (q = U.onVnodeBeforeUpdate) && nt(q, S, g, h),
        G && kt(g, h, S, 'beforeUpdate'),
        S && Nt(S, !0),
        ((z.innerHTML && U.innerHTML == null) || (z.textContent && U.textContent == null)) &&
          c(N, ''),
        R
          ? W(h.dynamicChildren, R, N, S, j, No(g, A), I)
          : D || Q(h, g, N, null, S, j, No(g, A), I, !1),
        F > 0)
      ) {
        if (F & 16) Y(N, z, U, S, A)
        else if (
          (F & 2 && z.class !== U.class && i(N, 'class', null, U.class, A),
          F & 4 && i(N, 'style', z.style, U.style, A),
          F & 8)
        ) {
          const Z = g.dynamicProps
          for (let ie = 0; ie < Z.length; ie++) {
            const ne = Z[ie],
              Me = z[ne],
              Ie = U[ne]
            ;(Ie !== Me || ne === 'value') && i(N, ne, Me, Ie, A, S)
          }
        }
        F & 1 && h.children !== g.children && c(N, g.children)
      } else !D && R == null && Y(N, z, U, S, A)
      ;((q = U.onVnodeUpdated) || G) &&
        Oe(() => {
          ;(q && nt(q, S, g, h), G && kt(g, h, S, 'updated'))
        }, j)
    },
    W = (h, g, S, j, A, I, D) => {
      for (let N = 0; N < g.length; N++) {
        const F = h[N],
          R = g[N],
          G = F.el && (F.type === ue || !zt(F, R) || F.shapeFlag & 198) ? f(F.el) : S
        v(F, R, G, null, j, A, I, D, !0)
      }
    },
    Y = (h, g, S, j, A) => {
      if (g !== S) {
        if (g !== re) for (const I in g) !Un(I) && !(I in S) && i(h, I, g[I], null, A, j)
        for (const I in S) {
          if (Un(I)) continue
          const D = S[I],
            N = g[I]
          D !== N && I !== 'value' && i(h, I, N, D, A, j)
        }
        'value' in S && i(h, 'value', g.value, S.value, A)
      }
    },
    k = (h, g, S, j, A, I, D, N, F) => {
      const R = (g.el = h ? h.el : a('')),
        G = (g.anchor = h ? h.anchor : a(''))
      let { patchFlag: z, dynamicChildren: U, slotScopeIds: q } = g
      ;(q && (N = N ? N.concat(q) : q),
        h == null
          ? (r(R, S, j), r(G, S, j), E(g.children || [], S, G, A, I, D, N, F))
          : z > 0 && z & 64 && U && h.dynamicChildren
            ? (W(h.dynamicChildren, U, S, A, I, D, N),
              (g.key != null || (A && g === A.subTree)) && ns(h, g, !0))
            : Q(h, g, S, G, A, I, D, N, F))
    },
    ee = (h, g, S, j, A, I, D, N, F) => {
      ;((g.slotScopeIds = N),
        h == null
          ? g.shapeFlag & 512
            ? A.ctx.activate(g, S, j, D, F)
            : ae(g, S, j, A, I, D, F)
          : M(h, g, F))
    },
    ae = (h, g, S, j, A, I, D) => {
      const N = (h.component = pp(h, j, A))
      if ((ho(h) && (N.ctx.renderer = Hn), hp(N, !1, D), N.asyncDep)) {
        if ((A && A.registerDep(N, B, D), !h.el)) {
          const F = (N.subTree = w(he))
          ;(C(null, F, g, S), (h.placeholder = F.el))
        }
      } else B(N, h, g, S, A, I, D)
    },
    M = (h, g, S) => {
      const j = (g.component = h.component)
      if (rp(h, g, S))
        if (j.asyncDep && !j.asyncResolved) {
          V(j, g, S)
          return
        } else ((j.next = g), j.update())
      else ((g.el = h.el), (j.vnode = g))
    },
    B = (h, g, S, j, A, I, D) => {
      const N = () => {
        if (h.isMounted) {
          let { next: z, bu: U, u: q, parent: Z, vnode: ie } = h
          {
            const et = vc(h)
            if (et) {
              ;(z && ((z.el = ie.el), V(h, z, D)),
                et.asyncDep.then(() => {
                  h.isUnmounted || N()
                }))
              return
            }
          }
          let ne = z,
            Me
          ;(Nt(h, !1),
            z ? ((z.el = ie.el), V(h, z, D)) : (z = ie),
            U && Io(U),
            (Me = z.props && z.props.onVnodeBeforeUpdate) && nt(Me, Z, z, ie),
            Nt(h, !0))
          const Ie = Vs(h),
            Ze = h.subTree
          ;((h.subTree = Ie),
            v(Ze, Ie, f(Ze.el), br(Ze), h, A, I),
            (z.el = Ie.el),
            ne === null && op(h, Ie.el),
            q && Oe(q, A),
            (Me = z.props && z.props.onVnodeUpdated) && Oe(() => nt(Me, Z, z, ie), A))
        } else {
          let z
          const { el: U, props: q } = g,
            { bm: Z, m: ie, parent: ne, root: Me, type: Ie } = h,
            Ze = gn(g)
          ;(Nt(h, !1),
            Z && Io(Z),
            !Ze && (z = q && q.onVnodeBeforeMount) && nt(z, ne, g),
            Nt(h, !0))
          {
            Me.ce && Me.ce._def.shadowRoot !== !1 && Me.ce._injectChildStyle(Ie)
            const et = (h.subTree = Vs(h))
            ;(v(null, et, S, j, h, A, I), (g.el = et.el))
          }
          if ((ie && Oe(ie, A), !Ze && (z = q && q.onVnodeMounted))) {
            const et = g
            Oe(() => nt(z, ne, et), A)
          }
          ;((g.shapeFlag & 256 || (ne && gn(ne.vnode) && ne.vnode.shapeFlag & 256)) &&
            h.a &&
            Oe(h.a, A),
            (h.isMounted = !0),
            (g = S = j = null))
        }
      }
      h.scope.on()
      const F = (h.effect = new Sl(N))
      h.scope.off()
      const R = (h.update = F.run.bind(F)),
        G = (h.job = F.runIfDirty.bind(F))
      ;((G.i = h), (G.id = h.uid), (F.scheduler = () => Ki(G)), Nt(h, !0), R())
    },
    V = (h, g, S) => {
      g.component = h
      const j = h.vnode.props
      ;((h.vnode = g),
        (h.next = null),
        Dd(h, g.props, j, S),
        Vd(h, g.children, S),
        xt(),
        Ms(h),
        St())
    },
    Q = (h, g, S, j, A, I, D, N, F = !1) => {
      const R = h && h.children,
        G = h ? h.shapeFlag : 0,
        z = g.children,
        { patchFlag: U, shapeFlag: q } = g
      if (U > 0) {
        if (U & 128) {
          yr(R, z, S, j, A, I, D, N, F)
          return
        } else if (U & 256) {
          Ge(R, z, S, j, A, I, D, N, F)
          return
        }
      }
      q & 8
        ? (G & 16 && Ln(R, A, I), z !== R && c(S, z))
        : G & 16
          ? q & 16
            ? yr(R, z, S, j, A, I, D, N, F)
            : Ln(R, A, I, !0)
          : (G & 8 && c(S, ''), q & 16 && E(z, S, j, A, I, D, N, F))
    },
    Ge = (h, g, S, j, A, I, D, N, F) => {
      ;((h = h || dn), (g = g || dn))
      const R = h.length,
        G = g.length,
        z = Math.min(R, G)
      let U
      for (U = 0; U < z; U++) {
        const q = (g[U] = F ? At(g[U]) : at(g[U]))
        v(h[U], q, S, null, A, I, D, N, F)
      }
      R > G ? Ln(h, A, I, !0, !1, z) : E(g, S, j, A, I, D, N, F, z)
    },
    yr = (h, g, S, j, A, I, D, N, F) => {
      let R = 0
      const G = g.length
      let z = h.length - 1,
        U = G - 1
      for (; R <= z && R <= U; ) {
        const q = h[R],
          Z = (g[R] = F ? At(g[R]) : at(g[R]))
        if (zt(q, Z)) v(q, Z, S, null, A, I, D, N, F)
        else break
        R++
      }
      for (; R <= z && R <= U; ) {
        const q = h[z],
          Z = (g[U] = F ? At(g[U]) : at(g[U]))
        if (zt(q, Z)) v(q, Z, S, null, A, I, D, N, F)
        else break
        ;(z--, U--)
      }
      if (R > z) {
        if (R <= U) {
          const q = U + 1,
            Z = q < G ? g[q].el : j
          for (; R <= U; ) (v(null, (g[R] = F ? At(g[R]) : at(g[R])), S, Z, A, I, D, N, F), R++)
        }
      } else if (R > U) for (; R <= z; ) (Qe(h[R], A, I, !0), R++)
      else {
        const q = R,
          Z = R,
          ie = new Map()
        for (R = Z; R <= U; R++) {
          const je = (g[R] = F ? At(g[R]) : at(g[R]))
          je.key != null && ie.set(je.key, R)
        }
        let ne,
          Me = 0
        const Ie = U - Z + 1
        let Ze = !1,
          et = 0
        const Fn = new Array(Ie)
        for (R = 0; R < Ie; R++) Fn[R] = 0
        for (R = q; R <= z; R++) {
          const je = h[R]
          if (Me >= Ie) {
            Qe(je, A, I, !0)
            continue
          }
          let tt
          if (je.key != null) tt = ie.get(je.key)
          else
            for (ne = Z; ne <= U; ne++)
              if (Fn[ne - Z] === 0 && zt(je, g[ne])) {
                tt = ne
                break
              }
          tt === void 0
            ? Qe(je, A, I, !0)
            : ((Fn[tt - Z] = R + 1),
              tt >= et ? (et = tt) : (Ze = !0),
              v(je, g[tt], S, null, A, I, D, N, F),
              Me++)
        }
        const Os = Ze ? Xd(Fn) : dn
        for (ne = Os.length - 1, R = Ie - 1; R >= 0; R--) {
          const je = Z + R,
            tt = g[je],
            Ts = g[je + 1],
            $s = je + 1 < G ? Ts.el || Ts.placeholder : j
          Fn[R] === 0
            ? v(null, tt, S, $s, A, I, D, N, F)
            : Ze && (ne < 0 || R !== Os[ne] ? Ft(tt, S, $s, 2) : ne--)
        }
      }
    },
    Ft = (h, g, S, j, A = null) => {
      const { el: I, type: D, transition: N, children: F, shapeFlag: R } = h
      if (R & 6) {
        Ft(h.component.subTree, g, S, j)
        return
      }
      if (R & 128) {
        h.suspense.move(g, S, j)
        return
      }
      if (R & 64) {
        D.move(h, g, S, Hn)
        return
      }
      if (D === ue) {
        r(I, g, S)
        for (let z = 0; z < F.length; z++) Ft(F[z], g, S, j)
        r(h.anchor, g, S)
        return
      }
      if (D === Ir) {
        P(h, g, S)
        return
      }
      if (j !== 2 && R & 1 && N)
        if (j === 0) (N.beforeEnter(I), r(I, g, S), Oe(() => N.enter(I), A))
        else {
          const { leave: z, delayLeave: U, afterLeave: q } = N,
            Z = () => {
              h.ctx.isUnmounted ? o(I) : r(I, g, S)
            },
            ie = () => {
              ;(I._isLeaving && I[mt](!0),
                z(I, () => {
                  ;(Z(), q && q())
                }))
            }
          U ? U(I, Z, ie) : ie()
        }
      else r(I, g, S)
    },
    Qe = (h, g, S, j = !1, A = !1) => {
      const {
        type: I,
        props: D,
        ref: N,
        children: F,
        dynamicChildren: R,
        shapeFlag: G,
        patchFlag: z,
        dirs: U,
        cacheIndex: q,
      } = h
      if (
        (z === -2 && (A = !1),
        N != null && (xt(), qn(N, null, S, h, !0), St()),
        q != null && (g.renderCache[q] = void 0),
        G & 256)
      ) {
        g.ctx.deactivate(h)
        return
      }
      const Z = G & 1 && U,
        ie = !gn(h)
      let ne
      if ((ie && (ne = D && D.onVnodeBeforeUnmount) && nt(ne, g, h), G & 6)) xf(h.component, S, j)
      else {
        if (G & 128) {
          h.suspense.unmount(S, j)
          return
        }
        ;(Z && kt(h, null, g, 'beforeUnmount'),
          G & 64
            ? h.type.remove(h, g, S, Hn, j)
            : R && !R.hasOnce && (I !== ue || (z > 0 && z & 64))
              ? Ln(R, g, S, !1, !0)
              : ((I === ue && z & 384) || (!A && G & 16)) && Ln(F, g, S),
          j && _s(h))
      }
      ;((ie && (ne = D && D.onVnodeUnmounted)) || Z) &&
        Oe(() => {
          ;(ne && nt(ne, g, h), Z && kt(h, null, g, 'unmounted'))
        }, S)
    },
    _s = (h) => {
      const { type: g, el: S, anchor: j, transition: A } = h
      if (g === ue) {
        Cf(S, j)
        return
      }
      if (g === Ir) {
        x(h)
        return
      }
      const I = () => {
        ;(o(S), A && !A.persisted && A.afterLeave && A.afterLeave())
      }
      if (h.shapeFlag & 1 && A && !A.persisted) {
        const { leave: D, delayLeave: N } = A,
          F = () => D(S, I)
        N ? N(h.el, I, F) : F()
      } else I()
    },
    Cf = (h, g) => {
      let S
      for (; h !== g; ) ((S = d(h)), o(h), (h = S))
      o(g)
    },
    xf = (h, g, S) => {
      const { bum: j, scope: A, job: I, subTree: D, um: N, m: F, a: R } = h
      ;(Ws(F),
        Ws(R),
        j && Io(j),
        A.stop(),
        I && ((I.flags |= 8), Qe(D, h, g, S)),
        N && Oe(N, g),
        Oe(() => {
          h.isUnmounted = !0
        }, g))
    },
    Ln = (h, g, S, j = !1, A = !1, I = 0) => {
      for (let D = I; D < h.length; D++) Qe(h[D], g, S, j, A)
    },
    br = (h) => {
      if (h.shapeFlag & 6) return br(h.component.subTree)
      if (h.shapeFlag & 128) return h.suspense.next()
      const g = d(h.anchor || h.el),
        S = g && g[Vl]
      return S ? d(S) : g
    }
  let Ao = !1
  const ws = (h, g, S) => {
      ;(h == null
        ? g._vnode && Qe(g._vnode, null, null, !0)
        : v(g._vnode || null, h, g, null, null, null, S),
        (g._vnode = h),
        Ao || ((Ao = !0), Ms(), Bl(), (Ao = !1)))
    },
    Hn = { p: v, um: Qe, m: Ft, r: _s, mt: ae, mc: E, pc: Q, pbc: W, n: br, o: e }
  return { render: ws, hydrate: void 0, createApp: Fd(ws) }
}
function No({ type: e, props: t }, n) {
  return (n === 'svg' && e === 'foreignObject') ||
    (n === 'mathml' && e === 'annotation-xml' && t && t.encoding && t.encoding.includes('html'))
    ? void 0
    : n
}
function Nt({ effect: e, job: t }, n) {
  n ? ((e.flags |= 32), (t.flags |= 4)) : ((e.flags &= -33), (t.flags &= -5))
}
function Kd(e, t) {
  return (!e || (e && !e.pendingBranch)) && t && !t.persisted
}
function ns(e, t, n = !1) {
  const r = e.children,
    o = t.children
  if (K(r) && K(o))
    for (let i = 0; i < r.length; i++) {
      const s = r[i]
      let a = o[i]
      ;(a.shapeFlag & 1 &&
        !a.dynamicChildren &&
        ((a.patchFlag <= 0 || a.patchFlag === 32) && ((a = o[i] = At(o[i])), (a.el = s.el)),
        !n && a.patchFlag !== -2 && ns(s, a)),
        a.type === hr && a.patchFlag !== -1 && (a.el = s.el),
        a.type === he && !a.el && (a.el = s.el))
    }
}
function Xd(e) {
  const t = e.slice(),
    n = [0]
  let r, o, i, s, a
  const l = e.length
  for (r = 0; r < l; r++) {
    const u = e[r]
    if (u !== 0) {
      if (((o = n[n.length - 1]), e[o] < u)) {
        ;((t[r] = o), n.push(r))
        continue
      }
      for (i = 0, s = n.length - 1; i < s; )
        ((a = (i + s) >> 1), e[n[a]] < u ? (i = a + 1) : (s = a))
      u < e[n[i]] && (i > 0 && (t[r] = n[i - 1]), (n[i] = r))
    }
  }
  for (i = n.length, s = n[i - 1]; i-- > 0; ) ((n[i] = s), (s = t[s]))
  return n
}
function vc(e) {
  const t = e.subTree.component
  if (t) return t.asyncDep && !t.asyncResolved ? t : vc(t)
}
function Ws(e) {
  if (e) for (let t = 0; t < e.length; t++) e[t].flags |= 8
}
const qd = Symbol.for('v-scx'),
  Yd = () => Ee(qd)
function mo(e, t) {
  return rs(e, null, t)
}
function Fe(e, t, n) {
  return rs(e, t, n)
}
function rs(e, t, n = re) {
  const { immediate: r, deep: o, flush: i, once: s } = n,
    a = de({}, n),
    l = (t && r) || (!t && i !== 'post')
  let u
  if (sr) {
    if (i === 'sync') {
      const p = Yd()
      u = p.__watcherHandles || (p.__watcherHandles = [])
    } else if (!l) {
      const p = () => {}
      return ((p.stop = lt), (p.resume = lt), (p.pause = lt), p)
    }
  }
  const c = _e
  a.call = (p, m, v) => Je(p, c, m, v)
  let f = !1
  ;(i === 'post'
    ? (a.scheduler = (p) => {
        Oe(p, c && c.suspense)
      })
    : i !== 'sync' &&
      ((f = !0),
      (a.scheduler = (p, m) => {
        m ? p() : Ki(p)
      })),
    (a.augmentJob = (p) => {
      ;(t && (p.flags |= 4), f && ((p.flags |= 2), c && ((p.id = c.uid), (p.i = c))))
    }))
  const d = pd(e, t, a)
  return (sr && (u ? u.push(d) : l && d()), d)
}
function Jd(e, t, n) {
  const r = this.proxy,
    o = ce(e) ? (e.includes('.') ? yc(r, e) : () => r[e]) : e.bind(r, r)
  let i
  X(t) ? (i = t) : ((i = t.handler), (n = t))
  const s = gr(this),
    a = rs(o, i.bind(r), n)
  return (s(), a)
}
function yc(e, t) {
  const n = t.split('.')
  return () => {
    let r = e
    for (let o = 0; o < n.length && r; o++) r = r[n[o]]
    return r
  }
}
const Qd = (e, t) =>
  t === 'modelValue' || t === 'model-value'
    ? e.modelModifiers
    : e[`${t}Modifiers`] || e[`${Ve(t)}Modifiers`] || e[`${nn(t)}Modifiers`]
function Zd(e, t, ...n) {
  if (e.isUnmounted) return
  const r = e.vnode.props || re
  let o = n
  const i = t.startsWith('update:'),
    s = i && Qd(r, t.slice(7))
  s && (s.trim && (o = n.map((c) => (ce(c) ? c.trim() : c))), s.number && (o = n.map(Tf)))
  let a,
    l = r[(a = Mo(t))] || r[(a = Mo(Ve(t)))]
  ;(!l && i && (l = r[(a = Mo(nn(t)))]), l && Je(l, e, 6, o))
  const u = r[a + 'Once']
  if (u) {
    if (!e.emitted) e.emitted = {}
    else if (e.emitted[a]) return
    ;((e.emitted[a] = !0), Je(u, e, 6, o))
  }
}
const ep = new WeakMap()
function bc(e, t, n = !1) {
  const r = n ? ep : t.emitsCache,
    o = r.get(e)
  if (o !== void 0) return o
  const i = e.emits
  let s = {},
    a = !1
  if (!X(e)) {
    const l = (u) => {
      const c = bc(u, t, !0)
      c && ((a = !0), de(s, c))
    }
    ;(!n && t.mixins.length && t.mixins.forEach(l),
      e.extends && l(e.extends),
      e.mixins && e.mixins.forEach(l))
  }
  return !i && !a
    ? (oe(e) && r.set(e, null), null)
    : (K(i) ? i.forEach((l) => (s[l] = null)) : de(s, i), oe(e) && r.set(e, s), s)
}
function vo(e, t) {
  return !e || !oo(t)
    ? !1
    : ((t = t.slice(2).replace(/Once$/, '')),
      te(e, t[0].toLowerCase() + t.slice(1)) || te(e, nn(t)) || te(e, t))
}
function Vs(e) {
  const {
      type: t,
      vnode: n,
      proxy: r,
      withProxy: o,
      propsOptions: [i],
      slots: s,
      attrs: a,
      emit: l,
      render: u,
      renderCache: c,
      props: f,
      data: d,
      setupState: p,
      ctx: m,
      inheritAttrs: v,
    } = e,
    b = Kr(e)
  let C, O
  try {
    if (n.shapeFlag & 4) {
      const x = o || r,
        _ = x
      ;((C = at(u.call(_, x, c, f, p, d, m))), (O = a))
    } else {
      const x = t
      ;((C = at(x.length > 1 ? x(f, { attrs: a, slots: s, emit: l }) : x(f, null))),
        (O = t.props ? a : tp(a)))
    }
  } catch (x) {
    ;((Jn.length = 0), fo(x, e, 1), (C = w(he)))
  }
  let P = C
  if (O && v !== !1) {
    const x = Object.keys(O),
      { shapeFlag: _ } = P
    x.length && _ & 7 && (i && x.some(Li) && (O = np(O, i)), (P = Rt(P, O, !1, !0)))
  }
  return (
    n.dirs && ((P = Rt(P, null, !1, !0)), (P.dirs = P.dirs ? P.dirs.concat(n.dirs) : n.dirs)),
    n.transition && Qt(P, n.transition),
    (C = P),
    Kr(b),
    C
  )
}
const tp = (e) => {
    let t
    for (const n in e) (n === 'class' || n === 'style' || oo(n)) && ((t || (t = {}))[n] = e[n])
    return t
  },
  np = (e, t) => {
    const n = {}
    for (const r in e) (!Li(r) || !(r.slice(9) in t)) && (n[r] = e[r])
    return n
  }
function rp(e, t, n) {
  const { props: r, children: o, component: i } = e,
    { props: s, children: a, patchFlag: l } = t,
    u = i.emitsOptions
  if (t.dirs || t.transition) return !0
  if (n && l >= 0) {
    if (l & 1024) return !0
    if (l & 16) return r ? Us(r, s, u) : !!s
    if (l & 8) {
      const c = t.dynamicProps
      for (let f = 0; f < c.length; f++) {
        const d = c[f]
        if (s[d] !== r[d] && !vo(u, d)) return !0
      }
    }
  } else
    return (o || a) && (!a || !a.$stable) ? !0 : r === s ? !1 : r ? (s ? Us(r, s, u) : !0) : !!s
  return !1
}
function Us(e, t, n) {
  const r = Object.keys(t)
  if (r.length !== Object.keys(e).length) return !0
  for (let o = 0; o < r.length; o++) {
    const i = r[o]
    if (t[i] !== e[i] && !vo(n, i)) return !0
  }
  return !1
}
function op({ vnode: e, parent: t }, n) {
  for (; t; ) {
    const r = t.subTree
    if ((r.suspense && r.suspense.activeBranch === e && (r.el = e.el), r === e))
      (((e = t.vnode).el = n), (t = t.parent))
    else break
  }
}
const Cc = (e) => e.__isSuspense
function ip(e, t) {
  t && t.pendingBranch ? (K(e) ? t.effects.push(...e) : t.effects.push(e)) : md(e)
}
const ue = Symbol.for('v-fgt'),
  hr = Symbol.for('v-txt'),
  he = Symbol.for('v-cmt'),
  Ir = Symbol.for('v-stc'),
  Jn = []
let Pe = null
function fi(e = !1) {
  Jn.push((Pe = e ? null : []))
}
function sp() {
  ;(Jn.pop(), (Pe = Jn[Jn.length - 1] || null))
}
let bn = 1
function Yr(e, t = !1) {
  ;((bn += e), e < 0 && Pe && t && (Pe.hasOnce = !0))
}
function xc(e) {
  return ((e.dynamicChildren = bn > 0 ? Pe || dn : null), sp(), bn > 0 && Pe && Pe.push(e), e)
}
function iy(e, t, n, r, o, i) {
  return xc(_c(e, t, n, r, o, i, !0))
}
function di(e, t, n, r, o) {
  return xc(w(e, t, n, r, o, !0))
}
function ut(e) {
  return e ? e.__v_isVNode === !0 : !1
}
function zt(e, t) {
  return e.type === t.type && e.key === t.key
}
const Sc = ({ key: e }) => e ?? null,
  jr = ({ ref: e, ref_key: t, ref_for: n }) => (
    typeof e == 'number' && (e = '' + e),
    e != null ? (ce(e) || le(e) || X(e) ? { i: ge, r: e, k: t, f: !!n } : e) : null
  )
function _c(e, t = null, n = null, r = 0, o = null, i = e === ue ? 0 : 1, s = !1, a = !1) {
  const l = {
    __v_isVNode: !0,
    __v_skip: !0,
    type: e,
    props: t,
    key: t && Sc(t),
    ref: t && jr(t),
    scopeId: Wl,
    slotScopeIds: null,
    children: n,
    component: null,
    suspense: null,
    ssContent: null,
    ssFallback: null,
    dirs: null,
    transition: null,
    el: null,
    anchor: null,
    target: null,
    targetStart: null,
    targetAnchor: null,
    staticCount: 0,
    shapeFlag: i,
    patchFlag: r,
    dynamicProps: o,
    dynamicChildren: null,
    appContext: null,
    ctx: ge,
  }
  return (
    a ? (os(l, n), i & 128 && e.normalize(l)) : n && (l.shapeFlag |= ce(n) ? 8 : 16),
    bn > 0 && !s && Pe && (l.patchFlag > 0 || i & 6) && l.patchFlag !== 32 && Pe.push(l),
    l
  )
}
const w = ap
function ap(e, t = null, n = null, r = 0, o = null, i = !1) {
  if (((!e || e === rc) && (e = he), ut(e))) {
    const a = Rt(e, t, !0)
    return (
      n && os(a, n),
      bn > 0 && !i && Pe && (a.shapeFlag & 6 ? (Pe[Pe.indexOf(e)] = a) : Pe.push(a)),
      (a.patchFlag = -2),
      a
    )
  }
  if ((yp(e) && (e = e.__vccOpts), t)) {
    t = lp(t)
    let { class: a, style: l } = t
    ;(a && !ce(a) && (t.class = Ni(a)),
      oe(l) && (Ui(l) && !K(l) && (l = de({}, l)), (t.style = ki(l))))
  }
  const s = ce(e) ? 1 : Cc(e) ? 128 : Ul(e) ? 64 : oe(e) ? 4 : X(e) ? 2 : 0
  return _c(e, t, n, r, o, s, i, !0)
}
function lp(e) {
  return e ? (Ui(e) || fc(e) ? de({}, e) : e) : null
}
function Rt(e, t, n = !1, r = !1) {
  const { props: o, ref: i, patchFlag: s, children: a, transition: l } = e,
    u = t ? up(o || {}, t) : o,
    c = {
      __v_isVNode: !0,
      __v_skip: !0,
      type: e.type,
      props: u,
      key: u && Sc(u),
      ref: t && t.ref ? (n && i ? (K(i) ? i.concat(jr(t)) : [i, jr(t)]) : jr(t)) : i,
      scopeId: e.scopeId,
      slotScopeIds: e.slotScopeIds,
      children: a,
      target: e.target,
      targetStart: e.targetStart,
      targetAnchor: e.targetAnchor,
      staticCount: e.staticCount,
      shapeFlag: e.shapeFlag,
      patchFlag: t && e.type !== ue ? (s === -1 ? 16 : s | 16) : s,
      dynamicProps: e.dynamicProps,
      dynamicChildren: e.dynamicChildren,
      appContext: e.appContext,
      dirs: e.dirs,
      transition: l,
      component: e.component,
      suspense: e.suspense,
      ssContent: e.ssContent && Rt(e.ssContent),
      ssFallback: e.ssFallback && Rt(e.ssFallback),
      placeholder: e.placeholder,
      el: e.el,
      anchor: e.anchor,
      ctx: e.ctx,
      ce: e.ce,
    }
  return (l && r && Qt(c, l.clone(c)), c)
}
function cp(e = ' ', t = 0) {
  return w(hr, null, e, t)
}
function sy(e, t) {
  const n = w(Ir, null, e)
  return ((n.staticCount = t), n)
}
function ay(e = '', t = !1) {
  return t ? (fi(), di(he, null, e)) : w(he, null, e)
}
function at(e) {
  return e == null || typeof e == 'boolean'
    ? w(he)
    : K(e)
      ? w(ue, null, e.slice())
      : ut(e)
        ? At(e)
        : w(hr, null, String(e))
}
function At(e) {
  return (e.el === null && e.patchFlag !== -1) || e.memo ? e : Rt(e)
}
function os(e, t) {
  let n = 0
  const { shapeFlag: r } = e
  if (t == null) t = null
  else if (K(t)) n = 16
  else if (typeof t == 'object')
    if (r & 65) {
      const o = t.default
      o && (o._c && (o._d = !1), os(e, o()), o._c && (o._d = !0))
      return
    } else {
      n = 32
      const o = t._
      !o && !fc(t)
        ? (t._ctx = ge)
        : o === 3 && ge && (ge.slots._ === 1 ? (t._ = 1) : ((t._ = 2), (e.patchFlag |= 1024)))
    }
  else
    X(t)
      ? ((t = { default: t, _ctx: ge }), (n = 32))
      : ((t = String(t)), r & 64 ? ((n = 16), (t = [cp(t)])) : (n = 8))
  ;((e.children = t), (e.shapeFlag |= n))
}
function up(...e) {
  const t = {}
  for (let n = 0; n < e.length; n++) {
    const r = e[n]
    for (const o in r)
      if (o === 'class') t.class !== r.class && (t.class = Ni([t.class, r.class]))
      else if (o === 'style') t.style = ki([t.style, r.style])
      else if (oo(o)) {
        const i = t[o],
          s = r[o]
        s && i !== s && !(K(i) && i.includes(s)) && (t[o] = i ? [].concat(i, s) : s)
      } else o !== '' && (t[o] = r[o])
  }
  return t
}
function nt(e, t, n, r = null) {
  Je(e, t, 7, [n, r])
}
const fp = lc()
let dp = 0
function pp(e, t, n) {
  const r = e.type,
    o = (t ? t.appContext : e.appContext) || fp,
    i = {
      uid: dp++,
      vnode: e,
      type: r,
      parent: t,
      appContext: o,
      root: null,
      next: null,
      subTree: null,
      effect: null,
      update: null,
      job: null,
      scope: new bl(!0),
      render: null,
      proxy: null,
      exposed: null,
      exposeProxy: null,
      withProxy: null,
      provides: t ? t.provides : Object.create(o.provides),
      ids: t ? t.ids : ['', 0, 0],
      accessCache: null,
      renderCache: [],
      components: null,
      directives: null,
      propsOptions: pc(r, o),
      emitsOptions: bc(r, o),
      emit: null,
      emitted: null,
      propsDefaults: re,
      inheritAttrs: r.inheritAttrs,
      ctx: re,
      data: re,
      props: re,
      attrs: re,
      slots: re,
      refs: re,
      setupState: re,
      setupContext: null,
      suspense: n,
      suspenseId: n ? n.pendingId : 0,
      asyncDep: null,
      asyncResolved: !1,
      isMounted: !1,
      isUnmounted: !1,
      isDeactivated: !1,
      bc: null,
      c: null,
      bm: null,
      m: null,
      bu: null,
      u: null,
      um: null,
      bum: null,
      da: null,
      a: null,
      rtg: null,
      rtc: null,
      ec: null,
      sp: null,
    }
  return (
    (i.ctx = { _: i }),
    (i.root = t ? t.root : i),
    (i.emit = Zd.bind(null, i)),
    e.ce && e.ce(i),
    i
  )
}
let _e = null
const Lt = () => _e || ge
let Jr, pi
{
  const e = lo(),
    t = (n, r) => {
      let o
      return (
        (o = e[n]) || (o = e[n] = []),
        o.push(r),
        (i) => {
          o.length > 1 ? o.forEach((s) => s(i)) : o[0](i)
        }
      )
    }
  ;((Jr = t('__VUE_INSTANCE_SETTERS__', (n) => (_e = n))),
    (pi = t('__VUE_SSR_SETTERS__', (n) => (sr = n))))
}
const gr = (e) => {
    const t = _e
    return (
      Jr(e),
      e.scope.on(),
      () => {
        ;(e.scope.off(), Jr(t))
      }
    )
  },
  Gs = () => {
    ;(_e && _e.scope.off(), Jr(null))
  }
function wc(e) {
  return e.vnode.shapeFlag & 4
}
let sr = !1
function hp(e, t = !1, n = !1) {
  t && pi(t)
  const { props: r, children: o } = e.vnode,
    i = wc(e)
  ;(Nd(e, r, i, t), Wd(e, o, n || t))
  const s = i ? gp(e, t) : void 0
  return (t && pi(!1), s)
}
function gp(e, t) {
  const n = e.type
  ;((e.accessCache = Object.create(null)), (e.proxy = new Proxy(e.ctx, Ad)))
  const { setup: r } = n
  if (r) {
    xt()
    const o = (e.setupContext = r.length > 1 ? Tc(e) : null),
      i = gr(e),
      s = dr(r, e, 0, [e.props, o]),
      a = dl(s)
    if ((St(), i(), (a || e.sp) && !gn(e) && ec(e), a)) {
      if ((s.then(Gs, Gs), t))
        return s
          .then((l) => {
            Ks(e, l)
          })
          .catch((l) => {
            fo(l, e, 0)
          })
      e.asyncDep = s
    } else Ks(e, s)
  } else Oc(e)
}
function Ks(e, t, n) {
  ;(X(t)
    ? e.type.__ssrInlineRender
      ? (e.ssrRender = t)
      : (e.render = t)
    : oe(t) && (e.setupState = Fl(t)),
    Oc(e))
}
function Oc(e, t, n) {
  const r = e.type
  e.render || (e.render = r.render || lt)
  {
    const o = gr(e)
    xt()
    try {
      Md(e)
    } finally {
      ;(St(), o())
    }
  }
}
const mp = {
  get(e, t) {
    return (Se(e, 'get', ''), e[t])
  },
}
function Tc(e) {
  const t = (n) => {
    e.exposed = n || {}
  }
  return { attrs: new Proxy(e.attrs, mp), slots: e.slots, emit: e.emit, expose: t }
}
function yo(e) {
  return e.exposed
    ? e.exposeProxy ||
        (e.exposeProxy = new Proxy(Fl(Gi(e.exposed)), {
          get(t, n) {
            if (n in t) return t[n]
            if (n in Yn) return Yn[n](e)
          },
          has(t, n) {
            return n in t || n in Yn
          },
        }))
    : e.proxy
}
function vp(e, t = !0) {
  return X(e) ? e.displayName || e.name : e.name || (t && e.__name)
}
function yp(e) {
  return X(e) && '__vccOpts' in e
}
const L = (e, t) => fd(e, t, sr)
function Zt(e, t, n) {
  try {
    Yr(-1)
    const r = arguments.length
    return r === 2
      ? oe(t) && !K(t)
        ? ut(t)
          ? w(e, null, [t])
          : w(e, t)
        : w(e, null, t)
      : (r > 3 ? (n = Array.prototype.slice.call(arguments, 2)) : r === 3 && ut(n) && (n = [n]),
        w(e, t, n))
  } finally {
    Yr(1)
  }
}
function ly(e, t) {
  const n = e.memo
  if (n.length != t.length) return !1
  for (let r = 0; r < n.length; r++) if (bt(n[r], t[r])) return !1
  return (bn > 0 && Pe && Pe.push(e), !0)
}
const bp = '3.5.22'
/**
 * @vue/runtime-dom v3.5.22
 * (c) 2018-present Yuxi (Evan) You and Vue contributors
 * @license MIT
 **/ let hi
const Xs = typeof window < 'u' && window.trustedTypes
if (Xs)
  try {
    hi = Xs.createPolicy('vue', { createHTML: (e) => e })
  } catch {}
const $c = hi ? (e) => hi.createHTML(e) : (e) => e,
  Cp = 'http://www.w3.org/2000/svg',
  xp = 'http://www.w3.org/1998/Math/MathML',
  gt = typeof document < 'u' ? document : null,
  qs = gt && gt.createElement('template'),
  Sp = {
    insert: (e, t, n) => {
      t.insertBefore(e, n || null)
    },
    remove: (e) => {
      const t = e.parentNode
      t && t.removeChild(e)
    },
    createElement: (e, t, n, r) => {
      const o =
        t === 'svg'
          ? gt.createElementNS(Cp, e)
          : t === 'mathml'
            ? gt.createElementNS(xp, e)
            : n
              ? gt.createElement(e, { is: n })
              : gt.createElement(e)
      return (
        e === 'select' && r && r.multiple != null && o.setAttribute('multiple', r.multiple),
        o
      )
    },
    createText: (e) => gt.createTextNode(e),
    createComment: (e) => gt.createComment(e),
    setText: (e, t) => {
      e.nodeValue = t
    },
    setElementText: (e, t) => {
      e.textContent = t
    },
    parentNode: (e) => e.parentNode,
    nextSibling: (e) => e.nextSibling,
    querySelector: (e) => gt.querySelector(e),
    setScopeId(e, t) {
      e.setAttribute(t, '')
    },
    insertStaticContent(e, t, n, r, o, i) {
      const s = n ? n.previousSibling : t.lastChild
      if (o && (o === i || o.nextSibling))
        for (; t.insertBefore(o.cloneNode(!0), n), !(o === i || !(o = o.nextSibling)); );
      else {
        qs.innerHTML = $c(
          r === 'svg' ? `<svg>${e}</svg>` : r === 'mathml' ? `<math>${e}</math>` : e
        )
        const a = qs.content
        if (r === 'svg' || r === 'mathml') {
          const l = a.firstChild
          for (; l.firstChild; ) a.appendChild(l.firstChild)
          a.removeChild(l)
        }
        t.insertBefore(a, n)
      }
      return [s ? s.nextSibling : t.firstChild, n ? n.previousSibling : t.lastChild]
    },
  },
  Tt = 'transition',
  Nn = 'animation',
  Cn = Symbol('_vtc'),
  Pc = {
    name: String,
    type: String,
    css: { type: Boolean, default: !0 },
    duration: [String, Number, Object],
    enterFromClass: String,
    enterActiveClass: String,
    enterToClass: String,
    appearFromClass: String,
    appearActiveClass: String,
    appearToClass: String,
    leaveFromClass: String,
    leaveActiveClass: String,
    leaveToClass: String,
  },
  Ec = de({}, Yl, Pc),
  _p = (e) => ((e.displayName = 'Transition'), (e.props = Ec), e),
  cy = _p((e, { slots: t }) => Zt(Cd, Ac(e), t)),
  Dt = (e, t = []) => {
    K(e) ? e.forEach((n) => n(...t)) : e && e(...t)
  },
  Ys = (e) => (e ? (K(e) ? e.some((t) => t.length > 1) : e.length > 1) : !1)
function Ac(e) {
  const t = {}
  for (const k in e) k in Pc || (t[k] = e[k])
  if (e.css === !1) return t
  const {
      name: n = 'v',
      type: r,
      duration: o,
      enterFromClass: i = `${n}-enter-from`,
      enterActiveClass: s = `${n}-enter-active`,
      enterToClass: a = `${n}-enter-to`,
      appearFromClass: l = i,
      appearActiveClass: u = s,
      appearToClass: c = a,
      leaveFromClass: f = `${n}-leave-from`,
      leaveActiveClass: d = `${n}-leave-active`,
      leaveToClass: p = `${n}-leave-to`,
    } = e,
    m = wp(o),
    v = m && m[0],
    b = m && m[1],
    {
      onBeforeEnter: C,
      onEnter: O,
      onEnterCancelled: P,
      onLeave: x,
      onLeaveCancelled: _,
      onBeforeAppear: H = C,
      onAppear: y = O,
      onAppearCancelled: E = P,
    } = t,
    $ = (k, ee, ae, M) => {
      ;((k._enterCancelled = M), $t(k, ee ? c : a), $t(k, ee ? u : s), ae && ae())
    },
    W = (k, ee) => {
      ;((k._isLeaving = !1), $t(k, f), $t(k, p), $t(k, d), ee && ee())
    },
    Y = (k) => (ee, ae) => {
      const M = k ? y : O,
        B = () => $(ee, k, ae)
      ;(Dt(M, [ee, B]),
        Js(() => {
          ;($t(ee, k ? l : i), rt(ee, k ? c : a), Ys(M) || Qs(ee, r, v, B))
        }))
    }
  return de(t, {
    onBeforeEnter(k) {
      ;(Dt(C, [k]), rt(k, i), rt(k, s))
    },
    onBeforeAppear(k) {
      ;(Dt(H, [k]), rt(k, l), rt(k, u))
    },
    onEnter: Y(!1),
    onAppear: Y(!0),
    onLeave(k, ee) {
      k._isLeaving = !0
      const ae = () => W(k, ee)
      ;(rt(k, f),
        k._enterCancelled ? (rt(k, d), gi(k)) : (gi(k), rt(k, d)),
        Js(() => {
          k._isLeaving && ($t(k, f), rt(k, p), Ys(x) || Qs(k, r, b, ae))
        }),
        Dt(x, [k, ae]))
    },
    onEnterCancelled(k) {
      ;($(k, !1, void 0, !0), Dt(P, [k]))
    },
    onAppearCancelled(k) {
      ;($(k, !0, void 0, !0), Dt(E, [k]))
    },
    onLeaveCancelled(k) {
      ;(W(k), Dt(_, [k]))
    },
  })
}
function wp(e) {
  if (e == null) return null
  if (oe(e)) return [Do(e.enter), Do(e.leave)]
  {
    const t = Do(e)
    return [t, t]
  }
}
function Do(e) {
  return $f(e)
}
function rt(e, t) {
  ;(t.split(/\s+/).forEach((n) => n && e.classList.add(n)), (e[Cn] || (e[Cn] = new Set())).add(t))
}
function $t(e, t) {
  t.split(/\s+/).forEach((r) => r && e.classList.remove(r))
  const n = e[Cn]
  n && (n.delete(t), n.size || (e[Cn] = void 0))
}
function Js(e) {
  requestAnimationFrame(() => {
    requestAnimationFrame(e)
  })
}
let Op = 0
function Qs(e, t, n, r) {
  const o = (e._endId = ++Op),
    i = () => {
      o === e._endId && r()
    }
  if (n != null) return setTimeout(i, n)
  const { type: s, timeout: a, propCount: l } = Mc(e, t)
  if (!s) return r()
  const u = s + 'end'
  let c = 0
  const f = () => {
      ;(e.removeEventListener(u, d), i())
    },
    d = (p) => {
      p.target === e && ++c >= l && f()
    }
  ;(setTimeout(() => {
    c < l && f()
  }, a + 1),
    e.addEventListener(u, d))
}
function Mc(e, t) {
  const n = window.getComputedStyle(e),
    r = (m) => (n[m] || '').split(', '),
    o = r(`${Tt}Delay`),
    i = r(`${Tt}Duration`),
    s = Zs(o, i),
    a = r(`${Nn}Delay`),
    l = r(`${Nn}Duration`),
    u = Zs(a, l)
  let c = null,
    f = 0,
    d = 0
  t === Tt
    ? s > 0 && ((c = Tt), (f = s), (d = i.length))
    : t === Nn
      ? u > 0 && ((c = Nn), (f = u), (d = l.length))
      : ((f = Math.max(s, u)),
        (c = f > 0 ? (s > u ? Tt : Nn) : null),
        (d = c ? (c === Tt ? i.length : l.length) : 0))
  const p = c === Tt && /\b(?:transform|all)(?:,|$)/.test(r(`${Tt}Property`).toString())
  return { type: c, timeout: f, propCount: d, hasTransform: p }
}
function Zs(e, t) {
  for (; e.length < t.length; ) e = e.concat(e)
  return Math.max(...t.map((n, r) => ea(n) + ea(e[r])))
}
function ea(e) {
  return e === 'auto' ? 0 : Number(e.slice(0, -1).replace(',', '.')) * 1e3
}
function gi(e) {
  return (e ? e.ownerDocument : document).body.offsetHeight
}
function Tp(e, t, n) {
  const r = e[Cn]
  ;(r && (t = (t ? [t, ...r] : [...r]).join(' ')),
    t == null ? e.removeAttribute('class') : n ? e.setAttribute('class', t) : (e.className = t))
}
const Qr = Symbol('_vod'),
  Ic = Symbol('_vsh'),
  uy = {
    name: 'show',
    beforeMount(e, { value: t }, { transition: n }) {
      ;((e[Qr] = e.style.display === 'none' ? '' : e.style.display),
        n && t ? n.beforeEnter(e) : Dn(e, t))
    },
    mounted(e, { value: t }, { transition: n }) {
      n && t && n.enter(e)
    },
    updated(e, { value: t, oldValue: n }, { transition: r }) {
      !t != !n &&
        (r
          ? t
            ? (r.beforeEnter(e), Dn(e, !0), r.enter(e))
            : r.leave(e, () => {
                Dn(e, !1)
              })
          : Dn(e, t))
    },
    beforeUnmount(e, { value: t }) {
      Dn(e, t)
    },
  }
function Dn(e, t) {
  ;((e.style.display = t ? e[Qr] : 'none'), (e[Ic] = !t))
}
const $p = Symbol(''),
  Pp = /(?:^|;)\s*display\s*:/
function Ep(e, t, n) {
  const r = e.style,
    o = ce(n)
  let i = !1
  if (n && !o) {
    if (t)
      if (ce(t))
        for (const s of t.split(';')) {
          const a = s.slice(0, s.indexOf(':')).trim()
          n[a] == null && Rr(r, a, '')
        }
      else for (const s in t) n[s] == null && Rr(r, s, '')
    for (const s in n) (s === 'display' && (i = !0), Rr(r, s, n[s]))
  } else if (o) {
    if (t !== n) {
      const s = r[$p]
      ;(s && (n += ';' + s), (r.cssText = n), (i = Pp.test(n)))
    }
  } else t && e.removeAttribute('style')
  Qr in e && ((e[Qr] = i ? r.display : ''), e[Ic] && (r.display = 'none'))
}
const ta = /\s*!important$/
function Rr(e, t, n) {
  if (K(n)) n.forEach((r) => Rr(e, t, r))
  else if ((n == null && (n = ''), t.startsWith('--'))) e.setProperty(t, n)
  else {
    const r = Ap(e, t)
    ta.test(n) ? e.setProperty(nn(r), n.replace(ta, ''), 'important') : (e[r] = n)
  }
}
const na = ['Webkit', 'Moz', 'ms'],
  Bo = {}
function Ap(e, t) {
  const n = Bo[t]
  if (n) return n
  let r = Ve(t)
  if (r !== 'filter' && r in e) return (Bo[t] = r)
  r = ao(r)
  for (let o = 0; o < na.length; o++) {
    const i = na[o] + r
    if (i in e) return (Bo[t] = i)
  }
  return t
}
const ra = 'http://www.w3.org/1999/xlink'
function oa(e, t, n, r, o, i = jf(t)) {
  r && t.startsWith('xlink:')
    ? n == null
      ? e.removeAttributeNS(ra, t.slice(6, t.length))
      : e.setAttributeNS(ra, t, n)
    : n == null || (i && !ml(n))
      ? e.removeAttribute(t)
      : e.setAttribute(t, i ? '' : _t(n) ? String(n) : n)
}
function ia(e, t, n, r, o) {
  if (t === 'innerHTML' || t === 'textContent') {
    n != null && (e[t] = t === 'innerHTML' ? $c(n) : n)
    return
  }
  const i = e.tagName
  if (t === 'value' && i !== 'PROGRESS' && !i.includes('-')) {
    const a = i === 'OPTION' ? e.getAttribute('value') || '' : e.value,
      l = n == null ? (e.type === 'checkbox' ? 'on' : '') : String(n)
    ;((a !== l || !('_value' in e)) && (e.value = l),
      n == null && e.removeAttribute(t),
      (e._value = n))
    return
  }
  let s = !1
  if (n === '' || n == null) {
    const a = typeof e[t]
    a === 'boolean'
      ? (n = ml(n))
      : n == null && a === 'string'
        ? ((n = ''), (s = !0))
        : a === 'number' && ((n = 0), (s = !0))
  }
  try {
    e[t] = n
  } catch {}
  s && e.removeAttribute(o || t)
}
function Mp(e, t, n, r) {
  e.addEventListener(t, n, r)
}
function Ip(e, t, n, r) {
  e.removeEventListener(t, n, r)
}
const sa = Symbol('_vei')
function jp(e, t, n, r, o = null) {
  const i = e[sa] || (e[sa] = {}),
    s = i[t]
  if (r && s) s.value = r
  else {
    const [a, l] = Rp(t)
    if (r) {
      const u = (i[t] = Fp(r, o))
      Mp(e, a, u, l)
    } else s && (Ip(e, a, s, l), (i[t] = void 0))
  }
}
const aa = /(?:Once|Passive|Capture)$/
function Rp(e) {
  let t
  if (aa.test(e)) {
    t = {}
    let r
    for (; (r = e.match(aa)); )
      ((e = e.slice(0, e.length - r[0].length)), (t[r[0].toLowerCase()] = !0))
  }
  return [e[2] === ':' ? e.slice(3) : nn(e.slice(2)), t]
}
let zo = 0
const Lp = Promise.resolve(),
  Hp = () => zo || (Lp.then(() => (zo = 0)), (zo = Date.now()))
function Fp(e, t) {
  const n = (r) => {
    if (!r._vts) r._vts = Date.now()
    else if (r._vts <= n.attached) return
    Je(kp(r, n.value), t, 5, [r])
  }
  return ((n.value = e), (n.attached = Hp()), n)
}
function kp(e, t) {
  if (K(t)) {
    const n = e.stopImmediatePropagation
    return (
      (e.stopImmediatePropagation = () => {
        ;(n.call(e), (e._stopped = !0))
      }),
      t.map((r) => (o) => !o._stopped && r && r(o))
    )
  } else return t
}
const la = (e) =>
    e.charCodeAt(0) === 111 &&
    e.charCodeAt(1) === 110 &&
    e.charCodeAt(2) > 96 &&
    e.charCodeAt(2) < 123,
  Np = (e, t, n, r, o, i) => {
    const s = o === 'svg'
    t === 'class'
      ? Tp(e, r, s)
      : t === 'style'
        ? Ep(e, n, r)
        : oo(t)
          ? Li(t) || jp(e, t, n, r, i)
          : (
                t[0] === '.'
                  ? ((t = t.slice(1)), !0)
                  : t[0] === '^'
                    ? ((t = t.slice(1)), !1)
                    : Dp(e, t, r, s)
              )
            ? (ia(e, t, r),
              !e.tagName.includes('-') &&
                (t === 'value' || t === 'checked' || t === 'selected') &&
                oa(e, t, r, s, i, t !== 'value'))
            : e._isVueCE && (/[A-Z]/.test(t) || !ce(r))
              ? ia(e, Ve(t), r, i, t)
              : (t === 'true-value'
                  ? (e._trueValue = r)
                  : t === 'false-value' && (e._falseValue = r),
                oa(e, t, r, s))
  }
function Dp(e, t, n, r) {
  if (r) return !!(t === 'innerHTML' || t === 'textContent' || (t in e && la(t) && X(n)))
  if (
    t === 'spellcheck' ||
    t === 'draggable' ||
    t === 'translate' ||
    t === 'autocorrect' ||
    t === 'form' ||
    (t === 'list' && e.tagName === 'INPUT') ||
    (t === 'type' && e.tagName === 'TEXTAREA')
  )
    return !1
  if (t === 'width' || t === 'height') {
    const o = e.tagName
    if (o === 'IMG' || o === 'VIDEO' || o === 'CANVAS' || o === 'SOURCE') return !1
  }
  return la(t) && ce(n) ? !1 : t in e
}
const jc = new WeakMap(),
  Rc = new WeakMap(),
  Zr = Symbol('_moveCb'),
  ca = Symbol('_enterCb'),
  Bp = (e) => (delete e.props.mode, e),
  zp = Bp({
    name: 'TransitionGroup',
    props: de({}, Ec, { tag: String, moveClass: String }),
    setup(e, { slots: t }) {
      const n = Lt(),
        r = ql()
      let o, i
      return (
        qi(() => {
          if (!o.length) return
          const s = e.moveClass || `${e.name || 'v'}-move`
          if (!Gp(o[0].el, n.vnode.el, s)) {
            o = []
            return
          }
          ;(o.forEach(Wp), o.forEach(Vp))
          const a = o.filter(Up)
          ;(gi(n.vnode.el),
            a.forEach((l) => {
              const u = l.el,
                c = u.style
              ;(rt(u, s), (c.transform = c.webkitTransform = c.transitionDuration = ''))
              const f = (u[Zr] = (d) => {
                ;(d && d.target !== u) ||
                  ((!d || d.propertyName.endsWith('transform')) &&
                    (u.removeEventListener('transitionend', f), (u[Zr] = null), $t(u, s)))
              })
              u.addEventListener('transitionend', f)
            }),
            (o = []))
        }),
        () => {
          const s = J(e),
            a = Ac(s)
          let l = s.tag || ue
          if (((o = []), i))
            for (let u = 0; u < i.length; u++) {
              const c = i[u]
              c.el &&
                c.el instanceof Element &&
                (o.push(c), Qt(c, ir(c, a, r, n)), jc.set(c, c.el.getBoundingClientRect()))
            }
          i = t.default ? Xi(t.default()) : []
          for (let u = 0; u < i.length; u++) {
            const c = i[u]
            c.key != null && Qt(c, ir(c, a, r, n))
          }
          return w(l, null, i)
        }
      )
    },
  }),
  Lc = zp
function Wp(e) {
  const t = e.el
  ;(t[Zr] && t[Zr](), t[ca] && t[ca]())
}
function Vp(e) {
  Rc.set(e, e.el.getBoundingClientRect())
}
function Up(e) {
  const t = jc.get(e),
    n = Rc.get(e),
    r = t.left - n.left,
    o = t.top - n.top
  if (r || o) {
    const i = e.el.style
    return (
      (i.transform = i.webkitTransform = `translate(${r}px,${o}px)`),
      (i.transitionDuration = '0s'),
      e
    )
  }
}
function Gp(e, t, n) {
  const r = e.cloneNode(),
    o = e[Cn]
  ;(o &&
    o.forEach((a) => {
      a.split(/\s+/).forEach((l) => l && r.classList.remove(l))
    }),
    n.split(/\s+/).forEach((a) => a && r.classList.add(a)),
    (r.style.display = 'none'))
  const i = t.nodeType === 1 ? t : t.parentNode
  i.appendChild(r)
  const { hasTransform: s } = Mc(r)
  return (i.removeChild(r), s)
}
const Kp = ['ctrl', 'shift', 'alt', 'meta'],
  Xp = {
    stop: (e) => e.stopPropagation(),
    prevent: (e) => e.preventDefault(),
    self: (e) => e.target !== e.currentTarget,
    ctrl: (e) => !e.ctrlKey,
    shift: (e) => !e.shiftKey,
    alt: (e) => !e.altKey,
    meta: (e) => !e.metaKey,
    left: (e) => 'button' in e && e.button !== 0,
    middle: (e) => 'button' in e && e.button !== 1,
    right: (e) => 'button' in e && e.button !== 2,
    exact: (e, t) => Kp.some((n) => e[`${n}Key`] && !t.includes(n)),
  },
  fy = (e, t) => {
    const n = e._withMods || (e._withMods = {}),
      r = t.join('.')
    return (
      n[r] ||
      (n[r] = (o, ...i) => {
        for (let s = 0; s < t.length; s++) {
          const a = Xp[t[s]]
          if (a && a(o, t)) return
        }
        return e(o, ...i)
      })
    )
  },
  qp = de({ patchProp: Np }, Sp)
let ua
function Hc() {
  return ua || (ua = Ud(qp))
}
const fa = (...e) => {
    Hc().render(...e)
  },
  dy = (...e) => {
    const t = Hc().createApp(...e),
      { mount: n } = t
    return (
      (t.mount = (r) => {
        const o = Jp(r)
        if (!o) return
        const i = t._component
        ;(!X(i) && !i.render && !i.template && (i.template = o.innerHTML),
          o.nodeType === 1 && (o.textContent = ''))
        const s = n(o, !1, Yp(o))
        return (
          o instanceof Element && (o.removeAttribute('v-cloak'), o.setAttribute('data-v-app', '')),
          s
        )
      }),
      t
    )
  }
function Yp(e) {
  if (e instanceof SVGElement) return 'svg'
  if (typeof MathMLElement == 'function' && e instanceof MathMLElement) return 'mathml'
}
function Jp(e) {
  return ce(e) ? document.querySelector(e) : e
}
/*!
 * pinia v3.0.3
 * (c) 2025 Eduardo San Martin Morote
 * @license MIT
 */ let Fc
const bo = (e) => (Fc = e),
  kc = Symbol()
function mi(e) {
  return (
    e &&
    typeof e == 'object' &&
    Object.prototype.toString.call(e) === '[object Object]' &&
    typeof e.toJSON != 'function'
  )
}
var Qn
;(function (e) {
  ;((e.direct = 'direct'), (e.patchObject = 'patch object'), (e.patchFunction = 'patch function'))
})(Qn || (Qn = {}))
function py() {
  const e = Cl(!0),
    t = e.run(() => qe({}))
  let n = [],
    r = []
  const o = Gi({
    install(i) {
      ;(bo(o),
        (o._a = i),
        i.provide(kc, o),
        (i.config.globalProperties.$pinia = o),
        r.forEach((s) => n.push(s)),
        (r = []))
    },
    use(i) {
      return (this._a ? n.push(i) : r.push(i), this)
    },
    _p: n,
    _a: null,
    _e: e,
    _s: new Map(),
    state: t,
  })
  return o
}
const Nc = () => {}
function da(e, t, n, r = Nc) {
  e.push(t)
  const o = () => {
    const i = e.indexOf(t)
    i > -1 && (e.splice(i, 1), r())
  }
  return (!n && xl() && Lf(o), o)
}
function sn(e, ...t) {
  e.slice().forEach((n) => {
    n(...t)
  })
}
const Qp = (e) => e(),
  pa = Symbol(),
  Wo = Symbol()
function vi(e, t) {
  e instanceof Map && t instanceof Map
    ? t.forEach((n, r) => e.set(r, n))
    : e instanceof Set && t instanceof Set && t.forEach(e.add, e)
  for (const n in t) {
    if (!t.hasOwnProperty(n)) continue
    const r = t[n],
      o = e[n]
    mi(o) && mi(r) && e.hasOwnProperty(n) && !le(r) && !Ct(r) ? (e[n] = vi(o, r)) : (e[n] = r)
  }
  return e
}
const Zp = Symbol()
function eh(e) {
  return !mi(e) || !Object.prototype.hasOwnProperty.call(e, Zp)
}
const { assign: Pt } = Object
function th(e) {
  return !!(le(e) && e.effect)
}
function nh(e, t, n, r) {
  const { state: o, actions: i, getters: s } = t,
    a = n.state.value[e]
  let l
  function u() {
    a || (n.state.value[e] = o ? o() : {})
    const c = sd(n.state.value[e])
    return Pt(
      c,
      i,
      Object.keys(s || {}).reduce(
        (f, d) => (
          (f[d] = Gi(
            L(() => {
              bo(n)
              const p = n._s.get(e)
              return s[d].call(p, p)
            })
          )),
          f
        ),
        {}
      )
    )
  }
  return ((l = Dc(e, u, t, n, r, !0)), l)
}
function Dc(e, t, n = {}, r, o, i) {
  let s
  const a = Pt({ actions: {} }, n),
    l = { deep: !0 }
  let u,
    c,
    f = [],
    d = [],
    p
  const m = r.state.value[e]
  ;(!i && !m && (r.state.value[e] = {}), qe({}))
  let v
  function b(E) {
    let $
    ;((u = c = !1),
      typeof E == 'function'
        ? (E(r.state.value[e]), ($ = { type: Qn.patchFunction, storeId: e, events: p }))
        : (vi(r.state.value[e], E),
          ($ = { type: Qn.patchObject, payload: E, storeId: e, events: p })))
    const W = (v = Symbol())
    ;(po().then(() => {
      v === W && (u = !0)
    }),
      (c = !0),
      sn(f, $, r.state.value[e]))
  }
  const C = i
    ? function () {
        const { state: $ } = n,
          W = $ ? $() : {}
        this.$patch((Y) => {
          Pt(Y, W)
        })
      }
    : Nc
  function O() {
    ;(s.stop(), (f = []), (d = []), r._s.delete(e))
  }
  const P = (E, $ = '') => {
      if (pa in E) return ((E[Wo] = $), E)
      const W = function () {
        bo(r)
        const Y = Array.from(arguments),
          k = [],
          ee = []
        function ae(V) {
          k.push(V)
        }
        function M(V) {
          ee.push(V)
        }
        sn(d, { args: Y, name: W[Wo], store: _, after: ae, onError: M })
        let B
        try {
          B = E.apply(this && this.$id === e ? this : _, Y)
        } catch (V) {
          throw (sn(ee, V), V)
        }
        return B instanceof Promise
          ? B.then((V) => (sn(k, V), V)).catch((V) => (sn(ee, V), Promise.reject(V)))
          : (sn(k, B), B)
      }
      return ((W[pa] = !0), (W[Wo] = $), W)
    },
    x = {
      _p: r,
      $id: e,
      $onAction: da.bind(null, d),
      $patch: b,
      $reset: C,
      $subscribe(E, $ = {}) {
        const W = da(f, E, $.detached, () => Y()),
          Y = s.run(() =>
            Fe(
              () => r.state.value[e],
              (k) => {
                ;($.flush === 'sync' ? c : u) && E({ storeId: e, type: Qn.direct, events: p }, k)
              },
              Pt({}, l, $)
            )
          )
        return W
      },
      $dispose: O,
    },
    _ = ct(x)
  r._s.set(e, _)
  const y = ((r._a && r._a.runWithContext) || Qp)(() =>
    r._e.run(() => (s = Cl()).run(() => t({ action: P })))
  )
  for (const E in y) {
    const $ = y[E]
    if ((le($) && !th($)) || Ct($))
      i || (m && eh($) && (le($) ? ($.value = m[E]) : vi($, m[E])), (r.state.value[e][E] = $))
    else if (typeof $ == 'function') {
      const W = P($, E)
      ;((y[E] = W), (a.actions[E] = $))
    }
  }
  return (
    Pt(_, y),
    Pt(J(_), y),
    Object.defineProperty(_, '$state', {
      get: () => r.state.value[e],
      set: (E) => {
        b(($) => {
          Pt($, E)
        })
      },
    }),
    r._p.forEach((E) => {
      Pt(
        _,
        s.run(() => E({ store: _, app: r._a, pinia: r, options: a }))
      )
    }),
    m && i && n.hydrate && n.hydrate(_.$state, m),
    (u = !0),
    (c = !0),
    _
  )
}
/*! #__NO_SIDE_EFFECTS__ */ function hy(e, t, n) {
  let r
  const o = typeof t == 'function'
  r = o ? n : t
  function i(s, a) {
    const l = kd()
    return (
      (s = s || (l ? Ee(kc, null) : null)),
      s && bo(s),
      (s = Fc),
      s._s.has(e) || (o ? Dc(e, t, r, s) : nh(e, r, s)),
      s._s.get(e)
    )
  }
  return ((i.$id = e), i)
}
function gy(e) {
  const t = J(e),
    n = {}
  for (const r in t) {
    const o = t[r]
    o.effect
      ? (n[r] = L({
          get: () => e[r],
          set(i) {
            e[r] = i
          },
        }))
      : (le(o) || Ct(o)) && (n[r] = cd(e, r))
  }
  return n
}
function ar(e) {
  '@babel/helpers - typeof'
  return (
    (ar =
      typeof Symbol == 'function' && typeof Symbol.iterator == 'symbol'
        ? function (t) {
            return typeof t
          }
        : function (t) {
            return t &&
              typeof Symbol == 'function' &&
              t.constructor === Symbol &&
              t !== Symbol.prototype
              ? 'symbol'
              : typeof t
          }),
    ar(e)
  )
}
function rh(e, t) {
  if (ar(e) != 'object' || !e) return e
  var n = e[Symbol.toPrimitive]
  if (n !== void 0) {
    var r = n.call(e, t)
    if (ar(r) != 'object') return r
    throw new TypeError('@@toPrimitive must return a primitive value.')
  }
  return (t === 'string' ? String : Number)(e)
}
function oh(e) {
  var t = rh(e, 'string')
  return ar(t) == 'symbol' ? t : t + ''
}
function ih(e, t, n) {
  return (
    (t = oh(t)) in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
function ha(e, t) {
  var n = Object.keys(e)
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(e)
    ;(t &&
      (r = r.filter(function (o) {
        return Object.getOwnPropertyDescriptor(e, o).enumerable
      })),
      n.push.apply(n, r))
  }
  return n
}
function me(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {}
    t % 2
      ? ha(Object(n), !0).forEach(function (r) {
          ih(e, r, n[r])
        })
      : Object.getOwnPropertyDescriptors
        ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n))
        : ha(Object(n)).forEach(function (r) {
            Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(n, r))
          })
  }
  return e
}
function T() {
  return (
    (T = Object.assign
      ? Object.assign.bind()
      : function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t]
            for (var r in n) ({}).hasOwnProperty.call(n, r) && (e[r] = n[r])
          }
          return e
        }),
    T.apply(null, arguments)
  )
}
const sh = (e) => typeof e == 'function',
  ah = Array.isArray,
  lh = (e) => typeof e == 'string',
  ch = (e) => e !== null && typeof e == 'object',
  uh = /^on[^a-z]/,
  fh = (e) => uh.test(e),
  is = (e) => {
    const t = Object.create(null)
    return (n) => t[n] || (t[n] = e(n))
  },
  dh = /-(\w)/g,
  Bc = is((e) => e.replace(dh, (t, n) => (n ? n.toUpperCase() : ''))),
  ph = /\B([A-Z])/g,
  hh = is((e) => e.replace(ph, '-$1').toLowerCase()),
  my = is((e) => e.charAt(0).toUpperCase() + e.slice(1)),
  gh = Object.prototype.hasOwnProperty,
  ga = (e, t) => gh.call(e, t)
function mh(e, t, n, r) {
  const o = e[n]
  if (o != null) {
    const i = ga(o, 'default')
    if (i && r === void 0) {
      const s = o.default
      r = o.type !== Function && sh(s) ? s() : s
    }
    o.type === Boolean && (!ga(t, n) && !i ? (r = !1) : r === '' && (r = !0))
  }
  return r
}
function vy(e) {
  return Object.keys(e).reduce(
    (t, n) => ((n.startsWith('data-') || n.startsWith('aria-')) && (t[n] = e[n]), t),
    {}
  )
}
function un(e) {
  let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {},
    n = arguments.length > 2 ? arguments[2] : void 0
  return typeof e == 'function' ? e(t) : (e ?? n)
}
function vh(e) {
  let t
  const n = new Promise((o) => {
      t = e(() => {
        o(!0)
      })
    }),
    r = () => {
      t?.()
    }
  return ((r.then = (o, i) => n.then(o, i)), (r.promise = n), r)
}
function De() {
  const e = []
  for (let t = 0; t < arguments.length; t++) {
    const n = t < 0 || arguments.length <= t ? void 0 : arguments[t]
    if (n) {
      if (lh(n)) e.push(n)
      else if (ah(n))
        for (let r = 0; r < n.length; r++) {
          const o = De(n[r])
          o && e.push(o)
        }
      else if (ch(n)) for (const r in n) n[r] && e.push(r)
    }
  }
  return e.join(' ')
}
const yh = (e) => e != null && e !== '',
  yy = (e, t) => {
    const n = T({}, e)
    return (
      Object.keys(t).forEach((r) => {
        const o = n[r]
        if (o)
          o.type || o.default
            ? (o.default = t[r])
            : o.def
              ? o.def(t[r])
              : (n[r] = { type: o, default: t[r] })
        else throw new Error(`not have ${r} prop`)
      }),
      n
    )
  },
  bh = (e) => {
    const t = Object.keys(e),
      n = {},
      r = {},
      o = {}
    for (let i = 0, s = t.length; i < s; i++) {
      const a = t[i]
      fh(a) ? ((n[a[2].toLowerCase() + a.slice(3)] = e[a]), (r[a] = e[a])) : (o[a] = e[a])
    }
    return { onEvents: r, events: n, extraAttrs: o }
  },
  Ch = function () {
    let e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : '',
      t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1
    const n = {},
      r = /;(?![^(]*\))/g,
      o = /:(.+)/
    return typeof e == 'object'
      ? e
      : (e.split(r).forEach(function (i) {
          if (i) {
            const s = i.split(o)
            if (s.length > 1) {
              const a = t ? Bc(s[0].trim()) : s[0].trim()
              n[a] = s[1].trim()
            }
          }
        }),
        n)
  },
  by = (e, t) => e[t] !== void 0,
  xh = Symbol('skipFlatten'),
  mn = function () {
    let e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [],
      t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0
    const n = Array.isArray(e) ? e : [e],
      r = []
    return (
      n.forEach((o) => {
        Array.isArray(o)
          ? r.push(...mn(o, t))
          : o && o.type === ue
            ? o.key === xh
              ? r.push(o)
              : r.push(...mn(o.children, t))
            : o && ut(o)
              ? t && !zc(o)
                ? r.push(o)
                : t || r.push(o)
              : yh(o) && r.push(o)
      }),
      r
    )
  },
  Cy = function (e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 'default',
      n = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : {}
    if (ut(e))
      return e.type === ue
        ? t === 'default'
          ? mn(e.children)
          : []
        : e.children && e.children[t]
          ? mn(e.children[t](n))
          : []
    {
      const r = e.$slots[t] && e.$slots[t](n)
      return mn(r)
    }
  },
  xy = (e) => {
    var t
    let n = ((t = e?.vnode) === null || t === void 0 ? void 0 : t.el) || (e && (e.$el || e))
    for (; n && !n.tagName; ) n = n.nextSibling
    return n
  },
  Sy = (e) => {
    const t = {}
    if (e.$ && e.$.vnode) {
      const n = e.$.vnode.props || {}
      Object.keys(e.$props).forEach((r) => {
        const o = e.$props[r],
          i = hh(r)
        ;(o !== void 0 || i in n) && (t[r] = o)
      })
    } else if (ut(e) && typeof e.type == 'object') {
      const n = e.props || {},
        r = {}
      Object.keys(n).forEach((i) => {
        r[Bc(i)] = n[i]
      })
      const o = e.type.props || {}
      Object.keys(o).forEach((i) => {
        const s = mh(o, r, i, r[i])
        ;(s !== void 0 || i in r) && (t[i] = s)
      })
    }
    return t
  },
  _y = function (e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 'default',
      n = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : e,
      r = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : !0,
      o
    if (e.$) {
      const i = e[t]
      if (i !== void 0) return typeof i == 'function' && r ? i(n) : i
      ;((o = e.$slots[t]), (o = r && o ? o(n) : o))
    } else if (ut(e)) {
      const i = e.props && e.props[t]
      if (i !== void 0 && e.props !== null) return typeof i == 'function' && r ? i(n) : i
      e.type === ue
        ? (o = e.children)
        : e.children && e.children[t] && ((o = e.children[t]), (o = r && o ? o(n) : o))
    }
    return (
      Array.isArray(o) &&
        ((o = mn(o)), (o = o.length === 1 ? o[0] : o), (o = o.length === 0 ? void 0 : o)),
      o
    )
  }
function wy() {
  let e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {},
    t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0,
    n = {}
  return (
    e.$ ? (n = T(T({}, n), e.$attrs)) : (n = T(T({}, n), e.props)),
    bh(n)[t ? 'onEvents' : 'events']
  )
}
function Oy(e, t) {
  let r = ((ut(e) ? e.props : e.$attrs) || {}).style || {}
  return (typeof r == 'string' && (r = Ch(r, t)), r)
}
function Ty(e) {
  return e.length === 1 && e[0].type === ue
}
function zc(e) {
  return (
    e &&
    (e.type === he ||
      (e.type === ue && e.children.length === 0) ||
      (e.type === hr && e.children.trim() === ''))
  )
}
function Wc() {
  let e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : []
  const t = []
  return (
    e.forEach((n) => {
      Array.isArray(n) ? t.push(...n) : n?.type === ue ? t.push(...Wc(n.children)) : t.push(n)
    }),
    t.filter((n) => !zc(n))
  )
}
function $y(e) {
  return (
    Array.isArray(e) && e.length === 1 && (e = e[0]),
    e && e.__v_isVNode && typeof e.type != 'symbol'
  )
}
function Py(e, t) {
  let n = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : 'default'
  var r, o
  return (r = t[n]) !== null && r !== void 0
    ? r
    : (o = e[n]) === null || o === void 0
      ? void 0
      : o.call(e)
}
const Sh = function () {
    for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++) t[n] = arguments[n]
    return t
  },
  ss = (e) => {
    const t = e
    return (
      (t.install = function (n) {
        n.component(t.displayName || t.name, e)
      }),
      e
    )
  }
function Ey() {
  return { type: [Function, Array] }
}
function He(e) {
  return { type: Object, default: e }
}
function Vo(e) {
  return { type: Boolean, default: e }
}
function Ay(e) {
  return { type: Function, default: e }
}
function yi(e, t) {
  return { validator: () => !0, default: e }
}
function ma(e) {
  return { type: Array, default: e }
}
function va(e) {
  return { type: String, default: e }
}
function _h(e, t) {
  return e ? { type: e, default: t } : yi(t)
}
const as = 'anticon',
  wh = Symbol('GlobalFormContextKey'),
  Oh = (e) => {
    Ot(wh, e)
  },
  Th = () => ({
    iconPrefixCls: String,
    getTargetContainer: { type: Function },
    getPopupContainer: { type: Function },
    prefixCls: String,
    getPrefixCls: { type: Function },
    renderEmpty: { type: Function },
    transformCellText: { type: Function },
    csp: He(),
    input: He(),
    autoInsertSpaceInButton: { type: Boolean, default: void 0 },
    locale: He(),
    pageHeader: He(),
    componentSize: { type: String },
    componentDisabled: { type: Boolean, default: void 0 },
    direction: { type: String, default: 'ltr' },
    space: He(),
    virtual: { type: Boolean, default: void 0 },
    dropdownMatchSelectWidth: { type: [Number, Boolean], default: !0 },
    form: He(),
    pagination: He(),
    theme: He(),
    select: He(),
    wave: He(),
  }),
  ls = Symbol('configProvider'),
  Vc = {
    getPrefixCls: (e, t) => t || (e ? `ant-${e}` : 'ant'),
    iconPrefixCls: L(() => as),
    getPopupContainer: L(() => () => document.body),
    direction: L(() => 'ltr'),
  },
  Uc = () => Ee(ls, Vc),
  $h = (e) => Ot(ls, e),
  Gc = Symbol('DisabledContextKey'),
  Kc = () => Ee(Gc, qe(void 0)),
  Ph = (e) => {
    const t = Kc()
    return (
      Ot(
        Gc,
        L(() => {
          var n
          return (n = e.value) !== null && n !== void 0 ? n : t.value
        })
      ),
      e
    )
  },
  Eh = {
    items_per_page: '/ page',
    jump_to: 'Go to',
    jump_to_confirm: 'confirm',
    page: '',
    prev_page: 'Previous Page',
    next_page: 'Next Page',
    prev_5: 'Previous 5 Pages',
    next_5: 'Next 5 Pages',
    prev_3: 'Previous 3 Pages',
    next_3: 'Next 3 Pages',
  },
  Ah = {
    locale: 'en_US',
    today: 'Today',
    now: 'Now',
    backToToday: 'Back to today',
    ok: 'Ok',
    clear: 'Clear',
    month: 'Month',
    year: 'Year',
    timeSelect: 'select time',
    dateSelect: 'select date',
    weekSelect: 'Choose a week',
    monthSelect: 'Choose a month',
    yearSelect: 'Choose a year',
    decadeSelect: 'Choose a decade',
    yearFormat: 'YYYY',
    dateFormat: 'M/D/YYYY',
    dayFormat: 'D',
    dateTimeFormat: 'M/D/YYYY HH:mm:ss',
    monthBeforeYear: !0,
    previousMonth: 'Previous month (PageUp)',
    nextMonth: 'Next month (PageDown)',
    previousYear: 'Last year (Control + left)',
    nextYear: 'Next year (Control + right)',
    previousDecade: 'Last decade',
    nextDecade: 'Next decade',
    previousCentury: 'Last century',
    nextCentury: 'Next century',
  },
  Xc = { placeholder: 'Select time', rangePlaceholder: ['Start time', 'End time'] },
  ya = {
    lang: T(
      {
        placeholder: 'Select date',
        yearPlaceholder: 'Select year',
        quarterPlaceholder: 'Select quarter',
        monthPlaceholder: 'Select month',
        weekPlaceholder: 'Select week',
        rangePlaceholder: ['Start date', 'End date'],
        rangeYearPlaceholder: ['Start year', 'End year'],
        rangeQuarterPlaceholder: ['Start quarter', 'End quarter'],
        rangeMonthPlaceholder: ['Start month', 'End month'],
        rangeWeekPlaceholder: ['Start week', 'End week'],
      },
      Ah
    ),
    timePickerLocale: T({}, Xc),
  },
  Re = '${label} is not a valid ${type}',
  xn = {
    locale: 'en',
    Pagination: Eh,
    DatePicker: ya,
    TimePicker: Xc,
    Calendar: ya,
    global: { placeholder: 'Please select' },
    Table: {
      filterTitle: 'Filter menu',
      filterConfirm: 'OK',
      filterReset: 'Reset',
      filterEmptyText: 'No filters',
      filterCheckall: 'Select all items',
      filterSearchPlaceholder: 'Search in filters',
      emptyText: 'No data',
      selectAll: 'Select current page',
      selectInvert: 'Invert current page',
      selectNone: 'Clear all data',
      selectionAll: 'Select all data',
      sortTitle: 'Sort',
      expand: 'Expand row',
      collapse: 'Collapse row',
      triggerDesc: 'Click to sort descending',
      triggerAsc: 'Click to sort ascending',
      cancelSort: 'Click to cancel sorting',
    },
    Tour: { Next: 'Next', Previous: 'Previous', Finish: 'Finish' },
    Modal: { okText: 'OK', cancelText: 'Cancel', justOkText: 'OK' },
    Popconfirm: { okText: 'OK', cancelText: 'Cancel' },
    Transfer: {
      titles: ['', ''],
      searchPlaceholder: 'Search here',
      itemUnit: 'item',
      itemsUnit: 'items',
      remove: 'Remove',
      selectCurrent: 'Select current page',
      removeCurrent: 'Remove current page',
      selectAll: 'Select all data',
      removeAll: 'Remove all data',
      selectInvert: 'Invert current page',
    },
    Upload: {
      uploading: 'Uploading...',
      removeFile: 'Remove file',
      uploadError: 'Upload error',
      previewFile: 'Preview file',
      downloadFile: 'Download file',
    },
    Empty: { description: 'No data' },
    Icon: { icon: 'icon' },
    Text: { edit: 'Edit', copy: 'Copy', copied: 'Copied', expand: 'Expand' },
    PageHeader: { back: 'Back' },
    Form: {
      optional: '(optional)',
      defaultValidateMessages: {
        default: 'Field validation error for ${label}',
        required: 'Please enter ${label}',
        enum: '${label} must be one of [${enum}]',
        whitespace: '${label} cannot be a blank character',
        date: {
          format: '${label} date format is invalid',
          parse: '${label} cannot be converted to a date',
          invalid: '${label} is an invalid date',
        },
        types: {
          string: Re,
          method: Re,
          array: Re,
          object: Re,
          number: Re,
          date: Re,
          boolean: Re,
          integer: Re,
          float: Re,
          regexp: Re,
          email: Re,
          url: Re,
          hex: Re,
        },
        string: {
          len: '${label} must be ${len} characters',
          min: '${label} must be at least ${min} characters',
          max: '${label} must be up to ${max} characters',
          range: '${label} must be between ${min}-${max} characters',
        },
        number: {
          len: '${label} must be equal to ${len}',
          min: '${label} must be minimum ${min}',
          max: '${label} must be maximum ${max}',
          range: '${label} must be between ${min}-${max}',
        },
        array: {
          len: 'Must be ${len} ${label}',
          min: 'At least ${min} ${label}',
          max: 'At most ${max} ${label}',
          range: 'The amount of ${label} must be between ${min}-${max}',
        },
        pattern: { mismatch: '${label} does not match the pattern ${pattern}' },
      },
    },
    Image: { preview: 'Preview' },
    QRCode: { expired: 'QR code expired', refresh: 'Refresh', scanned: 'Scanned' },
  },
  qc = be({
    compatConfig: { MODE: 3 },
    name: 'LocaleReceiver',
    props: {
      componentName: String,
      defaultLocale: { type: [Object, Function] },
      children: { type: Function },
    },
    setup(e, t) {
      let { slots: n } = t
      const r = Ee('localeData', {}),
        o = L(() => {
          const { componentName: s = 'global', defaultLocale: a } = e,
            l = a || xn[s || 'global'],
            { antLocale: u } = r,
            c = s && u ? u[s] : {}
          return T(T({}, typeof l == 'function' ? l() : l), c || {})
        }),
        i = L(() => {
          const { antLocale: s } = r,
            a = s && s.locale
          return s && s.exist && !a ? xn.locale : a
        })
      return () => {
        const s = e.children || n.default,
          { antLocale: a } = r
        return s?.(o.value, i.value, a)
      }
    },
  })
function My(e, t, n) {
  const r = Ee('localeData', {})
  return [
    L(() => {
      const { antLocale: i } = r,
        s = Jt(t) || xn[e],
        a = i ? i[e] : {}
      return T(T(T({}, typeof s == 'function' ? s() : s), a || {}), Jt(n) || {})
    }),
  ]
}
function cs(e) {
  for (var t = 0, n, r = 0, o = e.length; o >= 4; ++r, o -= 4)
    ((n =
      (e.charCodeAt(r) & 255) |
      ((e.charCodeAt(++r) & 255) << 8) |
      ((e.charCodeAt(++r) & 255) << 16) |
      ((e.charCodeAt(++r) & 255) << 24)),
      (n = (n & 65535) * 1540483477 + (((n >>> 16) * 59797) << 16)),
      (n ^= n >>> 24),
      (t =
        ((n & 65535) * 1540483477 + (((n >>> 16) * 59797) << 16)) ^
        ((t & 65535) * 1540483477 + (((t >>> 16) * 59797) << 16))))
  switch (o) {
    case 3:
      t ^= (e.charCodeAt(r + 2) & 255) << 16
    case 2:
      t ^= (e.charCodeAt(r + 1) & 255) << 8
    case 1:
      ;((t ^= e.charCodeAt(r) & 255), (t = (t & 65535) * 1540483477 + (((t >>> 16) * 59797) << 16)))
  }
  return (
    (t ^= t >>> 13),
    (t = (t & 65535) * 1540483477 + (((t >>> 16) * 59797) << 16)),
    ((t ^ (t >>> 15)) >>> 0).toString(36)
  )
}
const ba = '%'
class Mh {
  constructor(t) {
    ;((this.cache = new Map()), (this.instanceId = t))
  }
  get(t) {
    return this.cache.get(Array.isArray(t) ? t.join(ba) : t) || null
  }
  update(t, n) {
    const r = Array.isArray(t) ? t.join(ba) : t,
      o = this.cache.get(r),
      i = n(o)
    i === null ? this.cache.delete(r) : this.cache.set(r, i)
  }
}
const Yc = 'data-token-hash',
  Xt = 'data-css-hash',
  fn = '__cssinjs_instance__'
function lr() {
  const e = Math.random().toString(12).slice(2)
  if (typeof document < 'u' && document.head && document.body) {
    const t = document.body.querySelectorAll(`style[${Xt}]`) || [],
      { firstChild: n } = document.head
    Array.from(t).forEach((o) => {
      ;((o[fn] = o[fn] || e), o[fn] === e && document.head.insertBefore(o, n))
    })
    const r = {}
    Array.from(document.querySelectorAll(`style[${Xt}]`)).forEach((o) => {
      var i
      const s = o.getAttribute(Xt)
      r[s]
        ? o[fn] === e && ((i = o.parentNode) === null || i === void 0 || i.removeChild(o))
        : (r[s] = !0)
    })
  }
  return new Mh(e)
}
const Jc = Symbol('StyleContextKey'),
  Ih = () => {
    var e, t, n
    const r = Lt()
    let o
    if (r && r.appContext) {
      const i =
        (n =
          (t = (e = r.appContext) === null || e === void 0 ? void 0 : e.config) === null ||
          t === void 0
            ? void 0
            : t.globalProperties) === null || n === void 0
          ? void 0
          : n.__ANTDV_CSSINJS_CACHE__
      i
        ? (o = i)
        : ((o = lr()),
          r.appContext.config.globalProperties &&
            (r.appContext.config.globalProperties.__ANTDV_CSSINJS_CACHE__ = o))
    } else o = lr()
    return o
  },
  Qc = { cache: lr(), defaultCache: !0, hashPriority: 'low' },
  Co = () => {
    const e = Ih()
    return Ee(Jc, We(T(T({}, Qc), { cache: e })))
  },
  jh = (e) => {
    const t = Co(),
      n = We(T(T({}, Qc), { cache: lr() }))
    return (
      Fe(
        [() => Jt(e), t],
        () => {
          const r = T({}, t.value),
            o = Jt(e)
          Object.keys(o).forEach((s) => {
            const a = o[s]
            o[s] !== void 0 && (r[s] = a)
          })
          const { cache: i } = o
          ;((r.cache = r.cache || lr()),
            (r.defaultCache = !i && t.value.defaultCache),
            (n.value = r))
        },
        { immediate: !0 }
      ),
      Ot(Jc, n),
      n
    )
  },
  Rh = () => ({
    autoClear: Vo(),
    mock: va(),
    cache: He(),
    defaultCache: Vo(),
    hashPriority: va(),
    container: _h(),
    ssrInline: Vo(),
    transformers: ma(),
    linters: ma(),
  })
ss(
  be({
    name: 'AStyleProvider',
    inheritAttrs: !1,
    props: Rh(),
    setup(e, t) {
      let { slots: n } = t
      return (
        jh(e),
        () => {
          var r
          return (r = n.default) === null || r === void 0 ? void 0 : r.call(n)
        }
      )
    },
  })
)
function Zc(e, t, n, r) {
  const o = Co(),
    i = We(''),
    s = We()
  mo(() => {
    i.value = [e, ...t.value].join('%')
  })
  const a = (l) => {
    o.value.cache.update(l, (u) => {
      const [c = 0, f] = u || []
      return c - 1 === 0 ? (r?.(f, !1), null) : [c - 1, f]
    })
  }
  return (
    Fe(
      i,
      (l, u) => {
        ;(u && a(u),
          o.value.cache.update(l, (c) => {
            const [f = 0, d] = c || [],
              m = d || n()
            return [f + 1, m]
          }),
          (s.value = o.value.cache.get(i.value)[1]))
      },
      { immediate: !0 }
    ),
    Yi(() => {
      a(i.value)
    }),
    s
  )
}
function En() {
  return !!(typeof window < 'u' && window.document && window.document.createElement)
}
function Lh(e, t) {
  return e && e.contains ? e.contains(t) : !1
}
const Ca = 'data-vc-order',
  Hh = 'vc-util-key',
  bi = new Map()
function eu() {
  let { mark: e } = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {}
  return e ? (e.startsWith('data-') ? e : `data-${e}`) : Hh
}
function xo(e) {
  return e.attachTo ? e.attachTo : document.querySelector('head') || document.body
}
function Fh(e) {
  return e === 'queue' ? 'prependQueue' : e ? 'prepend' : 'append'
}
function tu(e) {
  return Array.from((bi.get(e) || e).children).filter((t) => t.tagName === 'STYLE')
}
function nu(e) {
  let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}
  if (!En()) return null
  const { csp: n, prepend: r } = t,
    o = document.createElement('style')
  ;(o.setAttribute(Ca, Fh(r)), n?.nonce && (o.nonce = n?.nonce), (o.innerHTML = e))
  const i = xo(t),
    { firstChild: s } = i
  if (r) {
    if (r === 'queue') {
      const a = tu(i).filter((l) => ['prepend', 'prependQueue'].includes(l.getAttribute(Ca)))
      if (a.length) return (i.insertBefore(o, a[a.length - 1].nextSibling), o)
    }
    i.insertBefore(o, s)
  } else i.appendChild(o)
  return o
}
function ru(e) {
  let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}
  const n = xo(t)
  return tu(n).find((r) => r.getAttribute(eu(t)) === e)
}
function ou(e) {
  let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}
  const n = ru(e, t)
  n && xo(t).removeChild(n)
}
function kh(e, t) {
  const n = bi.get(e)
  if (!n || !Lh(document, n)) {
    const r = nu('', t),
      { parentNode: o } = r
    ;(bi.set(e, o), e.removeChild(r))
  }
}
function eo(e, t) {
  let n = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : {}
  var r, o, i
  const s = xo(n)
  kh(s, n)
  const a = ru(t, n)
  if (a)
    return (
      !((r = n.csp) === null || r === void 0) &&
        r.nonce &&
        a.nonce !== ((o = n.csp) === null || o === void 0 ? void 0 : o.nonce) &&
        (a.nonce = (i = n.csp) === null || i === void 0 ? void 0 : i.nonce),
      a.innerHTML !== e && (a.innerHTML = e),
      a
    )
  const l = nu(e, n)
  return (l.setAttribute(eu(n), t), l)
}
function Nh(e, t) {
  if (e.length !== t.length) return !1
  for (let n = 0; n < e.length; n++) if (e[n] !== t[n]) return !1
  return !0
}
class Sn {
  constructor() {
    ;((this.cache = new Map()), (this.keys = []), (this.cacheCallTimes = 0))
  }
  size() {
    return this.keys.length
  }
  internalGet(t) {
    let n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1,
      r = { map: this.cache }
    return (
      t.forEach((o) => {
        var i
        r ? (r = (i = r?.map) === null || i === void 0 ? void 0 : i.get(o)) : (r = void 0)
      }),
      r?.value && n && (r.value[1] = this.cacheCallTimes++),
      r?.value
    )
  }
  get(t) {
    var n
    return (n = this.internalGet(t, !0)) === null || n === void 0 ? void 0 : n[0]
  }
  has(t) {
    return !!this.internalGet(t)
  }
  set(t, n) {
    if (!this.has(t)) {
      if (this.size() + 1 > Sn.MAX_CACHE_SIZE + Sn.MAX_CACHE_OFFSET) {
        const [o] = this.keys.reduce(
          (i, s) => {
            const [, a] = i
            return this.internalGet(s)[1] < a ? [s, this.internalGet(s)[1]] : i
          },
          [this.keys[0], this.cacheCallTimes]
        )
        this.delete(o)
      }
      this.keys.push(t)
    }
    let r = this.cache
    t.forEach((o, i) => {
      if (i === t.length - 1) r.set(o, { value: [n, this.cacheCallTimes++] })
      else {
        const s = r.get(o)
        ;(s ? s.map || (s.map = new Map()) : r.set(o, { map: new Map() }), (r = r.get(o).map))
      }
    })
  }
  deleteByPath(t, n) {
    var r
    const o = t.get(n[0])
    if (n.length === 1)
      return (
        o.map ? t.set(n[0], { map: o.map }) : t.delete(n[0]),
        (r = o.value) === null || r === void 0 ? void 0 : r[0]
      )
    const i = this.deleteByPath(o.map, n.slice(1))
    return ((!o.map || o.map.size === 0) && !o.value && t.delete(n[0]), i)
  }
  delete(t) {
    if (this.has(t))
      return ((this.keys = this.keys.filter((n) => !Nh(n, t))), this.deleteByPath(this.cache, t))
  }
}
Sn.MAX_CACHE_SIZE = 20
Sn.MAX_CACHE_OFFSET = 5
function Dh() {}
let iu = Dh,
  xa = 0
class su {
  constructor(t) {
    ;((this.derivatives = Array.isArray(t) ? t : [t]),
      (this.id = xa),
      t.length === 0 && iu(t.length > 0),
      (xa += 1))
  }
  getDerivativeToken(t) {
    return this.derivatives.reduce((n, r) => r(t, n), void 0)
  }
}
const Uo = new Sn()
function au(e) {
  const t = Array.isArray(e) ? e : [e]
  return (Uo.has(t) || Uo.set(t, new su(t)), Uo.get(t))
}
const Sa = new WeakMap()
function to(e) {
  let t = Sa.get(e) || ''
  return (
    t ||
      (Object.keys(e).forEach((n) => {
        const r = e[n]
        ;((t += n),
          r instanceof su ? (t += r.id) : r && typeof r == 'object' ? (t += to(r)) : (t += r))
      }),
      Sa.set(e, t)),
    t
  )
}
function Bh(e, t) {
  return cs(`${t}_${to(e)}`)
}
const Zn = `random-${Date.now()}-${Math.random()}`.replace(/\./g, ''),
  lu = '_bAmBoO_'
function zh(e, t, n) {
  var r, o
  if (En()) {
    eo(e, Zn)
    const i = document.createElement('div')
    ;((i.style.position = 'fixed'),
      (i.style.left = '0'),
      (i.style.top = '0'),
      t?.(i),
      document.body.appendChild(i))
    const s = n
      ? n(i)
      : (r = getComputedStyle(i).content) === null || r === void 0
        ? void 0
        : r.includes(lu)
    return ((o = i.parentNode) === null || o === void 0 || o.removeChild(i), ou(Zn), s)
  }
  return !1
}
let Go
function Wh() {
  return (
    Go === void 0 &&
      (Go = zh(`@layer ${Zn} { .${Zn} { content: "${lu}"!important; } }`, (e) => {
        e.className = Zn
      })),
    Go
  )
}
const _a = {},
  Vh = 'css',
  Wt = new Map()
function Uh(e) {
  Wt.set(e, (Wt.get(e) || 0) + 1)
}
function Gh(e, t) {
  typeof document < 'u' &&
    document.querySelectorAll(`style[${Yc}="${e}"]`).forEach((r) => {
      var o
      r[fn] === t && ((o = r.parentNode) === null || o === void 0 || o.removeChild(r))
    })
}
const Kh = 0
function Xh(e, t) {
  Wt.set(e, (Wt.get(e) || 0) - 1)
  const n = Array.from(Wt.keys()),
    r = n.filter((o) => (Wt.get(o) || 0) <= 0)
  n.length - r.length > Kh &&
    r.forEach((o) => {
      ;(Gh(o, t), Wt.delete(o))
    })
}
const qh = (e, t, n, r) => {
  const o = n.getDerivativeToken(e)
  let i = T(T({}, o), t)
  return (r && (i = r(i)), i)
}
function Yh(e, t) {
  let n = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : qe({})
  const r = Co(),
    o = L(() => T({}, ...t.value)),
    i = L(() => to(o.value)),
    s = L(() => to(n.value.override || _a))
  return Zc(
    'token',
    L(() => [n.value.salt || '', e.value.id, i.value, s.value]),
    () => {
      const { salt: l = '', override: u = _a, formatToken: c, getComputedToken: f } = n.value,
        d = f ? f(o.value, u, e.value) : qh(o.value, u, e.value, c),
        p = Bh(d, l)
      ;((d._tokenKey = p), Uh(p))
      const m = `${Vh}-${cs(p)}`
      return ((d._hashId = m), [d, m])
    },
    (l) => {
      var u
      Xh(l[0]._tokenKey, (u = r.value) === null || u === void 0 ? void 0 : u.cache.instanceId)
    }
  )
}
var Jh = {
    animationIterationCount: 1,
    aspectRatio: 1,
    borderImageOutset: 1,
    borderImageSlice: 1,
    borderImageWidth: 1,
    boxFlex: 1,
    boxFlexGroup: 1,
    boxOrdinalGroup: 1,
    columnCount: 1,
    columns: 1,
    flex: 1,
    flexGrow: 1,
    flexPositive: 1,
    flexShrink: 1,
    flexNegative: 1,
    flexOrder: 1,
    gridRow: 1,
    gridRowEnd: 1,
    gridRowSpan: 1,
    gridRowStart: 1,
    gridColumn: 1,
    gridColumnEnd: 1,
    gridColumnSpan: 1,
    gridColumnStart: 1,
    msGridRow: 1,
    msGridRowSpan: 1,
    msGridColumn: 1,
    msGridColumnSpan: 1,
    fontWeight: 1,
    lineHeight: 1,
    opacity: 1,
    order: 1,
    orphans: 1,
    tabSize: 1,
    widows: 1,
    zIndex: 1,
    zoom: 1,
    WebkitLineClamp: 1,
    fillOpacity: 1,
    floodOpacity: 1,
    stopOpacity: 1,
    strokeDasharray: 1,
    strokeDashoffset: 1,
    strokeMiterlimit: 1,
    strokeOpacity: 1,
    strokeWidth: 1,
  },
  cu = 'comm',
  uu = 'rule',
  fu = 'decl',
  Qh = '@import',
  Zh = '@namespace',
  eg = '@keyframes',
  tg = '@layer',
  du = Math.abs,
  us = String.fromCharCode
function pu(e) {
  return e.trim()
}
function Lr(e, t, n) {
  return e.replace(t, n)
}
function ng(e, t, n) {
  return e.indexOf(t, n)
}
function vn(e, t) {
  return e.charCodeAt(t) | 0
}
function _n(e, t, n) {
  return e.slice(t, n)
}
function st(e) {
  return e.length
}
function rg(e) {
  return e.length
}
function Or(e, t) {
  return (t.push(e), e)
}
var So = 1,
  wn = 1,
  hu = 0,
  Ue = 0,
  fe = 0,
  An = ''
function fs(e, t, n, r, o, i, s, a) {
  return {
    value: e,
    root: t,
    parent: n,
    type: r,
    props: o,
    children: i,
    line: So,
    column: wn,
    length: s,
    return: '',
    siblings: a,
  }
}
function og() {
  return fe
}
function ig() {
  return ((fe = Ue > 0 ? vn(An, --Ue) : 0), wn--, fe === 10 && ((wn = 1), So--), fe)
}
function Ye() {
  return ((fe = Ue < hu ? vn(An, Ue++) : 0), wn++, fe === 10 && ((wn = 1), So++), fe)
}
function Mt() {
  return vn(An, Ue)
}
function Hr() {
  return Ue
}
function _o(e, t) {
  return _n(An, e, t)
}
function cr(e) {
  switch (e) {
    case 0:
    case 9:
    case 10:
    case 13:
    case 32:
      return 5
    case 33:
    case 43:
    case 44:
    case 47:
    case 62:
    case 64:
    case 126:
    case 59:
    case 123:
    case 125:
      return 4
    case 58:
      return 3
    case 34:
    case 39:
    case 40:
    case 91:
      return 2
    case 41:
    case 93:
      return 1
  }
  return 0
}
function sg(e) {
  return ((So = wn = 1), (hu = st((An = e))), (Ue = 0), [])
}
function ag(e) {
  return ((An = ''), e)
}
function Ko(e) {
  return pu(_o(Ue - 1, Ci(e === 91 ? e + 2 : e === 40 ? e + 1 : e)))
}
function lg(e) {
  for (; (fe = Mt()) && fe < 33; ) Ye()
  return cr(e) > 2 || cr(fe) > 3 ? '' : ' '
}
function cg(e, t) {
  for (; --t && Ye() && !(fe < 48 || fe > 102 || (fe > 57 && fe < 65) || (fe > 70 && fe < 97)); );
  return _o(e, Hr() + (t < 6 && Mt() == 32 && Ye() == 32))
}
function Ci(e) {
  for (; Ye(); )
    switch (fe) {
      case e:
        return Ue
      case 34:
      case 39:
        e !== 34 && e !== 39 && Ci(fe)
        break
      case 40:
        e === 41 && Ci(e)
        break
      case 92:
        Ye()
        break
    }
  return Ue
}
function ug(e, t) {
  for (; Ye() && e + fe !== 57; ) if (e + fe === 84 && Mt() === 47) break
  return '/*' + _o(t, Ue - 1) + '*' + us(e === 47 ? e : Ye())
}
function fg(e) {
  for (; !cr(Mt()); ) Ye()
  return _o(e, Ue)
}
function dg(e) {
  return ag(Fr('', null, null, null, [''], (e = sg(e)), 0, [0], e))
}
function Fr(e, t, n, r, o, i, s, a, l) {
  for (
    var u = 0,
      c = 0,
      f = s,
      d = 0,
      p = 0,
      m = 0,
      v = 1,
      b = 1,
      C = 1,
      O = 0,
      P = '',
      x = o,
      _ = i,
      H = r,
      y = P;
    b;

  )
    switch (((m = O), (O = Ye()))) {
      case 40:
        if (m != 108 && vn(y, f - 1) == 58) {
          ng((y += Lr(Ko(O), '&', '&\f')), '&\f', du(u ? a[u - 1] : 0)) != -1 && (C = -1)
          break
        }
      case 34:
      case 39:
      case 91:
        y += Ko(O)
        break
      case 9:
      case 10:
      case 13:
      case 32:
        y += lg(m)
        break
      case 92:
        y += cg(Hr() - 1, 7)
        continue
      case 47:
        switch (Mt()) {
          case 42:
          case 47:
            ;(Or(pg(ug(Ye(), Hr()), t, n, l), l),
              (cr(m || 1) == 5 || cr(Mt() || 1) == 5) &&
                st(y) &&
                _n(y, -1, void 0) !== ' ' &&
                (y += ' '))
            break
          default:
            y += '/'
        }
        break
      case 123 * v:
        a[u++] = st(y) * C
      case 125 * v:
      case 59:
      case 0:
        switch (O) {
          case 0:
          case 125:
            b = 0
          case 59 + c:
            ;(C == -1 && (y = Lr(y, /\f/g, '')),
              p > 0 &&
                (st(y) - f || (v === 0 && m === 47)) &&
                Or(
                  p > 32 ? Oa(y + ';', r, n, f - 1, l) : Oa(Lr(y, ' ', '') + ';', r, n, f - 2, l),
                  l
                ))
            break
          case 59:
            y += ';'
          default:
            if ((Or((H = wa(y, t, n, u, c, o, a, P, (x = []), (_ = []), f, i)), i), O === 123))
              if (c === 0) Fr(y, t, H, H, x, i, f, a, _)
              else {
                switch (d) {
                  case 99:
                    if (vn(y, 3) === 110) break
                  case 108:
                    if (vn(y, 2) === 97) break
                  default:
                    c = 0
                  case 100:
                  case 109:
                  case 115:
                }
                c
                  ? Fr(
                      e,
                      H,
                      H,
                      r && Or(wa(e, H, H, 0, 0, o, a, P, o, (x = []), f, _), _),
                      o,
                      _,
                      f,
                      a,
                      r ? x : _
                    )
                  : Fr(y, H, H, H, [''], _, 0, a, _)
              }
        }
        ;((u = c = p = 0), (v = C = 1), (P = y = ''), (f = s))
        break
      case 58:
        ;((f = 1 + st(y)), (p = m))
      default:
        if (v < 1) {
          if (O == 123) --v
          else if (O == 125 && v++ == 0 && ig() == 125) continue
        }
        switch (((y += us(O)), O * v)) {
          case 38:
            C = c > 0 ? 1 : ((y += '\f'), -1)
            break
          case 44:
            ;((a[u++] = (st(y) - 1) * C), (C = 1))
            break
          case 64:
            ;(Mt() === 45 && (y += Ko(Ye())), (d = Mt()), (c = f = st((P = y += fg(Hr())))), O++)
            break
          case 45:
            m === 45 && st(y) == 2 && (v = 0)
        }
    }
  return i
}
function wa(e, t, n, r, o, i, s, a, l, u, c, f) {
  for (var d = o - 1, p = o === 0 ? i : [''], m = rg(p), v = 0, b = 0, C = 0; v < r; ++v)
    for (var O = 0, P = _n(e, d + 1, (d = du((b = s[v])))), x = e; O < m; ++O)
      (x = pu(b > 0 ? p[O] + ' ' + P : Lr(P, /&\f/g, p[O]))) && (l[C++] = x)
  return fs(e, t, n, o === 0 ? uu : a, l, u, c, f)
}
function pg(e, t, n, r) {
  return fs(e, t, n, cu, us(og()), _n(e, 2, -2), 0, r)
}
function Oa(e, t, n, r, o) {
  return fs(e, t, n, fu, _n(e, 0, r), _n(e, r + 1, -1), r, o)
}
function xi(e, t) {
  for (var n = '', r = 0; r < e.length; r++) n += t(e[r], r, e, t) || ''
  return n
}
function hg(e, t, n, r) {
  switch (e.type) {
    case tg:
      if (e.children.length) break
    case Qh:
    case Zh:
    case fu:
      return (e.return = e.return || e.value)
    case cu:
      return ''
    case eg:
      return (e.return = e.value + '{' + xi(e.children, r) + '}')
    case uu:
      if (!st((e.value = e.props.join(',')))) return ''
  }
  return st((n = xi(e.children, r))) ? (e.return = e.value + '{' + n + '}') : ''
}
const Ta = 'data-ant-cssinjs-cache-path',
  gg = '_FILE_STYLE__'
let qt,
  gu = !0
function mg() {
  var e
  if (!qt && ((qt = {}), En())) {
    const t = document.createElement('div')
    ;((t.className = Ta),
      (t.style.position = 'fixed'),
      (t.style.visibility = 'hidden'),
      (t.style.top = '-9999px'),
      document.body.appendChild(t))
    let n = getComputedStyle(t).content || ''
    ;((n = n.replace(/^"/, '').replace(/"$/, '')),
      n.split(';').forEach((o) => {
        const [i, s] = o.split(':')
        qt[i] = s
      }))
    const r = document.querySelector(`style[${Ta}]`)
    ;(r && ((gu = !1), (e = r.parentNode) === null || e === void 0 || e.removeChild(r)),
      document.body.removeChild(t))
  }
}
function vg(e) {
  return (mg(), !!qt[e])
}
function yg(e) {
  const t = qt[e]
  let n = null
  if (t && En())
    if (gu) n = gg
    else {
      const r = document.querySelector(`style[${Xt}="${qt[e]}"]`)
      r ? (n = r.innerHTML) : delete qt[e]
    }
  return [n, t]
}
const $a = En(),
  bg = '_skip_check_',
  mu = '_multi_value_'
function Pa(e) {
  return xi(dg(e), hg).replace(/\{%%%\:[^;];}/g, ';')
}
function Cg(e) {
  return typeof e == 'object' && e && (bg in e || mu in e)
}
function xg(e, t, n) {
  if (!t) return e
  const r = `.${t}`,
    o = n === 'low' ? `:where(${r})` : r
  return e
    .split(',')
    .map((s) => {
      var a
      const l = s.trim().split(/\s+/)
      let u = l[0] || ''
      const c = ((a = u.match(/^\w+/)) === null || a === void 0 ? void 0 : a[0]) || ''
      return ((u = `${c}${o}${u.slice(c.length)}`), [u, ...l.slice(1)].join(' '))
    })
    .join(',')
}
const Ea = new Set(),
  Si = function (e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {},
      {
        root: n,
        injectHash: r,
        parentSelectors: o,
      } = arguments.length > 2 && arguments[2] !== void 0
        ? arguments[2]
        : { root: !0, parentSelectors: [] }
    const {
      hashId: i,
      layer: s,
      path: a,
      hashPriority: l,
      transformers: u = [],
      linters: c = [],
    } = t
    let f = '',
      d = {}
    function p(b) {
      const C = b.getName(i)
      if (!d[C]) {
        const [O] = Si(b.style, t, { root: !1, parentSelectors: o })
        d[C] = `@keyframes ${b.getName(i)}${O}`
      }
    }
    function m(b) {
      let C = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : []
      return (
        b.forEach((O) => {
          Array.isArray(O) ? m(O, C) : O && C.push(O)
        }),
        C
      )
    }
    if (
      (m(Array.isArray(e) ? e : [e]).forEach((b) => {
        const C = typeof b == 'string' && !n ? {} : b
        if (typeof C == 'string')
          f += `${C}
`
        else if (C._keyframe) p(C)
        else {
          const O = u.reduce((P, x) => {
            var _
            return ((_ = x?.visit) === null || _ === void 0 ? void 0 : _.call(x, P)) || P
          }, C)
          Object.keys(O).forEach((P) => {
            var x
            const _ = O[P]
            if (typeof _ == 'object' && _ && (P !== 'animationName' || !_._keyframe) && !Cg(_)) {
              let H = !1,
                y = P.trim(),
                E = !1
              ;(n || r) && i
                ? y.startsWith('@')
                  ? (H = !0)
                  : (y = xg(P, i, l))
                : n && !i && (y === '&' || y === '') && ((y = ''), (E = !0))
              const [$, W] = Si(_, t, { root: E, injectHash: H, parentSelectors: [...o, y] })
              ;((d = T(T({}, d), W)), (f += `${y}${$}`))
            } else {
              let H = function (E, $) {
                const W = E.replace(/[A-Z]/g, (k) => `-${k.toLowerCase()}`)
                let Y = $
                ;(!Jh[E] && typeof Y == 'number' && Y !== 0 && (Y = `${Y}px`),
                  E === 'animationName' && $?._keyframe && (p($), (Y = $.getName(i))),
                  (f += `${W}:${Y};`))
              }
              const y = (x = _?.value) !== null && x !== void 0 ? x : _
              typeof _ == 'object' && _?.[mu] && Array.isArray(y)
                ? y.forEach((E) => {
                    H(P, E)
                  })
                : H(P, y)
            }
          })
        }
      }),
      !n)
    )
      f = `{${f}}`
    else if (s && Wh()) {
      const b = s.split(',')
      ;((f = `@layer ${b[b.length - 1].trim()} {${f}}`),
        b.length > 1 && (f = `@layer ${s}{%%%:%}${f}`))
    }
    return [f, d]
  }
function Sg(e, t) {
  return cs(`${e.join('%')}${t}`)
}
function _i(e, t) {
  const n = Co(),
    r = L(() => e.value.token._tokenKey),
    o = L(() => [r.value, ...e.value.path])
  let i = $a
  return (
    Zc(
      'style',
      o,
      () => {
        const { path: s, hashId: a, layer: l, nonce: u, clientOnly: c, order: f = 0 } = e.value,
          d = o.value.join('|')
        if (vg(d)) {
          const [y, E] = yg(d)
          if (y) return [y, r.value, E, {}, c, f]
        }
        const p = t(),
          { hashPriority: m, container: v, transformers: b, linters: C, cache: O } = n.value,
          [P, x] = Si(p, {
            hashId: a,
            hashPriority: m,
            layer: l,
            path: s.join('-'),
            transformers: b,
            linters: C,
          }),
          _ = Pa(P),
          H = Sg(o.value, _)
        if (i) {
          const y = { mark: Xt, prepend: 'queue', attachTo: v, priority: f },
            E = typeof u == 'function' ? u() : u
          E && (y.csp = { nonce: E })
          const $ = eo(_, H, y)
          ;(($[fn] = O.instanceId),
            $.setAttribute(Yc, r.value),
            Object.keys(x).forEach((W) => {
              Ea.has(W) ||
                (Ea.add(W),
                eo(Pa(x[W]), `_effect-${W}`, { mark: Xt, prepend: 'queue', attachTo: v }))
            }))
        }
        return [_, r.value, H, x, c, f]
      },
      (s, a) => {
        let [, , l] = s
        ;(a || n.value.autoClear) && $a && ou(l, { mark: Xt })
      }
    ),
    (s) => s
  )
}
class Yt {
  constructor(t, n) {
    ;((this._keyframe = !0), (this.name = t), (this.style = n))
  }
  getName() {
    let t = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : ''
    return t ? `${t}-${this.name}` : this.name
  }
}
const _g = '4.2.6'
function ye(e, t) {
  wg(e) && (e = '100%')
  var n = Og(e)
  return (
    (e = t === 360 ? e : Math.min(t, Math.max(0, parseFloat(e)))),
    n && (e = parseInt(String(e * t), 10) / 100),
    Math.abs(e - t) < 1e-6
      ? 1
      : (t === 360
          ? (e = (e < 0 ? (e % t) + t : e % t) / parseFloat(String(t)))
          : (e = (e % t) / parseFloat(String(t))),
        e)
  )
}
function Tr(e) {
  return Math.min(1, Math.max(0, e))
}
function wg(e) {
  return typeof e == 'string' && e.indexOf('.') !== -1 && parseFloat(e) === 1
}
function Og(e) {
  return typeof e == 'string' && e.indexOf('%') !== -1
}
function vu(e) {
  return ((e = parseFloat(e)), (isNaN(e) || e < 0 || e > 1) && (e = 1), e)
}
function $r(e) {
  return e <= 1 ? ''.concat(Number(e) * 100, '%') : e
}
function Ut(e) {
  return e.length === 1 ? '0' + e : String(e)
}
function Tg(e, t, n) {
  return { r: ye(e, 255) * 255, g: ye(t, 255) * 255, b: ye(n, 255) * 255 }
}
function Aa(e, t, n) {
  ;((e = ye(e, 255)), (t = ye(t, 255)), (n = ye(n, 255)))
  var r = Math.max(e, t, n),
    o = Math.min(e, t, n),
    i = 0,
    s = 0,
    a = (r + o) / 2
  if (r === o) ((s = 0), (i = 0))
  else {
    var l = r - o
    switch (((s = a > 0.5 ? l / (2 - r - o) : l / (r + o)), r)) {
      case e:
        i = (t - n) / l + (t < n ? 6 : 0)
        break
      case t:
        i = (n - e) / l + 2
        break
      case n:
        i = (e - t) / l + 4
        break
    }
    i /= 6
  }
  return { h: i, s, l: a }
}
function Xo(e, t, n) {
  return (
    n < 0 && (n += 1),
    n > 1 && (n -= 1),
    n < 1 / 6
      ? e + (t - e) * (6 * n)
      : n < 1 / 2
        ? t
        : n < 2 / 3
          ? e + (t - e) * (2 / 3 - n) * 6
          : e
  )
}
function $g(e, t, n) {
  var r, o, i
  if (((e = ye(e, 360)), (t = ye(t, 100)), (n = ye(n, 100)), t === 0)) ((o = n), (i = n), (r = n))
  else {
    var s = n < 0.5 ? n * (1 + t) : n + t - n * t,
      a = 2 * n - s
    ;((r = Xo(a, s, e + 1 / 3)), (o = Xo(a, s, e)), (i = Xo(a, s, e - 1 / 3)))
  }
  return { r: r * 255, g: o * 255, b: i * 255 }
}
function wi(e, t, n) {
  ;((e = ye(e, 255)), (t = ye(t, 255)), (n = ye(n, 255)))
  var r = Math.max(e, t, n),
    o = Math.min(e, t, n),
    i = 0,
    s = r,
    a = r - o,
    l = r === 0 ? 0 : a / r
  if (r === o) i = 0
  else {
    switch (r) {
      case e:
        i = (t - n) / a + (t < n ? 6 : 0)
        break
      case t:
        i = (n - e) / a + 2
        break
      case n:
        i = (e - t) / a + 4
        break
    }
    i /= 6
  }
  return { h: i, s: l, v: s }
}
function Pg(e, t, n) {
  ;((e = ye(e, 360) * 6), (t = ye(t, 100)), (n = ye(n, 100)))
  var r = Math.floor(e),
    o = e - r,
    i = n * (1 - t),
    s = n * (1 - o * t),
    a = n * (1 - (1 - o) * t),
    l = r % 6,
    u = [n, s, i, i, a, n][l],
    c = [a, n, n, s, i, i][l],
    f = [i, i, a, n, n, s][l]
  return { r: u * 255, g: c * 255, b: f * 255 }
}
function Oi(e, t, n, r) {
  var o = [
    Ut(Math.round(e).toString(16)),
    Ut(Math.round(t).toString(16)),
    Ut(Math.round(n).toString(16)),
  ]
  return r &&
    o[0].startsWith(o[0].charAt(1)) &&
    o[1].startsWith(o[1].charAt(1)) &&
    o[2].startsWith(o[2].charAt(1))
    ? o[0].charAt(0) + o[1].charAt(0) + o[2].charAt(0)
    : o.join('')
}
function Eg(e, t, n, r, o) {
  var i = [
    Ut(Math.round(e).toString(16)),
    Ut(Math.round(t).toString(16)),
    Ut(Math.round(n).toString(16)),
    Ut(Ag(r)),
  ]
  return o &&
    i[0].startsWith(i[0].charAt(1)) &&
    i[1].startsWith(i[1].charAt(1)) &&
    i[2].startsWith(i[2].charAt(1)) &&
    i[3].startsWith(i[3].charAt(1))
    ? i[0].charAt(0) + i[1].charAt(0) + i[2].charAt(0) + i[3].charAt(0)
    : i.join('')
}
function Ag(e) {
  return Math.round(parseFloat(e) * 255).toString(16)
}
function Ma(e) {
  return Le(e) / 255
}
function Le(e) {
  return parseInt(e, 16)
}
function Mg(e) {
  return { r: e >> 16, g: (e & 65280) >> 8, b: e & 255 }
}
var Ti = {
  aliceblue: '#f0f8ff',
  antiquewhite: '#faebd7',
  aqua: '#00ffff',
  aquamarine: '#7fffd4',
  azure: '#f0ffff',
  beige: '#f5f5dc',
  bisque: '#ffe4c4',
  black: '#000000',
  blanchedalmond: '#ffebcd',
  blue: '#0000ff',
  blueviolet: '#8a2be2',
  brown: '#a52a2a',
  burlywood: '#deb887',
  cadetblue: '#5f9ea0',
  chartreuse: '#7fff00',
  chocolate: '#d2691e',
  coral: '#ff7f50',
  cornflowerblue: '#6495ed',
  cornsilk: '#fff8dc',
  crimson: '#dc143c',
  cyan: '#00ffff',
  darkblue: '#00008b',
  darkcyan: '#008b8b',
  darkgoldenrod: '#b8860b',
  darkgray: '#a9a9a9',
  darkgreen: '#006400',
  darkgrey: '#a9a9a9',
  darkkhaki: '#bdb76b',
  darkmagenta: '#8b008b',
  darkolivegreen: '#556b2f',
  darkorange: '#ff8c00',
  darkorchid: '#9932cc',
  darkred: '#8b0000',
  darksalmon: '#e9967a',
  darkseagreen: '#8fbc8f',
  darkslateblue: '#483d8b',
  darkslategray: '#2f4f4f',
  darkslategrey: '#2f4f4f',
  darkturquoise: '#00ced1',
  darkviolet: '#9400d3',
  deeppink: '#ff1493',
  deepskyblue: '#00bfff',
  dimgray: '#696969',
  dimgrey: '#696969',
  dodgerblue: '#1e90ff',
  firebrick: '#b22222',
  floralwhite: '#fffaf0',
  forestgreen: '#228b22',
  fuchsia: '#ff00ff',
  gainsboro: '#dcdcdc',
  ghostwhite: '#f8f8ff',
  goldenrod: '#daa520',
  gold: '#ffd700',
  gray: '#808080',
  green: '#008000',
  greenyellow: '#adff2f',
  grey: '#808080',
  honeydew: '#f0fff0',
  hotpink: '#ff69b4',
  indianred: '#cd5c5c',
  indigo: '#4b0082',
  ivory: '#fffff0',
  khaki: '#f0e68c',
  lavenderblush: '#fff0f5',
  lavender: '#e6e6fa',
  lawngreen: '#7cfc00',
  lemonchiffon: '#fffacd',
  lightblue: '#add8e6',
  lightcoral: '#f08080',
  lightcyan: '#e0ffff',
  lightgoldenrodyellow: '#fafad2',
  lightgray: '#d3d3d3',
  lightgreen: '#90ee90',
  lightgrey: '#d3d3d3',
  lightpink: '#ffb6c1',
  lightsalmon: '#ffa07a',
  lightseagreen: '#20b2aa',
  lightskyblue: '#87cefa',
  lightslategray: '#778899',
  lightslategrey: '#778899',
  lightsteelblue: '#b0c4de',
  lightyellow: '#ffffe0',
  lime: '#00ff00',
  limegreen: '#32cd32',
  linen: '#faf0e6',
  magenta: '#ff00ff',
  maroon: '#800000',
  mediumaquamarine: '#66cdaa',
  mediumblue: '#0000cd',
  mediumorchid: '#ba55d3',
  mediumpurple: '#9370db',
  mediumseagreen: '#3cb371',
  mediumslateblue: '#7b68ee',
  mediumspringgreen: '#00fa9a',
  mediumturquoise: '#48d1cc',
  mediumvioletred: '#c71585',
  midnightblue: '#191970',
  mintcream: '#f5fffa',
  mistyrose: '#ffe4e1',
  moccasin: '#ffe4b5',
  navajowhite: '#ffdead',
  navy: '#000080',
  oldlace: '#fdf5e6',
  olive: '#808000',
  olivedrab: '#6b8e23',
  orange: '#ffa500',
  orangered: '#ff4500',
  orchid: '#da70d6',
  palegoldenrod: '#eee8aa',
  palegreen: '#98fb98',
  paleturquoise: '#afeeee',
  palevioletred: '#db7093',
  papayawhip: '#ffefd5',
  peachpuff: '#ffdab9',
  peru: '#cd853f',
  pink: '#ffc0cb',
  plum: '#dda0dd',
  powderblue: '#b0e0e6',
  purple: '#800080',
  rebeccapurple: '#663399',
  red: '#ff0000',
  rosybrown: '#bc8f8f',
  royalblue: '#4169e1',
  saddlebrown: '#8b4513',
  salmon: '#fa8072',
  sandybrown: '#f4a460',
  seagreen: '#2e8b57',
  seashell: '#fff5ee',
  sienna: '#a0522d',
  silver: '#c0c0c0',
  skyblue: '#87ceeb',
  slateblue: '#6a5acd',
  slategray: '#708090',
  slategrey: '#708090',
  snow: '#fffafa',
  springgreen: '#00ff7f',
  steelblue: '#4682b4',
  tan: '#d2b48c',
  teal: '#008080',
  thistle: '#d8bfd8',
  tomato: '#ff6347',
  turquoise: '#40e0d0',
  violet: '#ee82ee',
  wheat: '#f5deb3',
  white: '#ffffff',
  whitesmoke: '#f5f5f5',
  yellow: '#ffff00',
  yellowgreen: '#9acd32',
}
function ln(e) {
  var t = { r: 0, g: 0, b: 0 },
    n = 1,
    r = null,
    o = null,
    i = null,
    s = !1,
    a = !1
  return (
    typeof e == 'string' && (e = Rg(e)),
    typeof e == 'object' &&
      (pt(e.r) && pt(e.g) && pt(e.b)
        ? ((t = Tg(e.r, e.g, e.b)), (s = !0), (a = String(e.r).substr(-1) === '%' ? 'prgb' : 'rgb'))
        : pt(e.h) && pt(e.s) && pt(e.v)
          ? ((r = $r(e.s)), (o = $r(e.v)), (t = Pg(e.h, r, o)), (s = !0), (a = 'hsv'))
          : pt(e.h) &&
            pt(e.s) &&
            pt(e.l) &&
            ((r = $r(e.s)), (i = $r(e.l)), (t = $g(e.h, r, i)), (s = !0), (a = 'hsl')),
      Object.prototype.hasOwnProperty.call(e, 'a') && (n = e.a)),
    (n = vu(n)),
    {
      ok: s,
      format: e.format || a,
      r: Math.min(255, Math.max(t.r, 0)),
      g: Math.min(255, Math.max(t.g, 0)),
      b: Math.min(255, Math.max(t.b, 0)),
      a: n,
    }
  )
}
var Ig = '[-\\+]?\\d+%?',
  jg = '[-\\+]?\\d*\\.\\d+%?',
  It = '(?:'.concat(jg, ')|(?:').concat(Ig, ')'),
  qo = '[\\s|\\(]+('.concat(It, ')[,|\\s]+(').concat(It, ')[,|\\s]+(').concat(It, ')\\s*\\)?'),
  Yo = '[\\s|\\(]+('
    .concat(It, ')[,|\\s]+(')
    .concat(It, ')[,|\\s]+(')
    .concat(It, ')[,|\\s]+(')
    .concat(It, ')\\s*\\)?'),
  Ke = {
    CSS_UNIT: new RegExp(It),
    rgb: new RegExp('rgb' + qo),
    rgba: new RegExp('rgba' + Yo),
    hsl: new RegExp('hsl' + qo),
    hsla: new RegExp('hsla' + Yo),
    hsv: new RegExp('hsv' + qo),
    hsva: new RegExp('hsva' + Yo),
    hex3: /^#?([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$/,
    hex6: /^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$/,
    hex4: /^#?([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$/,
    hex8: /^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$/,
  }
function Rg(e) {
  if (((e = e.trim().toLowerCase()), e.length === 0)) return !1
  var t = !1
  if (Ti[e]) ((e = Ti[e]), (t = !0))
  else if (e === 'transparent') return { r: 0, g: 0, b: 0, a: 0, format: 'name' }
  var n = Ke.rgb.exec(e)
  return n
    ? { r: n[1], g: n[2], b: n[3] }
    : ((n = Ke.rgba.exec(e)),
      n
        ? { r: n[1], g: n[2], b: n[3], a: n[4] }
        : ((n = Ke.hsl.exec(e)),
          n
            ? { h: n[1], s: n[2], l: n[3] }
            : ((n = Ke.hsla.exec(e)),
              n
                ? { h: n[1], s: n[2], l: n[3], a: n[4] }
                : ((n = Ke.hsv.exec(e)),
                  n
                    ? { h: n[1], s: n[2], v: n[3] }
                    : ((n = Ke.hsva.exec(e)),
                      n
                        ? { h: n[1], s: n[2], v: n[3], a: n[4] }
                        : ((n = Ke.hex8.exec(e)),
                          n
                            ? {
                                r: Le(n[1]),
                                g: Le(n[2]),
                                b: Le(n[3]),
                                a: Ma(n[4]),
                                format: t ? 'name' : 'hex8',
                              }
                            : ((n = Ke.hex6.exec(e)),
                              n
                                ? {
                                    r: Le(n[1]),
                                    g: Le(n[2]),
                                    b: Le(n[3]),
                                    format: t ? 'name' : 'hex',
                                  }
                                : ((n = Ke.hex4.exec(e)),
                                  n
                                    ? {
                                        r: Le(n[1] + n[1]),
                                        g: Le(n[2] + n[2]),
                                        b: Le(n[3] + n[3]),
                                        a: Ma(n[4] + n[4]),
                                        format: t ? 'name' : 'hex8',
                                      }
                                    : ((n = Ke.hex3.exec(e)),
                                      n
                                        ? {
                                            r: Le(n[1] + n[1]),
                                            g: Le(n[2] + n[2]),
                                            b: Le(n[3] + n[3]),
                                            format: t ? 'name' : 'hex',
                                          }
                                        : !1)))))))))
}
function pt(e) {
  return !!Ke.CSS_UNIT.exec(String(e))
}
var ve = (function () {
    function e(t, n) {
      ;(t === void 0 && (t = ''), n === void 0 && (n = {}))
      var r
      if (t instanceof e) return t
      ;(typeof t == 'number' && (t = Mg(t)), (this.originalInput = t))
      var o = ln(t)
      ;((this.originalInput = t),
        (this.r = o.r),
        (this.g = o.g),
        (this.b = o.b),
        (this.a = o.a),
        (this.roundA = Math.round(100 * this.a) / 100),
        (this.format = (r = n.format) !== null && r !== void 0 ? r : o.format),
        (this.gradientType = n.gradientType),
        this.r < 1 && (this.r = Math.round(this.r)),
        this.g < 1 && (this.g = Math.round(this.g)),
        this.b < 1 && (this.b = Math.round(this.b)),
        (this.isValid = o.ok))
    }
    return (
      (e.prototype.isDark = function () {
        return this.getBrightness() < 128
      }),
      (e.prototype.isLight = function () {
        return !this.isDark()
      }),
      (e.prototype.getBrightness = function () {
        var t = this.toRgb()
        return (t.r * 299 + t.g * 587 + t.b * 114) / 1e3
      }),
      (e.prototype.getLuminance = function () {
        var t = this.toRgb(),
          n,
          r,
          o,
          i = t.r / 255,
          s = t.g / 255,
          a = t.b / 255
        return (
          i <= 0.03928 ? (n = i / 12.92) : (n = Math.pow((i + 0.055) / 1.055, 2.4)),
          s <= 0.03928 ? (r = s / 12.92) : (r = Math.pow((s + 0.055) / 1.055, 2.4)),
          a <= 0.03928 ? (o = a / 12.92) : (o = Math.pow((a + 0.055) / 1.055, 2.4)),
          0.2126 * n + 0.7152 * r + 0.0722 * o
        )
      }),
      (e.prototype.getAlpha = function () {
        return this.a
      }),
      (e.prototype.setAlpha = function (t) {
        return ((this.a = vu(t)), (this.roundA = Math.round(100 * this.a) / 100), this)
      }),
      (e.prototype.isMonochrome = function () {
        var t = this.toHsl().s
        return t === 0
      }),
      (e.prototype.toHsv = function () {
        var t = wi(this.r, this.g, this.b)
        return { h: t.h * 360, s: t.s, v: t.v, a: this.a }
      }),
      (e.prototype.toHsvString = function () {
        var t = wi(this.r, this.g, this.b),
          n = Math.round(t.h * 360),
          r = Math.round(t.s * 100),
          o = Math.round(t.v * 100)
        return this.a === 1
          ? 'hsv('.concat(n, ', ').concat(r, '%, ').concat(o, '%)')
          : 'hsva('.concat(n, ', ').concat(r, '%, ').concat(o, '%, ').concat(this.roundA, ')')
      }),
      (e.prototype.toHsl = function () {
        var t = Aa(this.r, this.g, this.b)
        return { h: t.h * 360, s: t.s, l: t.l, a: this.a }
      }),
      (e.prototype.toHslString = function () {
        var t = Aa(this.r, this.g, this.b),
          n = Math.round(t.h * 360),
          r = Math.round(t.s * 100),
          o = Math.round(t.l * 100)
        return this.a === 1
          ? 'hsl('.concat(n, ', ').concat(r, '%, ').concat(o, '%)')
          : 'hsla('.concat(n, ', ').concat(r, '%, ').concat(o, '%, ').concat(this.roundA, ')')
      }),
      (e.prototype.toHex = function (t) {
        return (t === void 0 && (t = !1), Oi(this.r, this.g, this.b, t))
      }),
      (e.prototype.toHexString = function (t) {
        return (t === void 0 && (t = !1), '#' + this.toHex(t))
      }),
      (e.prototype.toHex8 = function (t) {
        return (t === void 0 && (t = !1), Eg(this.r, this.g, this.b, this.a, t))
      }),
      (e.prototype.toHex8String = function (t) {
        return (t === void 0 && (t = !1), '#' + this.toHex8(t))
      }),
      (e.prototype.toHexShortString = function (t) {
        return (t === void 0 && (t = !1), this.a === 1 ? this.toHexString(t) : this.toHex8String(t))
      }),
      (e.prototype.toRgb = function () {
        return { r: Math.round(this.r), g: Math.round(this.g), b: Math.round(this.b), a: this.a }
      }),
      (e.prototype.toRgbString = function () {
        var t = Math.round(this.r),
          n = Math.round(this.g),
          r = Math.round(this.b)
        return this.a === 1
          ? 'rgb('.concat(t, ', ').concat(n, ', ').concat(r, ')')
          : 'rgba('.concat(t, ', ').concat(n, ', ').concat(r, ', ').concat(this.roundA, ')')
      }),
      (e.prototype.toPercentageRgb = function () {
        var t = function (n) {
          return ''.concat(Math.round(ye(n, 255) * 100), '%')
        }
        return { r: t(this.r), g: t(this.g), b: t(this.b), a: this.a }
      }),
      (e.prototype.toPercentageRgbString = function () {
        var t = function (n) {
          return Math.round(ye(n, 255) * 100)
        }
        return this.a === 1
          ? 'rgb('.concat(t(this.r), '%, ').concat(t(this.g), '%, ').concat(t(this.b), '%)')
          : 'rgba('
              .concat(t(this.r), '%, ')
              .concat(t(this.g), '%, ')
              .concat(t(this.b), '%, ')
              .concat(this.roundA, ')')
      }),
      (e.prototype.toName = function () {
        if (this.a === 0) return 'transparent'
        if (this.a < 1) return !1
        for (
          var t = '#' + Oi(this.r, this.g, this.b, !1), n = 0, r = Object.entries(Ti);
          n < r.length;
          n++
        ) {
          var o = r[n],
            i = o[0],
            s = o[1]
          if (t === s) return i
        }
        return !1
      }),
      (e.prototype.toString = function (t) {
        var n = !!t
        t = t ?? this.format
        var r = !1,
          o = this.a < 1 && this.a >= 0,
          i = !n && o && (t.startsWith('hex') || t === 'name')
        return i
          ? t === 'name' && this.a === 0
            ? this.toName()
            : this.toRgbString()
          : (t === 'rgb' && (r = this.toRgbString()),
            t === 'prgb' && (r = this.toPercentageRgbString()),
            (t === 'hex' || t === 'hex6') && (r = this.toHexString()),
            t === 'hex3' && (r = this.toHexString(!0)),
            t === 'hex4' && (r = this.toHex8String(!0)),
            t === 'hex8' && (r = this.toHex8String()),
            t === 'name' && (r = this.toName()),
            t === 'hsl' && (r = this.toHslString()),
            t === 'hsv' && (r = this.toHsvString()),
            r || this.toHexString())
      }),
      (e.prototype.toNumber = function () {
        return (Math.round(this.r) << 16) + (Math.round(this.g) << 8) + Math.round(this.b)
      }),
      (e.prototype.clone = function () {
        return new e(this.toString())
      }),
      (e.prototype.lighten = function (t) {
        t === void 0 && (t = 10)
        var n = this.toHsl()
        return ((n.l += t / 100), (n.l = Tr(n.l)), new e(n))
      }),
      (e.prototype.brighten = function (t) {
        t === void 0 && (t = 10)
        var n = this.toRgb()
        return (
          (n.r = Math.max(0, Math.min(255, n.r - Math.round(255 * -(t / 100))))),
          (n.g = Math.max(0, Math.min(255, n.g - Math.round(255 * -(t / 100))))),
          (n.b = Math.max(0, Math.min(255, n.b - Math.round(255 * -(t / 100))))),
          new e(n)
        )
      }),
      (e.prototype.darken = function (t) {
        t === void 0 && (t = 10)
        var n = this.toHsl()
        return ((n.l -= t / 100), (n.l = Tr(n.l)), new e(n))
      }),
      (e.prototype.tint = function (t) {
        return (t === void 0 && (t = 10), this.mix('white', t))
      }),
      (e.prototype.shade = function (t) {
        return (t === void 0 && (t = 10), this.mix('black', t))
      }),
      (e.prototype.desaturate = function (t) {
        t === void 0 && (t = 10)
        var n = this.toHsl()
        return ((n.s -= t / 100), (n.s = Tr(n.s)), new e(n))
      }),
      (e.prototype.saturate = function (t) {
        t === void 0 && (t = 10)
        var n = this.toHsl()
        return ((n.s += t / 100), (n.s = Tr(n.s)), new e(n))
      }),
      (e.prototype.greyscale = function () {
        return this.desaturate(100)
      }),
      (e.prototype.spin = function (t) {
        var n = this.toHsl(),
          r = (n.h + t) % 360
        return ((n.h = r < 0 ? 360 + r : r), new e(n))
      }),
      (e.prototype.mix = function (t, n) {
        n === void 0 && (n = 50)
        var r = this.toRgb(),
          o = new e(t).toRgb(),
          i = n / 100,
          s = {
            r: (o.r - r.r) * i + r.r,
            g: (o.g - r.g) * i + r.g,
            b: (o.b - r.b) * i + r.b,
            a: (o.a - r.a) * i + r.a,
          }
        return new e(s)
      }),
      (e.prototype.analogous = function (t, n) {
        ;(t === void 0 && (t = 6), n === void 0 && (n = 30))
        var r = this.toHsl(),
          o = 360 / n,
          i = [this]
        for (r.h = (r.h - ((o * t) >> 1) + 720) % 360; --t; )
          ((r.h = (r.h + o) % 360), i.push(new e(r)))
        return i
      }),
      (e.prototype.complement = function () {
        var t = this.toHsl()
        return ((t.h = (t.h + 180) % 360), new e(t))
      }),
      (e.prototype.monochromatic = function (t) {
        t === void 0 && (t = 6)
        for (var n = this.toHsv(), r = n.h, o = n.s, i = n.v, s = [], a = 1 / t; t--; )
          (s.push(new e({ h: r, s: o, v: i })), (i = (i + a) % 1))
        return s
      }),
      (e.prototype.splitcomplement = function () {
        var t = this.toHsl(),
          n = t.h
        return [
          this,
          new e({ h: (n + 72) % 360, s: t.s, l: t.l }),
          new e({ h: (n + 216) % 360, s: t.s, l: t.l }),
        ]
      }),
      (e.prototype.onBackground = function (t) {
        var n = this.toRgb(),
          r = new e(t).toRgb(),
          o = n.a + r.a * (1 - n.a)
        return new e({
          r: (n.r * n.a + r.r * r.a * (1 - n.a)) / o,
          g: (n.g * n.a + r.g * r.a * (1 - n.a)) / o,
          b: (n.b * n.a + r.b * r.a * (1 - n.a)) / o,
          a: o,
        })
      }),
      (e.prototype.triad = function () {
        return this.polyad(3)
      }),
      (e.prototype.tetrad = function () {
        return this.polyad(4)
      }),
      (e.prototype.polyad = function (t) {
        for (var n = this.toHsl(), r = n.h, o = [this], i = 360 / t, s = 1; s < t; s++)
          o.push(new e({ h: (r + s * i) % 360, s: n.s, l: n.l }))
        return o
      }),
      (e.prototype.equals = function (t) {
        return this.toRgbString() === new e(t).toRgbString()
      }),
      e
    )
  })(),
  Pr = 2,
  Ia = 0.16,
  Lg = 0.05,
  Hg = 0.05,
  Fg = 0.15,
  yu = 5,
  bu = 4,
  kg = [
    { index: 7, opacity: 0.15 },
    { index: 6, opacity: 0.25 },
    { index: 5, opacity: 0.3 },
    { index: 5, opacity: 0.45 },
    { index: 5, opacity: 0.65 },
    { index: 5, opacity: 0.85 },
    { index: 4, opacity: 0.9 },
    { index: 3, opacity: 0.95 },
    { index: 2, opacity: 0.97 },
    { index: 1, opacity: 0.98 },
  ]
function ja(e) {
  var t = e.r,
    n = e.g,
    r = e.b,
    o = wi(t, n, r)
  return { h: o.h * 360, s: o.s, v: o.v }
}
function Er(e) {
  var t = e.r,
    n = e.g,
    r = e.b
  return '#'.concat(Oi(t, n, r, !1))
}
function Ng(e, t, n) {
  var r = n / 100,
    o = { r: (t.r - e.r) * r + e.r, g: (t.g - e.g) * r + e.g, b: (t.b - e.b) * r + e.b }
  return o
}
function Ra(e, t, n) {
  var r
  return (
    Math.round(e.h) >= 60 && Math.round(e.h) <= 240
      ? (r = n ? Math.round(e.h) - Pr * t : Math.round(e.h) + Pr * t)
      : (r = n ? Math.round(e.h) + Pr * t : Math.round(e.h) - Pr * t),
    r < 0 ? (r += 360) : r >= 360 && (r -= 360),
    r
  )
}
function La(e, t, n) {
  if (e.h === 0 && e.s === 0) return e.s
  var r
  return (
    n ? (r = e.s - Ia * t) : t === bu ? (r = e.s + Ia) : (r = e.s + Lg * t),
    r > 1 && (r = 1),
    n && t === yu && r > 0.1 && (r = 0.1),
    r < 0.06 && (r = 0.06),
    Number(r.toFixed(2))
  )
}
function Ha(e, t, n) {
  var r
  return (n ? (r = e.v + Hg * t) : (r = e.v - Fg * t), r > 1 && (r = 1), Number(r.toFixed(2)))
}
function en(e) {
  for (
    var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {},
      n = [],
      r = ln(e),
      o = yu;
    o > 0;
    o -= 1
  ) {
    var i = ja(r),
      s = Er(ln({ h: Ra(i, o, !0), s: La(i, o, !0), v: Ha(i, o, !0) }))
    n.push(s)
  }
  n.push(Er(r))
  for (var a = 1; a <= bu; a += 1) {
    var l = ja(r),
      u = Er(ln({ h: Ra(l, a), s: La(l, a), v: Ha(l, a) }))
    n.push(u)
  }
  return t.theme === 'dark'
    ? kg.map(function (c) {
        var f = c.index,
          d = c.opacity,
          p = Er(Ng(ln(t.backgroundColor || '#141414'), ln(n[f]), d * 100))
        return p
      })
    : n
}
var Jo = {
    red: '#F5222D',
    volcano: '#FA541C',
    orange: '#FA8C16',
    gold: '#FAAD14',
    yellow: '#FADB14',
    lime: '#A0D911',
    green: '#52C41A',
    cyan: '#13C2C2',
    blue: '#1890FF',
    geekblue: '#2F54EB',
    purple: '#722ED1',
    magenta: '#EB2F96',
    grey: '#666666',
  },
  kr = {},
  Qo = {}
Object.keys(Jo).forEach(function (e) {
  ;((kr[e] = en(Jo[e])),
    (kr[e].primary = kr[e][5]),
    (Qo[e] = en(Jo[e], { theme: 'dark', backgroundColor: '#141414' })),
    (Qo[e].primary = Qo[e][5]))
})
var Dg = kr.blue
const Bg = (e) => {
  const { controlHeight: t } = e
  return { controlHeightSM: t * 0.75, controlHeightXS: t * 0.5, controlHeightLG: t * 1.25 }
}
function zg(e) {
  const { sizeUnit: t, sizeStep: n } = e
  return {
    sizeXXL: t * (n + 8),
    sizeXL: t * (n + 4),
    sizeLG: t * (n + 2),
    sizeMD: t * (n + 1),
    sizeMS: t * n,
    size: t * n,
    sizeSM: t * (n - 1),
    sizeXS: t * (n - 2),
    sizeXXS: t * (n - 3),
  }
}
const Cu = {
    blue: '#1677ff',
    purple: '#722ED1',
    cyan: '#13C2C2',
    green: '#52C41A',
    magenta: '#EB2F96',
    pink: '#eb2f96',
    red: '#F5222D',
    orange: '#FA8C16',
    yellow: '#FADB14',
    volcano: '#FA541C',
    geekblue: '#2F54EB',
    gold: '#FAAD14',
    lime: '#A0D911',
  },
  wo = T(T({}, Cu), {
    colorPrimary: '#1677ff',
    colorSuccess: '#52c41a',
    colorWarning: '#faad14',
    colorError: '#ff4d4f',
    colorInfo: '#1677ff',
    colorTextBase: '',
    colorBgBase: '',
    fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
    fontSize: 14,
    lineWidth: 1,
    lineType: 'solid',
    motionUnit: 0.1,
    motionBase: 0,
    motionEaseOutCirc: 'cubic-bezier(0.08, 0.82, 0.17, 1)',
    motionEaseInOutCirc: 'cubic-bezier(0.78, 0.14, 0.15, 0.86)',
    motionEaseOut: 'cubic-bezier(0.215, 0.61, 0.355, 1)',
    motionEaseInOut: 'cubic-bezier(0.645, 0.045, 0.355, 1)',
    motionEaseOutBack: 'cubic-bezier(0.12, 0.4, 0.29, 1.46)',
    motionEaseInBack: 'cubic-bezier(0.71, -0.46, 0.88, 0.6)',
    motionEaseInQuint: 'cubic-bezier(0.755, 0.05, 0.855, 0.06)',
    motionEaseOutQuint: 'cubic-bezier(0.23, 1, 0.32, 1)',
    borderRadius: 6,
    sizeUnit: 4,
    sizeStep: 4,
    sizePopupArrow: 16,
    controlHeight: 32,
    zIndexBase: 0,
    zIndexPopupBase: 1e3,
    opacityImage: 1,
    wireframe: !1,
  })
function Wg(e, t) {
  let { generateColorPalettes: n, generateNeutralColorPalettes: r } = t
  const {
      colorSuccess: o,
      colorWarning: i,
      colorError: s,
      colorInfo: a,
      colorPrimary: l,
      colorBgBase: u,
      colorTextBase: c,
    } = e,
    f = n(l),
    d = n(o),
    p = n(i),
    m = n(s),
    v = n(a),
    b = r(u, c)
  return T(T({}, b), {
    colorPrimaryBg: f[1],
    colorPrimaryBgHover: f[2],
    colorPrimaryBorder: f[3],
    colorPrimaryBorderHover: f[4],
    colorPrimaryHover: f[5],
    colorPrimary: f[6],
    colorPrimaryActive: f[7],
    colorPrimaryTextHover: f[8],
    colorPrimaryText: f[9],
    colorPrimaryTextActive: f[10],
    colorSuccessBg: d[1],
    colorSuccessBgHover: d[2],
    colorSuccessBorder: d[3],
    colorSuccessBorderHover: d[4],
    colorSuccessHover: d[4],
    colorSuccess: d[6],
    colorSuccessActive: d[7],
    colorSuccessTextHover: d[8],
    colorSuccessText: d[9],
    colorSuccessTextActive: d[10],
    colorErrorBg: m[1],
    colorErrorBgHover: m[2],
    colorErrorBorder: m[3],
    colorErrorBorderHover: m[4],
    colorErrorHover: m[5],
    colorError: m[6],
    colorErrorActive: m[7],
    colorErrorTextHover: m[8],
    colorErrorText: m[9],
    colorErrorTextActive: m[10],
    colorWarningBg: p[1],
    colorWarningBgHover: p[2],
    colorWarningBorder: p[3],
    colorWarningBorderHover: p[4],
    colorWarningHover: p[4],
    colorWarning: p[6],
    colorWarningActive: p[7],
    colorWarningTextHover: p[8],
    colorWarningText: p[9],
    colorWarningTextActive: p[10],
    colorInfoBg: v[1],
    colorInfoBgHover: v[2],
    colorInfoBorder: v[3],
    colorInfoBorderHover: v[4],
    colorInfoHover: v[4],
    colorInfo: v[6],
    colorInfoActive: v[7],
    colorInfoTextHover: v[8],
    colorInfoText: v[9],
    colorInfoTextActive: v[10],
    colorBgMask: new ve('#000').setAlpha(0.45).toRgbString(),
    colorWhite: '#fff',
  })
}
const Vg = (e) => {
  let t = e,
    n = e,
    r = e,
    o = e
  return (
    e < 6 && e >= 5 ? (t = e + 1) : e < 16 && e >= 6 ? (t = e + 2) : e >= 16 && (t = 16),
    e < 7 && e >= 5
      ? (n = 4)
      : e < 8 && e >= 7
        ? (n = 5)
        : e < 14 && e >= 8
          ? (n = 6)
          : e < 16 && e >= 14
            ? (n = 7)
            : e >= 16 && (n = 8),
    e < 6 && e >= 2 ? (r = 1) : e >= 6 && (r = 2),
    e > 4 && e < 8 ? (o = 4) : e >= 8 && (o = 6),
    {
      borderRadius: e > 16 ? 16 : e,
      borderRadiusXS: r,
      borderRadiusSM: n,
      borderRadiusLG: t,
      borderRadiusOuter: o,
    }
  )
}
function Ug(e) {
  const { motionUnit: t, motionBase: n, borderRadius: r, lineWidth: o } = e
  return T(
    {
      motionDurationFast: `${(n + t).toFixed(1)}s`,
      motionDurationMid: `${(n + t * 2).toFixed(1)}s`,
      motionDurationSlow: `${(n + t * 3).toFixed(1)}s`,
      lineWidthBold: o + 1,
    },
    Vg(r)
  )
}
const ht = (e, t) => new ve(e).setAlpha(t).toRgbString(),
  Bn = (e, t) => new ve(e).darken(t).toHexString(),
  Gg = (e) => {
    const t = en(e)
    return {
      1: t[0],
      2: t[1],
      3: t[2],
      4: t[3],
      5: t[4],
      6: t[5],
      7: t[6],
      8: t[4],
      9: t[5],
      10: t[6],
    }
  },
  Kg = (e, t) => {
    const n = e || '#fff',
      r = t || '#000'
    return {
      colorBgBase: n,
      colorTextBase: r,
      colorText: ht(r, 0.88),
      colorTextSecondary: ht(r, 0.65),
      colorTextTertiary: ht(r, 0.45),
      colorTextQuaternary: ht(r, 0.25),
      colorFill: ht(r, 0.15),
      colorFillSecondary: ht(r, 0.06),
      colorFillTertiary: ht(r, 0.04),
      colorFillQuaternary: ht(r, 0.02),
      colorBgLayout: Bn(n, 4),
      colorBgContainer: Bn(n, 0),
      colorBgElevated: Bn(n, 0),
      colorBgSpotlight: ht(r, 0.85),
      colorBorder: Bn(n, 15),
      colorBorderSecondary: Bn(n, 6),
    }
  }
function Xg(e) {
  const t = new Array(10).fill(null).map((n, r) => {
    const o = r - 1,
      i = e * Math.pow(2.71828, o / 5),
      s = r > 1 ? Math.floor(i) : Math.ceil(i)
    return Math.floor(s / 2) * 2
  })
  return (
    (t[1] = e),
    t.map((n) => {
      const r = n + 8
      return { size: n, lineHeight: r / n }
    })
  )
}
const qg = (e) => {
  const t = Xg(e),
    n = t.map((o) => o.size),
    r = t.map((o) => o.lineHeight)
  return {
    fontSizeSM: n[0],
    fontSize: n[1],
    fontSizeLG: n[2],
    fontSizeXL: n[3],
    fontSizeHeading1: n[6],
    fontSizeHeading2: n[5],
    fontSizeHeading3: n[4],
    fontSizeHeading4: n[3],
    fontSizeHeading5: n[2],
    lineHeight: r[1],
    lineHeightLG: r[2],
    lineHeightSM: r[0],
    lineHeightHeading1: r[6],
    lineHeightHeading2: r[5],
    lineHeightHeading3: r[4],
    lineHeightHeading4: r[3],
    lineHeightHeading5: r[2],
  }
}
function Yg(e) {
  const t = Object.keys(Cu)
    .map((n) => {
      const r = en(e[n])
      return new Array(10).fill(1).reduce((o, i, s) => ((o[`${n}-${s + 1}`] = r[s]), o), {})
    })
    .reduce((n, r) => ((n = T(T({}, n), r)), n), {})
  return T(
    T(
      T(
        T(
          T(T(T({}, e), t), Wg(e, { generateColorPalettes: Gg, generateNeutralColorPalettes: Kg })),
          qg(e.fontSize)
        ),
        zg(e)
      ),
      Bg(e)
    ),
    Ug(e)
  )
}
function Zo(e) {
  return e >= 0 && e <= 255
}
function Ar(e, t) {
  const { r: n, g: r, b: o, a: i } = new ve(e).toRgb()
  if (i < 1) return e
  const { r: s, g: a, b: l } = new ve(t).toRgb()
  for (let u = 0.01; u <= 1; u += 0.01) {
    const c = Math.round((n - s * (1 - u)) / u),
      f = Math.round((r - a * (1 - u)) / u),
      d = Math.round((o - l * (1 - u)) / u)
    if (Zo(c) && Zo(f) && Zo(d))
      return new ve({ r: c, g: f, b: d, a: Math.round(u * 100) / 100 }).toRgbString()
  }
  return new ve({ r: n, g: r, b: o, a: 1 }).toRgbString()
}
var Jg = function (e, t) {
  var n = {}
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
  if (e != null && typeof Object.getOwnPropertySymbols == 'function')
    for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
      t.indexOf(r[o]) < 0 &&
        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
        (n[r[o]] = e[r[o]])
  return n
}
function Qg(e) {
  const { override: t } = e,
    n = Jg(e, ['override']),
    r = T({}, t)
  Object.keys(wo).forEach((p) => {
    delete r[p]
  })
  const o = T(T({}, n), r),
    i = 480,
    s = 576,
    a = 768,
    l = 992,
    u = 1200,
    c = 1600,
    f = 2e3
  return T(
    T(T({}, o), {
      colorLink: o.colorInfoText,
      colorLinkHover: o.colorInfoHover,
      colorLinkActive: o.colorInfoActive,
      colorFillContent: o.colorFillSecondary,
      colorFillContentHover: o.colorFill,
      colorFillAlter: o.colorFillQuaternary,
      colorBgContainerDisabled: o.colorFillTertiary,
      colorBorderBg: o.colorBgContainer,
      colorSplit: Ar(o.colorBorderSecondary, o.colorBgContainer),
      colorTextPlaceholder: o.colorTextQuaternary,
      colorTextDisabled: o.colorTextQuaternary,
      colorTextHeading: o.colorText,
      colorTextLabel: o.colorTextSecondary,
      colorTextDescription: o.colorTextTertiary,
      colorTextLightSolid: o.colorWhite,
      colorHighlight: o.colorError,
      colorBgTextHover: o.colorFillSecondary,
      colorBgTextActive: o.colorFill,
      colorIcon: o.colorTextTertiary,
      colorIconHover: o.colorText,
      colorErrorOutline: Ar(o.colorErrorBg, o.colorBgContainer),
      colorWarningOutline: Ar(o.colorWarningBg, o.colorBgContainer),
      fontSizeIcon: o.fontSizeSM,
      lineWidth: o.lineWidth,
      controlOutlineWidth: o.lineWidth * 2,
      controlInteractiveSize: o.controlHeight / 2,
      controlItemBgHover: o.colorFillTertiary,
      controlItemBgActive: o.colorPrimaryBg,
      controlItemBgActiveHover: o.colorPrimaryBgHover,
      controlItemBgActiveDisabled: o.colorFill,
      controlTmpOutline: o.colorFillQuaternary,
      controlOutline: Ar(o.colorPrimaryBg, o.colorBgContainer),
      lineType: o.lineType,
      borderRadius: o.borderRadius,
      borderRadiusXS: o.borderRadiusXS,
      borderRadiusSM: o.borderRadiusSM,
      borderRadiusLG: o.borderRadiusLG,
      fontWeightStrong: 600,
      opacityLoading: 0.65,
      linkDecoration: 'none',
      linkHoverDecoration: 'none',
      linkFocusDecoration: 'none',
      controlPaddingHorizontal: 12,
      controlPaddingHorizontalSM: 8,
      paddingXXS: o.sizeXXS,
      paddingXS: o.sizeXS,
      paddingSM: o.sizeSM,
      padding: o.size,
      paddingMD: o.sizeMD,
      paddingLG: o.sizeLG,
      paddingXL: o.sizeXL,
      paddingContentHorizontalLG: o.sizeLG,
      paddingContentVerticalLG: o.sizeMS,
      paddingContentHorizontal: o.sizeMS,
      paddingContentVertical: o.sizeSM,
      paddingContentHorizontalSM: o.size,
      paddingContentVerticalSM: o.sizeXS,
      marginXXS: o.sizeXXS,
      marginXS: o.sizeXS,
      marginSM: o.sizeSM,
      margin: o.size,
      marginMD: o.sizeMD,
      marginLG: o.sizeLG,
      marginXL: o.sizeXL,
      marginXXL: o.sizeXXL,
      boxShadow: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
      boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
      boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
      screenXS: i,
      screenXSMin: i,
      screenXSMax: s - 1,
      screenSM: s,
      screenSMMin: s,
      screenSMMax: a - 1,
      screenMD: a,
      screenMDMin: a,
      screenMDMax: l - 1,
      screenLG: l,
      screenLGMin: l,
      screenLGMax: u - 1,
      screenXL: u,
      screenXLMin: u,
      screenXLMax: c - 1,
      screenXXL: c,
      screenXXLMin: c,
      screenXXLMax: f - 1,
      screenXXXL: f,
      screenXXXLMin: f,
      boxShadowPopoverArrow: '3px 3px 7px rgba(0, 0, 0, 0.1)',
      boxShadowCard: `
      0 1px 2px -2px ${new ve('rgba(0, 0, 0, 0.16)').toRgbString()},
      0 3px 6px 0 ${new ve('rgba(0, 0, 0, 0.12)').toRgbString()},
      0 5px 12px 4px ${new ve('rgba(0, 0, 0, 0.09)').toRgbString()}
    `,
      boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
      boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
      boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
      boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
      boxShadowTabsOverflowLeft: 'inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)',
      boxShadowTabsOverflowRight: 'inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)',
      boxShadowTabsOverflowTop: 'inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)',
      boxShadowTabsOverflowBottom: 'inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)',
    }),
    r
  )
}
const xu = (e) => ({
    boxSizing: 'border-box',
    margin: 0,
    padding: 0,
    color: e.colorText,
    fontSize: e.fontSize,
    lineHeight: e.lineHeight,
    listStyle: 'none',
    fontFamily: e.fontFamily,
  }),
  Zg = () => ({
    display: 'inline-flex',
    alignItems: 'center',
    color: 'inherit',
    fontStyle: 'normal',
    lineHeight: 0,
    textAlign: 'center',
    textTransform: 'none',
    verticalAlign: '-0.125em',
    textRendering: 'optimizeLegibility',
    '-webkit-font-smoothing': 'antialiased',
    '-moz-osx-font-smoothing': 'grayscale',
    '> *': { lineHeight: 1 },
    svg: { display: 'inline-block' },
  }),
  Iy = () => ({
    '&::before': { display: 'table', content: '""' },
    '&::after': { display: 'table', clear: 'both', content: '""' },
  }),
  e0 = (e) => ({
    a: {
      color: e.colorLink,
      textDecoration: e.linkDecoration,
      backgroundColor: 'transparent',
      outline: 'none',
      cursor: 'pointer',
      transition: `color ${e.motionDurationSlow}`,
      '-webkit-text-decoration-skip': 'objects',
      '&:hover': { color: e.colorLinkHover },
      '&:active': { color: e.colorLinkActive },
      '&:active,\n  &:hover': { textDecoration: e.linkHoverDecoration, outline: 0 },
      '&:focus': { textDecoration: e.linkFocusDecoration, outline: 0 },
      '&[disabled]': { color: e.colorTextDisabled, cursor: 'not-allowed' },
    },
  }),
  t0 = (e, t) => {
    const { fontFamily: n, fontSize: r } = e,
      o = `[class^="${t}"], [class*=" ${t}"]`
    return {
      [o]: {
        fontFamily: n,
        fontSize: r,
        boxSizing: 'border-box',
        '&::before, &::after': { boxSizing: 'border-box' },
        [o]: { boxSizing: 'border-box', '&::before, &::after': { boxSizing: 'border-box' } },
      },
    }
  },
  n0 = (e) => ({
    outline: `${e.lineWidthBold}px solid ${e.colorPrimaryBorder}`,
    outlineOffset: 1,
    transition: 'outline-offset 0s, outline 0s',
  }),
  jy = (e) => ({ '&:focus-visible': T({}, n0(e)) })
function ds(e, t, n) {
  return (r) => {
    const o = L(() => r?.value),
      [i, s, a] = To(),
      { getPrefixCls: l, iconPrefixCls: u } = Uc(),
      c = L(() => l()),
      f = L(() => ({ theme: i.value, token: s.value, hashId: a.value, path: ['Shared', c.value] }))
    _i(f, () => [{ '&': e0(s.value) }])
    const d = L(() => ({
      theme: i.value,
      token: s.value,
      hashId: a.value,
      path: [e, o.value, u.value],
    }))
    return [
      _i(d, () => {
        const { token: p, flush: m } = o0(s.value),
          v = typeof n == 'function' ? n(p) : n,
          b = T(T({}, v), s.value[e]),
          C = `.${o.value}`,
          O = Oo(
            p,
            { componentCls: C, prefixCls: o.value, iconCls: `.${u.value}`, antCls: `.${c.value}` },
            b
          ),
          P = t(O, {
            hashId: a.value,
            prefixCls: o.value,
            rootPrefixCls: c.value,
            iconPrefixCls: u.value,
            overrideComponentToken: s.value[e],
          })
        return (m(e, b), [t0(s.value, o.value), P])
      }),
      a,
    ]
  }
}
const Su = typeof CSSINJS_STATISTIC < 'u'
let $i = !0
function Oo() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++) t[n] = arguments[n]
  if (!Su) return T({}, ...t)
  $i = !1
  const r = {}
  return (
    t.forEach((o) => {
      Object.keys(o).forEach((s) => {
        Object.defineProperty(r, s, { configurable: !0, enumerable: !0, get: () => o[s] })
      })
    }),
    ($i = !0),
    r
  )
}
function r0() {}
function o0(e) {
  let t,
    n = e,
    r = r0
  return (
    Su &&
      ((t = new Set()),
      (n = new Proxy(e, {
        get(o, i) {
          return ($i && t.add(i), o[i])
        },
      })),
      (r = (o, i) => {
        Array.from(t)
      })),
    { token: n, keys: t, flush: r }
  )
}
const i0 = au(Yg),
  _u = { token: wo, hashed: !0 },
  wu = Symbol('DesignTokenContext'),
  Pi = We(),
  s0 = (e) => {
    ;(Ot(wu, e),
      Fe(
        e,
        () => {
          ;((Pi.value = Jt(e)), rd(Pi))
        },
        { immediate: !0, deep: !0 }
      ))
  },
  a0 = be({
    props: { value: He() },
    setup(e, t) {
      let { slots: n } = t
      return (
        s0(L(() => e.value)),
        () => {
          var r
          return (r = n.default) === null || r === void 0 ? void 0 : r.call(n)
        }
      )
    },
  })
function To() {
  const e = Ee(
      wu,
      L(() => Pi.value || _u)
    ),
    t = L(() => `${_g}-${e.value.hashed || ''}`),
    n = L(() => e.value.theme || i0),
    r = Yh(
      n,
      L(() => [wo, e.value.token]),
      L(() => ({
        salt: t.value,
        override: T({ override: e.value.token }, e.value.components),
        formatToken: Qg,
      }))
    )
  return [n, L(() => r.value[0]), L(() => (e.value.hashed ? r.value[1] : ''))]
}
const ps = be({
  compatConfig: { MODE: 3 },
  setup() {
    const [, e] = To(),
      t = L(() => (new ve(e.value.colorBgBase).toHsl().l < 0.5 ? { opacity: 0.65 } : {}))
    return () =>
      w(
        'svg',
        {
          style: t.value,
          width: '184',
          height: '152',
          viewBox: '0 0 184 152',
          xmlns: 'http://www.w3.org/2000/svg',
        },
        [
          w('g', { fill: 'none', 'fill-rule': 'evenodd' }, [
            w('g', { transform: 'translate(24 31.67)' }, [
              w(
                'ellipse',
                {
                  'fill-opacity': '.8',
                  fill: '#F5F5F7',
                  cx: '67.797',
                  cy: '106.89',
                  rx: '67.797',
                  ry: '12.668',
                },
                null
              ),
              w(
                'path',
                {
                  d: 'M122.034 69.674L98.109 40.229c-1.148-1.386-2.826-2.225-4.593-2.225h-51.44c-1.766 0-3.444.839-4.592 2.225L13.56 69.674v15.383h108.475V69.674z',
                  fill: '#AEB8C2',
                },
                null
              ),
              w(
                'path',
                {
                  d: 'M101.537 86.214L80.63 61.102c-1.001-1.207-2.507-1.867-4.048-1.867H31.724c-1.54 0-3.047.66-4.048 1.867L6.769 86.214v13.792h94.768V86.214z',
                  fill: 'url(#linearGradient-1)',
                  transform: 'translate(13.56)',
                },
                null
              ),
              w(
                'path',
                {
                  d: 'M33.83 0h67.933a4 4 0 0 1 4 4v93.344a4 4 0 0 1-4 4H33.83a4 4 0 0 1-4-4V4a4 4 0 0 1 4-4z',
                  fill: '#F5F5F7',
                },
                null
              ),
              w(
                'path',
                {
                  d: 'M42.678 9.953h50.237a2 2 0 0 1 2 2V36.91a2 2 0 0 1-2 2H42.678a2 2 0 0 1-2-2V11.953a2 2 0 0 1 2-2zM42.94 49.767h49.713a2.262 2.262 0 1 1 0 4.524H42.94a2.262 2.262 0 0 1 0-4.524zM42.94 61.53h49.713a2.262 2.262 0 1 1 0 4.525H42.94a2.262 2.262 0 0 1 0-4.525zM121.813 105.032c-.775 3.071-3.497 5.36-6.735 5.36H20.515c-3.238 0-5.96-2.29-6.734-5.36a7.309 7.309 0 0 1-.222-1.79V69.675h26.318c2.907 0 5.25 2.448 5.25 5.42v.04c0 2.971 2.37 5.37 5.277 5.37h34.785c2.907 0 5.277-2.421 5.277-5.393V75.1c0-2.972 2.343-5.426 5.25-5.426h26.318v33.569c0 .617-.077 1.216-.221 1.789z',
                  fill: '#DCE0E6',
                },
                null
              ),
            ]),
            w(
              'path',
              {
                d: 'M149.121 33.292l-6.83 2.65a1 1 0 0 1-1.317-1.23l1.937-6.207c-2.589-2.944-4.109-6.534-4.109-10.408C138.802 8.102 148.92 0 161.402 0 173.881 0 184 8.102 184 18.097c0 9.995-10.118 18.097-22.599 18.097-4.528 0-8.744-1.066-12.28-2.902z',
                fill: '#DCE0E6',
              },
              null
            ),
            w('g', { transform: 'translate(149.65 15.383)', fill: '#FFF' }, [
              w('ellipse', { cx: '20.654', cy: '3.167', rx: '2.849', ry: '2.815' }, null),
              w('path', { d: 'M5.698 5.63H0L2.898.704zM9.259.704h4.985V5.63H9.259z' }, null),
            ]),
          ]),
        ]
      )
  },
})
ps.PRESENTED_IMAGE_DEFAULT = !0
const Ou = be({
  compatConfig: { MODE: 3 },
  setup() {
    const [, e] = To(),
      t = L(() => {
        const {
          colorFill: n,
          colorFillTertiary: r,
          colorFillQuaternary: o,
          colorBgContainer: i,
        } = e.value
        return {
          borderColor: new ve(n).onBackground(i).toHexString(),
          shadowColor: new ve(r).onBackground(i).toHexString(),
          contentColor: new ve(o).onBackground(i).toHexString(),
        }
      })
    return () =>
      w(
        'svg',
        { width: '64', height: '41', viewBox: '0 0 64 41', xmlns: 'http://www.w3.org/2000/svg' },
        [
          w('g', { transform: 'translate(0 1)', fill: 'none', 'fill-rule': 'evenodd' }, [
            w(
              'ellipse',
              { fill: t.value.shadowColor, cx: '32', cy: '33', rx: '32', ry: '7' },
              null
            ),
            w('g', { 'fill-rule': 'nonzero', stroke: t.value.borderColor }, [
              w(
                'path',
                {
                  d: 'M55 12.76L44.854 1.258C44.367.474 43.656 0 42.907 0H21.093c-.749 0-1.46.474-1.947 1.257L9 12.761V22h46v-9.24z',
                },
                null
              ),
              w(
                'path',
                {
                  d: 'M41.613 15.931c0-1.605.994-2.93 2.227-2.931H55v18.137C55 33.26 53.68 35 52.05 35h-40.1C10.32 35 9 33.259 9 31.137V13h11.16c1.233 0 2.227 1.323 2.227 2.928v.022c0 1.605 1.005 2.901 2.237 2.901h14.752c1.232 0 2.237-1.308 2.237-2.913v-.007z',
                  fill: t.value.contentColor,
                },
                null
              ),
            ]),
          ]),
        ]
      )
  },
})
Ou.PRESENTED_IMAGE_SIMPLE = !0
const l0 = (e) => {
    const { componentCls: t, margin: n, marginXS: r, marginXL: o, fontSize: i, lineHeight: s } = e
    return {
      [t]: {
        marginInline: r,
        fontSize: i,
        lineHeight: s,
        textAlign: 'center',
        [`${t}-image`]: {
          height: e.emptyImgHeight,
          marginBottom: r,
          opacity: e.opacityImage,
          img: { height: '100%' },
          svg: { height: '100%', margin: 'auto' },
        },
        [`${t}-footer`]: { marginTop: n },
        '&-normal': {
          marginBlock: o,
          color: e.colorTextDisabled,
          [`${t}-image`]: { height: e.emptyImgHeightMD },
        },
        '&-small': {
          marginBlock: r,
          color: e.colorTextDisabled,
          [`${t}-image`]: { height: e.emptyImgHeightSM },
        },
      },
    }
  },
  c0 = ds('Empty', (e) => {
    const { componentCls: t, controlHeightLG: n } = e,
      r = Oo(e, {
        emptyImgCls: `${t}-img`,
        emptyImgHeight: n * 2.5,
        emptyImgHeightMD: n,
        emptyImgHeightSM: n * 0.875,
      })
    return [l0(r)]
  })
var u0 = function (e, t) {
  var n = {}
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
  if (e != null && typeof Object.getOwnPropertySymbols == 'function')
    for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
      t.indexOf(r[o]) < 0 &&
        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
        (n[r[o]] = e[r[o]])
  return n
}
const f0 = () => ({ prefixCls: String, imageStyle: He(), image: yi(), description: yi() }),
  hs = be({
    name: 'AEmpty',
    compatConfig: { MODE: 3 },
    inheritAttrs: !1,
    props: f0(),
    setup(e, t) {
      let { slots: n = {}, attrs: r } = t
      const { direction: o, prefixCls: i } = $o('empty', e),
        [s, a] = c0(i)
      return () => {
        var l, u
        const c = i.value,
          f = T(T({}, e), r),
          {
            image: d = ((l = n.image) === null || l === void 0 ? void 0 : l.call(n)) || Zt(ps),
            description: p = ((u = n.description) === null || u === void 0 ? void 0 : u.call(n)) ||
              void 0,
            imageStyle: m,
            class: v = '',
          } = f,
          b = u0(f, ['image', 'description', 'imageStyle', 'class']),
          C = typeof d == 'function' ? d() : d,
          O = typeof C == 'object' && 'type' in C && C.type.PRESENTED_IMAGE_SIMPLE
        return s(
          w(
            qc,
            {
              componentName: 'Empty',
              children: (P) => {
                const x = typeof p < 'u' ? p : P.description,
                  _ = typeof x == 'string' ? x : 'empty'
                let H = null
                return (
                  typeof C == 'string' ? (H = w('img', { alt: _, src: C }, null)) : (H = C),
                  w(
                    'div',
                    me(
                      {
                        class: De(c, v, a.value, {
                          [`${c}-normal`]: O,
                          [`${c}-rtl`]: o.value === 'rtl',
                        }),
                      },
                      b
                    ),
                    [
                      w('div', { class: `${c}-image`, style: m }, [H]),
                      x && w('p', { class: `${c}-description` }, [x]),
                      n.default && w('div', { class: `${c}-footer` }, [Wc(n.default())]),
                    ]
                  )
                )
              },
            },
            null
          )
        )
      }
    },
  })
hs.PRESENTED_IMAGE_DEFAULT = () => Zt(ps)
hs.PRESENTED_IMAGE_SIMPLE = () => Zt(Ou)
const zn = ss(hs),
  Tu = (e) => {
    const { prefixCls: t } = $o('empty', e)
    return ((r) => {
      switch (r) {
        case 'Table':
        case 'List':
          return w(zn, { image: zn.PRESENTED_IMAGE_SIMPLE }, null)
        case 'Select':
        case 'TreeSelect':
        case 'Cascader':
        case 'Transfer':
        case 'Mentions':
          return w(zn, { image: zn.PRESENTED_IMAGE_SIMPLE, class: `${t.value}-small` }, null)
        default:
          return w(zn, null, null)
      }
    })(e.componentName)
  }
function d0(e) {
  return w(Tu, { componentName: e }, null)
}
const $u = Symbol('SizeContextKey'),
  Pu = () => Ee($u, qe(void 0)),
  p0 = (e) => {
    const t = Pu()
    return (
      Ot(
        $u,
        L(() => e.value || t.value)
      ),
      e
    )
  },
  $o = (e, t) => {
    const n = Pu(),
      r = Kc(),
      o = Ee(ls, T(T({}, Vc), { renderEmpty: (y) => Zt(Tu, { componentName: y }) })),
      i = L(() => o.getPrefixCls(e, t.prefixCls)),
      s = L(() => {
        var y, E
        return (y = t.direction) !== null && y !== void 0
          ? y
          : (E = o.direction) === null || E === void 0
            ? void 0
            : E.value
      }),
      a = L(() => {
        var y
        return (y = t.iconPrefixCls) !== null && y !== void 0 ? y : o.iconPrefixCls.value
      }),
      l = L(() => o.getPrefixCls()),
      u = L(() => {
        var y
        return (y = o.autoInsertSpaceInButton) === null || y === void 0 ? void 0 : y.value
      }),
      c = o.renderEmpty,
      f = o.space,
      d = o.pageHeader,
      p = o.form,
      m = L(() => {
        var y, E
        return (y = t.getTargetContainer) !== null && y !== void 0
          ? y
          : (E = o.getTargetContainer) === null || E === void 0
            ? void 0
            : E.value
      }),
      v = L(() => {
        var y, E, $
        return (E = (y = t.getContainer) !== null && y !== void 0 ? y : t.getPopupContainer) !==
          null && E !== void 0
          ? E
          : ($ = o.getPopupContainer) === null || $ === void 0
            ? void 0
            : $.value
      }),
      b = L(() => {
        var y, E
        return (y = t.dropdownMatchSelectWidth) !== null && y !== void 0
          ? y
          : (E = o.dropdownMatchSelectWidth) === null || E === void 0
            ? void 0
            : E.value
      }),
      C = L(() => {
        var y
        return (
          (t.virtual === void 0
            ? ((y = o.virtual) === null || y === void 0 ? void 0 : y.value) !== !1
            : t.virtual !== !1) && b.value !== !1
        )
      }),
      O = L(() => t.size || n.value),
      P = L(() => {
        var y, E, $
        return (y = t.autocomplete) !== null && y !== void 0
          ? y
          : ($ = (E = o.input) === null || E === void 0 ? void 0 : E.value) === null || $ === void 0
            ? void 0
            : $.autocomplete
      }),
      x = L(() => {
        var y
        return (y = t.disabled) !== null && y !== void 0 ? y : r.value
      }),
      _ = L(() => {
        var y
        return (y = t.csp) !== null && y !== void 0 ? y : o.csp
      }),
      H = L(() => {
        var y, E
        return (y = t.wave) !== null && y !== void 0
          ? y
          : (E = o.wave) === null || E === void 0
            ? void 0
            : E.value
      })
    return {
      configProvider: o,
      prefixCls: i,
      direction: s,
      size: O,
      getTargetContainer: m,
      getPopupContainer: v,
      space: f,
      pageHeader: d,
      form: p,
      autoInsertSpaceInButton: u,
      renderEmpty: c,
      virtual: C,
      dropdownMatchSelectWidth: b,
      rootPrefixCls: l,
      getPrefixCls: o.getPrefixCls,
      autocomplete: P,
      csp: _,
      iconPrefixCls: a,
      disabled: x,
      select: o.select,
      wave: H,
    }
  }
function h0(e, t) {
  for (var n = 0; n < t.length; n++) {
    var r = t[n]
    ;((r.enumerable = r.enumerable || !1),
      (r.configurable = !0),
      'value' in r && (r.writable = !0),
      Object.defineProperty(e, r.key, r))
  }
}
function Eu(e, t, n) {
  return (n && h0(e, n), e)
}
function Nr() {
  return (Nr =
    Object.assign ||
    function (e) {
      for (var t = 1; t < arguments.length; t++) {
        var n = arguments[t]
        for (var r in n) Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r])
      }
      return e
    }).apply(this, arguments)
}
function Au(e, t) {
  ;((e.prototype = Object.create(t.prototype)), (e.prototype.constructor = e), (e.__proto__ = t))
}
function Mu(e, t) {
  if (e == null) return {}
  var n,
    r,
    o = {},
    i = Object.keys(e)
  for (r = 0; r < i.length; r++) t.indexOf((n = i[r])) >= 0 || (o[n] = e[n])
  return o
}
function Fa(e) {
  return (
    ((t = e) != null && typeof t == 'object' && Array.isArray(t) === !1) == 1 &&
    Object.prototype.toString.call(e) === '[object Object]'
  )
  var t
}
var Iu = Object.prototype,
  ju = Iu.toString,
  g0 = Iu.hasOwnProperty,
  Ru = /^\s*function (\w+)/
function ka(e) {
  var t,
    n = (t = e?.type) !== null && t !== void 0 ? t : e
  if (n) {
    var r = n.toString().match(Ru)
    return r ? r[1] : ''
  }
  return ''
}
var tn = function (e) {
    var t, n
    return (
      Fa(e) !== !1 &&
      typeof (t = e.constructor) == 'function' &&
      Fa((n = t.prototype)) !== !1 &&
      n.hasOwnProperty('isPrototypeOf') !== !1
    )
  },
  m0 = function (e) {
    return e
  },
  ke = m0,
  ur = function (e, t) {
    return g0.call(e, t)
  },
  v0 =
    Number.isInteger ||
    function (e) {
      return typeof e == 'number' && isFinite(e) && Math.floor(e) === e
    },
  On =
    Array.isArray ||
    function (e) {
      return ju.call(e) === '[object Array]'
    },
  Tn = function (e) {
    return ju.call(e) === '[object Function]'
  },
  no = function (e) {
    return tn(e) && ur(e, '_vueTypes_name')
  },
  Lu = function (e) {
    return (
      tn(e) &&
      (ur(e, 'type') ||
        ['_vueTypes_name', 'validator', 'default', 'required'].some(function (t) {
          return ur(e, t)
        }))
    )
  }
function gs(e, t) {
  return Object.defineProperty(e.bind(t), '__original', { value: e })
}
function rn(e, t, n) {
  var r,
    o = !0,
    i = ''
  r = tn(e) ? e : { type: e }
  var s = no(r) ? r._vueTypes_name + ' - ' : ''
  if (Lu(r) && r.type !== null) {
    if (r.type === void 0 || r.type === !0 || (!r.required && t === void 0)) return o
    On(r.type)
      ? ((o = r.type.some(function (f) {
          return rn(f, t) === !0
        })),
        (i = r.type
          .map(function (f) {
            return ka(f)
          })
          .join(' or ')))
      : (o =
          (i = ka(r)) === 'Array'
            ? On(t)
            : i === 'Object'
              ? tn(t)
              : i === 'String' || i === 'Number' || i === 'Boolean' || i === 'Function'
                ? (function (f) {
                    if (f == null) return ''
                    var d = f.constructor.toString().match(Ru)
                    return d ? d[1] : ''
                  })(t) === i
                : t instanceof r.type)
  }
  if (!o) {
    var a = s + 'value "' + t + '" should be of type "' + i + '"'
    return a
  }
  if (ur(r, 'validator') && Tn(r.validator)) {
    var l = ke,
      u = []
    if (
      ((ke = function (f) {
        u.push(f)
      }),
      (o = r.validator(t)),
      (ke = l),
      !o)
    ) {
      var c =
        (u.length > 1 ? '* ' : '') +
        u.join(`
* `)
      return ((u.length = 0), c)
    }
  }
  return o
}
function Ne(e, t) {
  var n = Object.defineProperties(t, {
      _vueTypes_name: { value: e, writable: !0 },
      isRequired: {
        get: function () {
          return ((this.required = !0), this)
        },
      },
      def: {
        value: function (o) {
          return o !== void 0 || this.default
            ? Tn(o) || rn(this, o) === !0
              ? ((this.default = On(o)
                  ? function () {
                      return [].concat(o)
                    }
                  : tn(o)
                    ? function () {
                        return Object.assign({}, o)
                      }
                    : o),
                this)
              : (ke(this._vueTypes_name + ' - invalid default value: "' + o + '"'), this)
            : this
        },
      },
    }),
    r = n.validator
  return (Tn(r) && (n.validator = gs(r, n)), n)
}
function ft(e, t) {
  var n = Ne(e, t)
  return Object.defineProperty(n, 'validate', {
    value: function (r) {
      return (
        Tn(this.validator) &&
          ke(
            this._vueTypes_name +
              ` - calling .validate() will overwrite the current custom validator function. Validator info:
` +
              JSON.stringify(this)
          ),
        (this.validator = gs(r, this)),
        this
      )
    },
  })
}
function Na(e, t, n) {
  var r,
    o,
    i =
      ((r = t),
      (o = {}),
      Object.getOwnPropertyNames(r).forEach(function (f) {
        o[f] = Object.getOwnPropertyDescriptor(r, f)
      }),
      Object.defineProperties({}, o))
  if (((i._vueTypes_name = e), !tn(n))) return i
  var s,
    a,
    l = n.validator,
    u = Mu(n, ['validator'])
  if (Tn(l)) {
    var c = i.validator
    ;(c && (c = (a = (s = c).__original) !== null && a !== void 0 ? a : s),
      (i.validator = gs(
        c
          ? function (f) {
              return c.call(this, f) && l.call(this, f)
            }
          : l,
        i
      )))
  }
  return Object.assign(i, u)
}
function Po(e) {
  return e.replace(/^(?!\s*$)/gm, '  ')
}
var y0 = function () {
    return ft('any', {})
  },
  b0 = function () {
    return ft('function', { type: Function })
  },
  C0 = function () {
    return ft('boolean', { type: Boolean })
  },
  x0 = function () {
    return ft('string', { type: String })
  },
  S0 = function () {
    return ft('number', { type: Number })
  },
  _0 = function () {
    return ft('array', { type: Array })
  },
  w0 = function () {
    return ft('object', { type: Object })
  },
  O0 = function () {
    return Ne('integer', {
      type: Number,
      validator: function (e) {
        return v0(e)
      },
    })
  },
  T0 = function () {
    return Ne('symbol', {
      validator: function (e) {
        return typeof e == 'symbol'
      },
    })
  }
function $0(e, t) {
  if ((t === void 0 && (t = 'custom validation failed'), typeof e != 'function'))
    throw new TypeError('[VueTypes error]: You must provide a function as argument')
  return Ne(e.name || '<<anonymous function>>', {
    validator: function (n) {
      var r = e(n)
      return (r || ke(this._vueTypes_name + ' - ' + t), r)
    },
  })
}
function P0(e) {
  if (!On(e)) throw new TypeError('[VueTypes error]: You must provide an array as argument.')
  var t = 'oneOf - value should be one of "' + e.join('", "') + '".',
    n = e.reduce(function (r, o) {
      if (o != null) {
        var i = o.constructor
        r.indexOf(i) === -1 && r.push(i)
      }
      return r
    }, [])
  return Ne('oneOf', {
    type: n.length > 0 ? n : void 0,
    validator: function (r) {
      var o = e.indexOf(r) !== -1
      return (o || ke(t), o)
    },
  })
}
function E0(e) {
  if (!On(e)) throw new TypeError('[VueTypes error]: You must provide an array as argument')
  for (var t = !1, n = [], r = 0; r < e.length; r += 1) {
    var o = e[r]
    if (Lu(o)) {
      if (no(o) && o._vueTypes_name === 'oneOf') {
        n = n.concat(o.type)
        continue
      }
      if ((Tn(o.validator) && (t = !0), o.type !== !0 && o.type)) {
        n = n.concat(o.type)
        continue
      }
    }
    n.push(o)
  }
  return (
    (n = n.filter(function (i, s) {
      return n.indexOf(i) === s
    })),
    Ne(
      'oneOfType',
      t
        ? {
            type: n,
            validator: function (i) {
              var s = [],
                a = e.some(function (l) {
                  var u = rn(no(l) && l._vueTypes_name === 'oneOf' ? l.type || null : l, i)
                  return (typeof u == 'string' && s.push(u), u === !0)
                })
              return (
                a ||
                  ke(
                    'oneOfType - provided value does not match any of the ' +
                      s.length +
                      ` passed-in validators:
` +
                      Po(
                        s.join(`
`)
                      )
                  ),
                a
              )
            },
          }
        : { type: n }
    )
  )
}
function A0(e) {
  return Ne('arrayOf', {
    type: Array,
    validator: function (t) {
      var n,
        r = t.every(function (o) {
          return (n = rn(e, o)) === !0
        })
      return (
        r ||
          ke(
            `arrayOf - value validation error:
` + Po(n)
          ),
        r
      )
    },
  })
}
function M0(e) {
  return Ne('instanceOf', { type: e })
}
function I0(e) {
  return Ne('objectOf', {
    type: Object,
    validator: function (t) {
      var n,
        r = Object.keys(t).every(function (o) {
          return (n = rn(e, t[o])) === !0
        })
      return (
        r ||
          ke(
            `objectOf - value validation error:
` + Po(n)
          ),
        r
      )
    },
  })
}
function j0(e) {
  var t = Object.keys(e),
    n = t.filter(function (o) {
      var i
      return !!(!((i = e[o]) === null || i === void 0) && i.required)
    }),
    r = Ne('shape', {
      type: Object,
      validator: function (o) {
        var i = this
        if (!tn(o)) return !1
        var s = Object.keys(o)
        if (
          n.length > 0 &&
          n.some(function (l) {
            return s.indexOf(l) === -1
          })
        ) {
          var a = n.filter(function (l) {
            return s.indexOf(l) === -1
          })
          return (
            ke(
              a.length === 1
                ? 'shape - required property "' + a[0] + '" is not defined.'
                : 'shape - required properties "' + a.join('", "') + '" are not defined.'
            ),
            !1
          )
        }
        return s.every(function (l) {
          if (t.indexOf(l) === -1)
            return (
              i._vueTypes_isLoose === !0 ||
              (ke(
                'shape - shape definition does not include a "' +
                  l +
                  '" property. Allowed keys: "' +
                  t.join('", "') +
                  '".'
              ),
              !1)
            )
          var u = rn(e[l], o[l])
          return (
            typeof u == 'string' &&
              ke(
                'shape - "' +
                  l +
                  `" property validation error:
 ` +
                  Po(u)
              ),
            u === !0
          )
        })
      },
    })
  return (
    Object.defineProperty(r, '_vueTypes_isLoose', { writable: !0, value: !1 }),
    Object.defineProperty(r, 'loose', {
      get: function () {
        return ((this._vueTypes_isLoose = !0), this)
      },
    }),
    r
  )
}
var ot = (function () {
  function e() {}
  return (
    (e.extend = function (t) {
      var n = this
      if (On(t))
        return (
          t.forEach(function (f) {
            return n.extend(f)
          }),
          this
        )
      var r = t.name,
        o = t.validate,
        i = o !== void 0 && o,
        s = t.getter,
        a = s !== void 0 && s,
        l = Mu(t, ['name', 'validate', 'getter'])
      if (ur(this, r)) throw new TypeError('[VueTypes error]: Type "' + r + '" already defined')
      var u,
        c = l.type
      return no(c)
        ? (delete l.type,
          Object.defineProperty(
            this,
            r,
            a
              ? {
                  get: function () {
                    return Na(r, c, l)
                  },
                }
              : {
                  value: function () {
                    var f,
                      d = Na(r, c, l)
                    return (
                      d.validator &&
                        (d.validator = (f = d.validator).bind.apply(
                          f,
                          [d].concat([].slice.call(arguments))
                        )),
                      d
                    )
                  },
                }
          ))
        : ((u = a
            ? {
                get: function () {
                  var f = Object.assign({}, l)
                  return i ? ft(r, f) : Ne(r, f)
                },
                enumerable: !0,
              }
            : {
                value: function () {
                  var f,
                    d,
                    p = Object.assign({}, l)
                  return (
                    (f = i ? ft(r, p) : Ne(r, p)),
                    p.validator &&
                      (f.validator = (d = p.validator).bind.apply(
                        d,
                        [f].concat([].slice.call(arguments))
                      )),
                    f
                  )
                },
                enumerable: !0,
              }),
          Object.defineProperty(this, r, u))
    }),
    Eu(e, null, [
      {
        key: 'any',
        get: function () {
          return y0()
        },
      },
      {
        key: 'func',
        get: function () {
          return b0().def(this.defaults.func)
        },
      },
      {
        key: 'bool',
        get: function () {
          return C0().def(this.defaults.bool)
        },
      },
      {
        key: 'string',
        get: function () {
          return x0().def(this.defaults.string)
        },
      },
      {
        key: 'number',
        get: function () {
          return S0().def(this.defaults.number)
        },
      },
      {
        key: 'array',
        get: function () {
          return _0().def(this.defaults.array)
        },
      },
      {
        key: 'object',
        get: function () {
          return w0().def(this.defaults.object)
        },
      },
      {
        key: 'integer',
        get: function () {
          return O0().def(this.defaults.integer)
        },
      },
      {
        key: 'symbol',
        get: function () {
          return T0()
        },
      },
    ]),
    e
  )
})()
function Hu(e) {
  var t
  return (
    e === void 0 &&
      (e = {
        func: function () {},
        bool: !0,
        string: '',
        number: 0,
        array: function () {
          return []
        },
        object: function () {
          return {}
        },
        integer: 0,
      }),
    ((t = (function (n) {
      function r() {
        return n.apply(this, arguments) || this
      }
      return (
        Au(r, n),
        Eu(r, null, [
          {
            key: 'sensibleDefaults',
            get: function () {
              return Nr({}, this.defaults)
            },
            set: function (o) {
              this.defaults = o !== !1 ? Nr({}, o !== !0 ? o : e) : {}
            },
          },
        ]),
        r
      )
    })(ot)).defaults = Nr({}, e)),
    t
  )
}
;((ot.defaults = {}),
  (ot.custom = $0),
  (ot.oneOf = P0),
  (ot.instanceOf = M0),
  (ot.oneOfType = E0),
  (ot.arrayOf = A0),
  (ot.objectOf = I0),
  (ot.shape = j0),
  (ot.utils = {
    validate: function (e, t) {
      return rn(t, e) === !0
    },
    toType: function (e, t, n) {
      return (n === void 0 && (n = !1), n ? ft(e, t) : Ne(e, t))
    },
  }))
;(function (e) {
  function t() {
    return e.apply(this, arguments) || this
  }
  return (Au(t, e), t)
})(Hu())
const Fu = Hu({
  func: void 0,
  bool: void 0,
  string: void 0,
  number: void 0,
  array: void 0,
  object: void 0,
  integer: void 0,
})
Fu.extend([
  { name: 'looseBool', getter: !0, type: Boolean, default: void 0 },
  { name: 'style', getter: !0, type: [String, Object], default: void 0 },
  { name: 'VueNode', getter: !0, type: null },
])
function R0(e) {
  let { prefixCls: t, animation: n, transitionName: r } = e
  return n ? { name: `${t}-${n}` } : r ? { name: r } : {}
}
Sh('bottomLeft', 'bottomRight', 'topLeft', 'topRight')
const Ry = function (e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}
    return T(
      e
        ? {
            name: e,
            appear: !0,
            enterFromClass: `${e}-enter ${e}-enter-prepare ${e}-enter-start`,
            enterActiveClass: `${e}-enter ${e}-enter-prepare`,
            enterToClass: `${e}-enter ${e}-enter-active`,
            leaveFromClass: ` ${e}-leave`,
            leaveActiveClass: `${e}-leave ${e}-leave-active`,
            leaveToClass: `${e}-leave ${e}-leave-active`,
          }
        : { css: !1 },
      t
    )
  },
  ku = function (e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}
    return T(
      e
        ? {
            name: e,
            appear: !0,
            appearActiveClass: `${e}`,
            appearToClass: `${e}-appear ${e}-appear-active`,
            enterFromClass: `${e}-appear ${e}-enter ${e}-appear-prepare ${e}-enter-prepare`,
            enterActiveClass: `${e}`,
            enterToClass: `${e}-enter ${e}-appear ${e}-appear-active ${e}-enter-active`,
            leaveActiveClass: `${e} ${e}-leave`,
            leaveToClass: `${e}-leave-active`,
          }
        : { css: !1 },
      t
    )
  },
  Ly = (e, t, n) => (n !== void 0 ? n : `${e}-${t}`),
  Nu = Symbol('PortalContextKey'),
  L0 = function (e) {
    let t =
      arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : { inTriggerContext: !0 }
    Ot(Nu, {
      inTriggerContext: t.inTriggerContext,
      shouldRender: L(() => {
        const { sPopupVisible: n, popupRef: r, forceRender: o, autoDestroy: i } = e || {}
        let s = !1
        return ((n || r || o) && (s = !0), !n && i && (s = !1), s)
      }),
    })
  },
  H0 = () => {
    L0({}, { inTriggerContext: !1 })
    const e = Ee(Nu, { shouldRender: L(() => !1), inTriggerContext: !1 })
    return { shouldRender: L(() => e.shouldRender.value || e.inTriggerContext === !1) }
  },
  F0 = be({
    compatConfig: { MODE: 3 },
    name: 'Portal',
    inheritAttrs: !1,
    props: { getContainer: Fu.func.isRequired, didUpdate: Function },
    setup(e, t) {
      let { slots: n } = t,
        r = !0,
        o
      const { shouldRender: i } = H0()
      function s() {
        i.value && (o = e.getContainer())
      }
      ;(nc(() => {
        ;((r = !1), s())
      }),
        pr(() => {
          o || s()
        }))
      const a = Fe(i, () => {
        ;(i.value && !o && (o = e.getContainer()), o && a())
      })
      return (
        qi(() => {
          po(() => {
            var l
            i.value && ((l = e.didUpdate) === null || l === void 0 || l.call(e, e))
          })
        }),
        () => {
          var l
          return i.value
            ? r
              ? (l = n.default) === null || l === void 0
                ? void 0
                : l.call(n)
              : o
                ? w(Kl, { to: o }, n)
                : null
            : null
        }
      )
    },
  })
var k0 = Symbol('iconContext'),
  Du = function () {
    return Ee(k0, { prefixCls: qe('anticon'), rootClassName: qe(''), csp: qe() })
  }
function ms() {
  return !!(typeof window < 'u' && window.document && window.document.createElement)
}
function N0(e, t) {
  return e && e.contains ? e.contains(t) : !1
}
var Da = 'data-vc-order',
  D0 = 'vc-icon-key',
  Ei = new Map()
function Bu() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {},
    t = e.mark
  return t ? (t.startsWith('data-') ? t : 'data-'.concat(t)) : D0
}
function vs(e) {
  if (e.attachTo) return e.attachTo
  var t = document.querySelector('head')
  return t || document.body
}
function B0(e) {
  return e === 'queue' ? 'prependQueue' : e ? 'prepend' : 'append'
}
function zu(e) {
  return Array.from((Ei.get(e) || e).children).filter(function (t) {
    return t.tagName === 'STYLE'
  })
}
function Wu(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}
  if (!ms()) return null
  var n = t.csp,
    r = t.prepend,
    o = document.createElement('style')
  ;(o.setAttribute(Da, B0(r)), n && n.nonce && (o.nonce = n.nonce), (o.innerHTML = e))
  var i = vs(t),
    s = i.firstChild
  if (r) {
    if (r === 'queue') {
      var a = zu(i).filter(function (l) {
        return ['prepend', 'prependQueue'].includes(l.getAttribute(Da))
      })
      if (a.length) return (i.insertBefore(o, a[a.length - 1].nextSibling), o)
    }
    i.insertBefore(o, s)
  } else i.appendChild(o)
  return o
}
function z0(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {},
    n = vs(t)
  return zu(n).find(function (r) {
    return r.getAttribute(Bu(t)) === e
  })
}
function W0(e, t) {
  var n = Ei.get(e)
  if (!n || !N0(document, n)) {
    var r = Wu('', t),
      o = r.parentNode
    ;(Ei.set(e, o), e.removeChild(r))
  }
}
function V0(e, t) {
  var n = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : {},
    r = vs(n)
  W0(r, n)
  var o = z0(t, n)
  if (o)
    return (
      n.csp && n.csp.nonce && o.nonce !== n.csp.nonce && (o.nonce = n.csp.nonce),
      o.innerHTML !== e && (o.innerHTML = e),
      o
    )
  var i = Wu(e, n)
  return (i.setAttribute(Bu(n), t), i)
}
function Ba(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        U0(e, o, n[o])
      }))
  }
  return e
}
function U0(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
function za(e) {
  return (
    typeof e == 'object' &&
    typeof e.name == 'string' &&
    typeof e.theme == 'string' &&
    (typeof e.icon == 'object' || typeof e.icon == 'function')
  )
}
function Ai(e, t, n) {
  return n
    ? Zt(
        e.tag,
        Ba({ key: t }, n, e.attrs),
        (e.children || []).map(function (r, o) {
          return Ai(r, ''.concat(t, '-').concat(e.tag, '-').concat(o))
        })
      )
    : Zt(
        e.tag,
        Ba({ key: t }, e.attrs),
        (e.children || []).map(function (r, o) {
          return Ai(r, ''.concat(t, '-').concat(e.tag, '-').concat(o))
        })
      )
}
function Vu(e) {
  return en(e)[0]
}
function Uu(e) {
  return e ? (Array.isArray(e) ? e : [e]) : []
}
var G0 = `
.anticon {
  display: inline-block;
  color: inherit;
  font-style: normal;
  line-height: 0;
  text-align: center;
  text-transform: none;
  vertical-align: -0.125em;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.anticon > * {
  line-height: 1;
}

.anticon svg {
  display: inline-block;
}

.anticon::before {
  display: none;
}

.anticon .anticon-icon {
  display: block;
}

.anticon[tabindex] {
  cursor: pointer;
}

.anticon-spin::before,
.anticon-spin {
  display: inline-block;
  -webkit-animation: loadingCircle 1s infinite linear;
  animation: loadingCircle 1s infinite linear;
}

@-webkit-keyframes loadingCircle {
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

@keyframes loadingCircle {
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
`
function Gu(e) {
  return e && e.getRootNode && e.getRootNode()
}
function K0(e) {
  return ms() ? Gu(e) instanceof ShadowRoot : !1
}
function X0(e) {
  return K0(e) ? Gu(e) : null
}
var q0 = function () {
    var t = Du(),
      n = t.prefixCls,
      r = t.csp,
      o = Lt(),
      i = G0
    ;(n && (i = i.replace(/anticon/g, n.value)),
      po(function () {
        if (ms()) {
          var s = o.vnode.el,
            a = X0(s)
          V0(i, '@ant-design-vue-icons', { prepend: !0, csp: r.value, attachTo: a })
        }
      }))
  },
  Y0 = ['icon', 'primaryColor', 'secondaryColor']
function J0(e, t) {
  if (e == null) return {}
  var n = Q0(e, t),
    r,
    o
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e)
    for (o = 0; o < i.length; o++)
      ((r = i[o]),
        !(t.indexOf(r) >= 0) && Object.prototype.propertyIsEnumerable.call(e, r) && (n[r] = e[r]))
  }
  return n
}
function Q0(e, t) {
  if (e == null) return {}
  var n = {},
    r = Object.keys(e),
    o,
    i
  for (i = 0; i < r.length; i++) ((o = r[i]), !(t.indexOf(o) >= 0) && (n[o] = e[o]))
  return n
}
function Dr(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        Z0(e, o, n[o])
      }))
  }
  return e
}
function Z0(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var er = ct({ primaryColor: '#333', secondaryColor: '#E6E6E6', calculated: !1 })
function em(e) {
  var t = e.primaryColor,
    n = e.secondaryColor
  ;((er.primaryColor = t), (er.secondaryColor = n || Vu(t)), (er.calculated = !!n))
}
function tm() {
  return Dr({}, er)
}
var Ht = function (t, n) {
  var r = Dr({}, t, n.attrs),
    o = r.icon,
    i = r.primaryColor,
    s = r.secondaryColor,
    a = J0(r, Y0),
    l = er
  if ((i && (l = { primaryColor: i, secondaryColor: s || Vu(i) }), za(o), !za(o))) return null
  var u = o
  return (
    u &&
      typeof u.icon == 'function' &&
      (u = Dr({}, u, { icon: u.icon(l.primaryColor, l.secondaryColor) })),
    Ai(
      u.icon,
      'svg-'.concat(u.name),
      Dr({}, a, {
        'data-icon': u.name,
        width: '1em',
        height: '1em',
        fill: 'currentColor',
        'aria-hidden': 'true',
      })
    )
  )
}
Ht.props = { icon: Object, primaryColor: String, secondaryColor: String, focusable: String }
Ht.inheritAttrs = !1
Ht.displayName = 'IconBase'
Ht.getTwoToneColors = tm
Ht.setTwoToneColors = em
function nm(e, t) {
  return sm(e) || im(e, t) || om(e, t) || rm()
}
function rm() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)
}
function om(e, t) {
  if (e) {
    if (typeof e == 'string') return Wa(e, t)
    var n = Object.prototype.toString.call(e).slice(8, -1)
    if ((n === 'Object' && e.constructor && (n = e.constructor.name), n === 'Map' || n === 'Set'))
      return Array.from(e)
    if (n === 'Arguments' || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return Wa(e, t)
  }
}
function Wa(e, t) {
  ;(t == null || t > e.length) && (t = e.length)
  for (var n = 0, r = new Array(t); n < t; n++) r[n] = e[n]
  return r
}
function im(e, t) {
  var n = e == null ? null : (typeof Symbol < 'u' && e[Symbol.iterator]) || e['@@iterator']
  if (n != null) {
    var r = [],
      o = !0,
      i = !1,
      s,
      a
    try {
      for (
        n = n.call(e);
        !(o = (s = n.next()).done) && (r.push(s.value), !(t && r.length === t));
        o = !0
      );
    } catch (l) {
      ;((i = !0), (a = l))
    } finally {
      try {
        !o && n.return != null && n.return()
      } finally {
        if (i) throw a
      }
    }
    return r
  }
}
function sm(e) {
  if (Array.isArray(e)) return e
}
function Ku(e) {
  var t = Uu(e),
    n = nm(t, 2),
    r = n[0],
    o = n[1]
  return Ht.setTwoToneColors({ primaryColor: r, secondaryColor: o })
}
function am() {
  var e = Ht.getTwoToneColors()
  return e.calculated ? [e.primaryColor, e.secondaryColor] : e.primaryColor
}
var lm = be({
    name: 'InsertStyles',
    setup: function () {
      return (
        q0(),
        function () {
          return null
        }
      )
    },
  }),
  cm = ['class', 'icon', 'spin', 'rotate', 'tabindex', 'twoToneColor', 'onClick']
function um(e, t) {
  return hm(e) || pm(e, t) || dm(e, t) || fm()
}
function fm() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)
}
function dm(e, t) {
  if (e) {
    if (typeof e == 'string') return Va(e, t)
    var n = Object.prototype.toString.call(e).slice(8, -1)
    if ((n === 'Object' && e.constructor && (n = e.constructor.name), n === 'Map' || n === 'Set'))
      return Array.from(e)
    if (n === 'Arguments' || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return Va(e, t)
  }
}
function Va(e, t) {
  ;(t == null || t > e.length) && (t = e.length)
  for (var n = 0, r = new Array(t); n < t; n++) r[n] = e[n]
  return r
}
function pm(e, t) {
  var n = e == null ? null : (typeof Symbol < 'u' && e[Symbol.iterator]) || e['@@iterator']
  if (n != null) {
    var r = [],
      o = !0,
      i = !1,
      s,
      a
    try {
      for (
        n = n.call(e);
        !(o = (s = n.next()).done) && (r.push(s.value), !(t && r.length === t));
        o = !0
      );
    } catch (l) {
      ;((i = !0), (a = l))
    } finally {
      try {
        !o && n.return != null && n.return()
      } finally {
        if (i) throw a
      }
    }
    return r
  }
}
function hm(e) {
  if (Array.isArray(e)) return e
}
function Ua(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        Vn(e, o, n[o])
      }))
  }
  return e
}
function Vn(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
function gm(e, t) {
  if (e == null) return {}
  var n = mm(e, t),
    r,
    o
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e)
    for (o = 0; o < i.length; o++)
      ((r = i[o]),
        !(t.indexOf(r) >= 0) && Object.prototype.propertyIsEnumerable.call(e, r) && (n[r] = e[r]))
  }
  return n
}
function mm(e, t) {
  if (e == null) return {}
  var n = {},
    r = Object.keys(e),
    o,
    i
  for (i = 0; i < r.length; i++) ((o = r[i]), !(t.indexOf(o) >= 0) && (n[o] = e[o]))
  return n
}
Ku(Dg.primary)
var Ae = function (t, n) {
  var r,
    o = Ua({}, t, n.attrs),
    i = o.class,
    s = o.icon,
    a = o.spin,
    l = o.rotate,
    u = o.tabindex,
    c = o.twoToneColor,
    f = o.onClick,
    d = gm(o, cm),
    p = Du(),
    m = p.prefixCls,
    v = p.rootClassName,
    b =
      ((r = {}),
      Vn(r, v.value, !!v.value),
      Vn(r, m.value, !0),
      Vn(r, ''.concat(m.value, '-').concat(s.name), !!s.name),
      Vn(r, ''.concat(m.value, '-spin'), !!a || s.name === 'loading'),
      r),
    C = u
  C === void 0 && f && (C = -1)
  var O = l
      ? { msTransform: 'rotate('.concat(l, 'deg)'), transform: 'rotate('.concat(l, 'deg)') }
      : void 0,
    P = Uu(c),
    x = um(P, 2),
    _ = x[0],
    H = x[1]
  return w(
    'span',
    Ua({ role: 'img', 'aria-label': s.name }, d, { onClick: f, class: [b, i], tabindex: C }),
    [w(Ht, { icon: s, primaryColor: _, secondaryColor: H, style: O }, null), w(lm, null, null)]
  )
}
Ae.props = { spin: Boolean, rotate: Number, icon: Object, twoToneColor: [String, Array] }
Ae.displayName = 'AntdIcon'
Ae.inheritAttrs = !1
Ae.getTwoToneColor = am
Ae.setTwoToneColor = Ku
var vm = {
  icon: {
    tag: 'svg',
    attrs: { viewBox: '0 0 1024 1024', focusable: 'false' },
    children: [
      {
        tag: 'path',
        attrs: {
          d: 'M988 548c-19.9 0-36-16.1-36-36 0-59.4-11.6-117-34.6-171.3a440.45 440.45 0 00-94.3-139.9 437.71 437.71 0 00-139.9-94.3C629 83.6 571.4 72 512 72c-19.9 0-36-16.1-36-36s16.1-36 36-36c69.1 0 136.2 13.5 199.3 40.3C772.3 66 827 103 874 150c47 47 83.9 101.8 109.7 162.7 26.7 63.1 40.2 130.2 40.2 199.3.1 19.9-16 36-35.9 36z',
        },
      },
    ],
  },
  name: 'loading',
  theme: 'outlined',
}
function Ga(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        ym(e, o, n[o])
      }))
  }
  return e
}
function ym(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var mr = function (t, n) {
  var r = Ga({}, t, n.attrs)
  return w(Ae, Ga({}, r, { icon: vm }), null)
}
mr.displayName = 'LoadingOutlined'
mr.inheritAttrs = !1
var bm = {
  icon: {
    tag: 'svg',
    attrs: { 'fill-rule': 'evenodd', viewBox: '64 64 896 896', focusable: 'false' },
    children: [
      {
        tag: 'path',
        attrs: {
          d: 'M799.86 166.31c.02 0 .04.02.08.06l57.69 57.7c.04.03.05.05.06.08a.12.12 0 010 .06c0 .03-.02.05-.06.09L569.93 512l287.7 287.7c.04.04.05.06.06.09a.12.12 0 010 .07c0 .02-.02.04-.06.08l-57.7 57.69c-.03.04-.05.05-.07.06a.12.12 0 01-.07 0c-.03 0-.05-.02-.09-.06L512 569.93l-287.7 287.7c-.04.04-.06.05-.09.06a.12.12 0 01-.07 0c-.02 0-.04-.02-.08-.06l-57.69-57.7c-.04-.03-.05-.05-.06-.07a.12.12 0 010-.07c0-.03.02-.05.06-.09L454.07 512l-287.7-287.7c-.04-.04-.05-.06-.06-.09a.12.12 0 010-.07c0-.02.02-.04.06-.08l57.7-57.69c.03-.04.05-.05.07-.06a.12.12 0 01.07 0c.03 0 .05.02.09.06L512 454.07l287.7-287.7c.04-.04.06-.05.09-.06a.12.12 0 01.07 0z',
        },
      },
    ],
  },
  name: 'close',
  theme: 'outlined',
}
function Ka(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        Cm(e, o, n[o])
      }))
  }
  return e
}
function Cm(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var vr = function (t, n) {
  var r = Ka({}, t, n.attrs)
  return w(Ae, Ka({}, r, { icon: bm }), null)
}
vr.displayName = 'CloseOutlined'
vr.inheritAttrs = !1
var xm = {
  icon: {
    tag: 'svg',
    attrs: { 'fill-rule': 'evenodd', viewBox: '64 64 896 896', focusable: 'false' },
    children: [
      {
        tag: 'path',
        attrs: {
          d: 'M512 64c247.4 0 448 200.6 448 448S759.4 960 512 960 64 759.4 64 512 264.6 64 512 64zm127.98 274.82h-.04l-.08.06L512 466.75 384.14 338.88c-.04-.05-.06-.06-.08-.06a.12.12 0 00-.07 0c-.03 0-.05.01-.09.05l-45.02 45.02a.2.2 0 00-.05.09.12.12 0 000 .07v.02a.27.27 0 00.06.06L466.75 512 338.88 639.86c-.05.04-.06.06-.06.08a.12.12 0 000 .07c0 .03.01.05.05.09l45.02 45.02a.2.2 0 00.09.05.12.12 0 00.07 0c.02 0 .04-.01.08-.05L512 557.25l127.86 127.87c.04.04.06.05.08.05a.12.12 0 00.07 0c.03 0 .05-.01.09-.05l45.02-45.02a.2.2 0 00.05-.09.12.12 0 000-.07v-.02a.27.27 0 00-.05-.06L557.25 512l127.87-127.86c.04-.04.05-.06.05-.08a.12.12 0 000-.07c0-.03-.01-.05-.05-.09l-45.02-45.02a.2.2 0 00-.09-.05.12.12 0 00-.07 0z',
        },
      },
    ],
  },
  name: 'close-circle',
  theme: 'filled',
}
function Xa(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        Sm(e, o, n[o])
      }))
  }
  return e
}
function Sm(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var Mn = function (t, n) {
  var r = Xa({}, t, n.attrs)
  return w(Ae, Xa({}, r, { icon: xm }), null)
}
Mn.displayName = 'CloseCircleFilled'
Mn.inheritAttrs = !1
var _m = {
  icon: {
    tag: 'svg',
    attrs: { viewBox: '64 64 896 896', focusable: 'false' },
    children: [
      {
        tag: 'path',
        attrs: {
          d: 'M699 353h-46.9c-10.2 0-19.9 4.9-25.9 13.3L469 584.3l-71.2-98.8c-6-8.3-15.6-13.3-25.9-13.3H325c-6.5 0-10.3 7.4-6.5 12.7l124.6 172.8a31.8 31.8 0 0051.7 0l210.6-292c3.9-5.3.1-12.7-6.4-12.7z',
        },
      },
      {
        tag: 'path',
        attrs: {
          d: 'M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z',
        },
      },
    ],
  },
  name: 'check-circle',
  theme: 'outlined',
}
function qa(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        wm(e, o, n[o])
      }))
  }
  return e
}
function wm(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var ys = function (t, n) {
  var r = qa({}, t, n.attrs)
  return w(Ae, qa({}, r, { icon: _m }), null)
}
ys.displayName = 'CheckCircleOutlined'
ys.inheritAttrs = !1
var Om = {
  icon: {
    tag: 'svg',
    attrs: { viewBox: '64 64 896 896', focusable: 'false' },
    children: [
      {
        tag: 'path',
        attrs: {
          d: 'M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z',
        },
      },
      {
        tag: 'path',
        attrs: {
          d: 'M464 688a48 48 0 1096 0 48 48 0 10-96 0zm24-112h48c4.4 0 8-3.6 8-8V296c0-4.4-3.6-8-8-8h-48c-4.4 0-8 3.6-8 8v272c0 4.4 3.6 8 8 8z',
        },
      },
    ],
  },
  name: 'exclamation-circle',
  theme: 'outlined',
}
function Ya(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        Tm(e, o, n[o])
      }))
  }
  return e
}
function Tm(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var bs = function (t, n) {
  var r = Ya({}, t, n.attrs)
  return w(Ae, Ya({}, r, { icon: Om }), null)
}
bs.displayName = 'ExclamationCircleOutlined'
bs.inheritAttrs = !1
var $m = {
  icon: {
    tag: 'svg',
    attrs: { viewBox: '64 64 896 896', focusable: 'false' },
    children: [
      {
        tag: 'path',
        attrs: {
          d: 'M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z',
        },
      },
      {
        tag: 'path',
        attrs: {
          d: 'M464 336a48 48 0 1096 0 48 48 0 10-96 0zm72 112h-48c-4.4 0-8 3.6-8 8v272c0 4.4 3.6 8 8 8h48c4.4 0 8-3.6 8-8V456c0-4.4-3.6-8-8-8z',
        },
      },
    ],
  },
  name: 'info-circle',
  theme: 'outlined',
}
function Ja(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        Pm(e, o, n[o])
      }))
  }
  return e
}
function Pm(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var Cs = function (t, n) {
  var r = Ja({}, t, n.attrs)
  return w(Ae, Ja({}, r, { icon: $m }), null)
}
Cs.displayName = 'InfoCircleOutlined'
Cs.inheritAttrs = !1
var Em = {
  icon: {
    tag: 'svg',
    attrs: { 'fill-rule': 'evenodd', viewBox: '64 64 896 896', focusable: 'false' },
    children: [
      {
        tag: 'path',
        attrs: {
          d: 'M512 64c247.4 0 448 200.6 448 448S759.4 960 512 960 64 759.4 64 512 264.6 64 512 64zm0 76c-205.4 0-372 166.6-372 372s166.6 372 372 372 372-166.6 372-372-166.6-372-372-372zm128.01 198.83c.03 0 .05.01.09.06l45.02 45.01a.2.2 0 01.05.09.12.12 0 010 .07c0 .02-.01.04-.05.08L557.25 512l127.87 127.86a.27.27 0 01.05.06v.02a.12.12 0 010 .07c0 .03-.01.05-.05.09l-45.02 45.02a.2.2 0 01-.09.05.12.12 0 01-.07 0c-.02 0-.04-.01-.08-.05L512 557.25 384.14 685.12c-.04.04-.06.05-.08.05a.12.12 0 01-.07 0c-.03 0-.05-.01-.09-.05l-45.02-45.02a.2.2 0 01-.05-.09.12.12 0 010-.07c0-.02.01-.04.06-.08L466.75 512 338.88 384.14a.27.27 0 01-.05-.06l-.01-.02a.12.12 0 010-.07c0-.03.01-.05.05-.09l45.02-45.02a.2.2 0 01.09-.05.12.12 0 01.07 0c.02 0 .04.01.08.06L512 466.75l127.86-127.86c.04-.05.06-.06.08-.06a.12.12 0 01.07 0z',
        },
      },
    ],
  },
  name: 'close-circle',
  theme: 'outlined',
}
function Qa(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        Am(e, o, n[o])
      }))
  }
  return e
}
function Am(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var xs = function (t, n) {
  var r = Qa({}, t, n.attrs)
  return w(Ae, Qa({}, r, { icon: Em }), null)
}
xs.displayName = 'CloseCircleOutlined'
xs.inheritAttrs = !1
var Mm = {
  icon: {
    tag: 'svg',
    attrs: { viewBox: '64 64 896 896', focusable: 'false' },
    children: [
      {
        tag: 'path',
        attrs: {
          d: 'M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm193.5 301.7l-210.6 292a31.8 31.8 0 01-51.7 0L318.5 484.9c-3.8-5.3 0-12.7 6.5-12.7h46.9c10.2 0 19.9 4.9 25.9 13.3l71.2 98.8 157.2-218c6-8.3 15.6-13.3 25.9-13.3H699c6.5 0 10.3 7.4 6.5 12.7z',
        },
      },
    ],
  },
  name: 'check-circle',
  theme: 'filled',
}
function Za(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        Im(e, o, n[o])
      }))
  }
  return e
}
function Im(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var In = function (t, n) {
  var r = Za({}, t, n.attrs)
  return w(Ae, Za({}, r, { icon: Mm }), null)
}
In.displayName = 'CheckCircleFilled'
In.inheritAttrs = !1
var jm = {
  icon: {
    tag: 'svg',
    attrs: { viewBox: '64 64 896 896', focusable: 'false' },
    children: [
      {
        tag: 'path',
        attrs: {
          d: 'M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm-32 232c0-4.4 3.6-8 8-8h48c4.4 0 8 3.6 8 8v272c0 4.4-3.6 8-8 8h-48c-4.4 0-8-3.6-8-8V296zm32 440a48.01 48.01 0 010-96 48.01 48.01 0 010 96z',
        },
      },
    ],
  },
  name: 'exclamation-circle',
  theme: 'filled',
}
function el(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        Rm(e, o, n[o])
      }))
  }
  return e
}
function Rm(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var jn = function (t, n) {
  var r = el({}, t, n.attrs)
  return w(Ae, el({}, r, { icon: jm }), null)
}
jn.displayName = 'ExclamationCircleFilled'
jn.inheritAttrs = !1
var Lm = {
  icon: {
    tag: 'svg',
    attrs: { viewBox: '64 64 896 896', focusable: 'false' },
    children: [
      {
        tag: 'path',
        attrs: {
          d: 'M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm32 664c0 4.4-3.6 8-8 8h-48c-4.4 0-8-3.6-8-8V456c0-4.4 3.6-8 8-8h48c4.4 0 8 3.6 8 8v272zm-32-344a48.01 48.01 0 010-96 48.01 48.01 0 010 96z',
        },
      },
    ],
  },
  name: 'info-circle',
  theme: 'filled',
}
function tl(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? Object(arguments[t]) : {},
      r = Object.keys(n)
    ;(typeof Object.getOwnPropertySymbols == 'function' &&
      (r = r.concat(
        Object.getOwnPropertySymbols(n).filter(function (o) {
          return Object.getOwnPropertyDescriptor(n, o).enumerable
        })
      )),
      r.forEach(function (o) {
        Hm(e, o, n[o])
      }))
  }
  return e
}
function Hm(e, t, n) {
  return (
    t in e
      ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
      : (e[t] = n),
    e
  )
}
var Rn = function (t, n) {
  var r = tl({}, t, n.attrs)
  return w(Ae, tl({}, r, { icon: Lm }), null)
}
Rn.displayName = 'InfoCircleFilled'
Rn.inheritAttrs = !1
var Hy =
  typeof globalThis < 'u'
    ? globalThis
    : typeof window < 'u'
      ? window
      : typeof global < 'u'
        ? global
        : typeof self < 'u'
          ? self
          : {}
function Fm(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, 'default') ? e.default : e
}
let Br = T({}, xn.Modal)
function km(e) {
  e ? (Br = T(T({}, Br), e)) : (Br = T({}, xn.Modal))
}
function Fy() {
  return Br
}
const Mi = 'internalMark',
  zr = be({
    compatConfig: { MODE: 3 },
    name: 'ALocaleProvider',
    props: { locale: { type: Object }, ANT_MARK__: String },
    setup(e, t) {
      let { slots: n } = t
      iu(e.ANT_MARK__ === Mi)
      const r = ct({ antLocale: T(T({}, e.locale), { exist: !0 }), ANT_MARK__: Mi })
      return (
        Ot('localeData', r),
        Fe(
          () => e.locale,
          (o) => {
            ;(km(o && o.Modal), (r.antLocale = T(T({}, o), { exist: !0 })))
          },
          { immediate: !0 }
        ),
        () => {
          var o
          return (o = n.default) === null || o === void 0 ? void 0 : o.call(n)
        }
      )
    },
  })
zr.install = function (e) {
  return (e.component(zr.name, zr), e)
}
const Nm = ss(zr),
  Xu = be({
    name: 'Notice',
    inheritAttrs: !1,
    props: [
      'prefixCls',
      'duration',
      'updateMark',
      'noticeKey',
      'closeIcon',
      'closable',
      'props',
      'onClick',
      'onClose',
      'holder',
      'visible',
    ],
    setup(e, t) {
      let { attrs: n, slots: r } = t,
        o,
        i = !1
      const s = L(() => (e.duration === void 0 ? 4.5 : e.duration)),
        a = () => {
          s.value &&
            !i &&
            (o = setTimeout(() => {
              u()
            }, s.value * 1e3))
        },
        l = () => {
          o && (clearTimeout(o), (o = null))
        },
        u = (f) => {
          ;(f && f.stopPropagation(), l())
          const { onClose: d, noticeKey: p } = e
          d && d(p)
        },
        c = () => {
          ;(l(), a())
        }
      return (
        pr(() => {
          a()
        }),
        Ji(() => {
          ;((i = !0), l())
        }),
        Fe(
          [s, () => e.updateMark, () => e.visible],
          (f, d) => {
            let [p, m, v] = f,
              [b, C, O] = d
            ;(p !== b || m !== C || (v !== O && O)) && c()
          },
          { flush: 'post' }
        ),
        () => {
          var f, d
          const {
              prefixCls: p,
              closable: m,
              closeIcon: v = (f = r.closeIcon) === null || f === void 0 ? void 0 : f.call(r),
              onClick: b,
              holder: C,
            } = e,
            { class: O, style: P } = n,
            x = `${p}-notice`,
            _ = Object.keys(n).reduce(
              (y, E) => (
                (E.startsWith('data-') || E.startsWith('aria-') || E === 'role') && (y[E] = n[E]),
                y
              ),
              {}
            ),
            H = w(
              'div',
              me(
                {
                  class: De(x, O, { [`${x}-closable`]: m }),
                  style: P,
                  onMouseenter: l,
                  onMouseleave: a,
                  onClick: b,
                },
                _
              ),
              [
                w('div', { class: `${x}-content` }, [
                  (d = r.default) === null || d === void 0 ? void 0 : d.call(r),
                ]),
                m
                  ? w('a', { tabindex: 0, onClick: u, class: `${x}-close` }, [
                      v || w('span', { class: `${x}-close-x` }, null),
                    ])
                  : null,
              ]
            )
          return C ? w(Kl, { to: C }, { default: () => H }) : H
        }
      )
    },
  })
var Dm = function (e, t) {
  var n = {}
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
  if (e != null && typeof Object.getOwnPropertySymbols == 'function')
    for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
      t.indexOf(r[o]) < 0 &&
        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
        (n[r[o]] = e[r[o]])
  return n
}
let nl = 0
const Bm = Date.now()
function rl() {
  const e = nl
  return ((nl += 1), `rcNotification_${Bm}_${e}`)
}
const ro = be({
  name: 'Notification',
  inheritAttrs: !1,
  props: ['prefixCls', 'transitionName', 'animation', 'maxCount', 'closeIcon', 'hashId'],
  setup(e, t) {
    let { attrs: n, expose: r, slots: o } = t
    const i = new Map(),
      s = qe([]),
      a = L(() => {
        const { prefixCls: c, animation: f = 'fade' } = e
        let d = e.transitionName
        return (!d && f && (d = `${c}-${f}`), ku(d))
      }),
      l = (c, f) => {
        const d = c.key || rl(),
          p = T(T({}, c), { key: d }),
          { maxCount: m } = e,
          v = s.value.map((C) => C.notice.key).indexOf(d),
          b = s.value.concat()
        ;(v !== -1
          ? b.splice(v, 1, { notice: p, holderCallback: f })
          : (m &&
              s.value.length >= m &&
              ((p.key = b[0].notice.key), (p.updateMark = rl()), (p.userPassKey = d), b.shift()),
            b.push({ notice: p, holderCallback: f })),
          (s.value = b))
      },
      u = (c) => {
        s.value = J(s.value).filter((f) => {
          let {
            notice: { key: d, userPassKey: p },
          } = f
          return (p || d) !== c
        })
      }
    return (
      r({ add: l, remove: u, notices: s }),
      () => {
        var c
        const {
            prefixCls: f,
            closeIcon: d = (c = o.closeIcon) === null || c === void 0
              ? void 0
              : c.call(o, { prefixCls: f }),
          } = e,
          p = s.value.map((v, b) => {
            let { notice: C, holderCallback: O } = v
            const P = b === s.value.length - 1 ? C.updateMark : void 0,
              { key: x, userPassKey: _ } = C,
              { content: H } = C,
              y = T(
                T(
                  T(
                    { prefixCls: f, closeIcon: typeof d == 'function' ? d({ prefixCls: f }) : d },
                    C
                  ),
                  C.props
                ),
                {
                  key: x,
                  noticeKey: _ || x,
                  updateMark: P,
                  onClose: (E) => {
                    var $
                    ;(u(E), ($ = C.onClose) === null || $ === void 0 || $.call(C))
                  },
                  onClick: C.onClick,
                }
              )
            return O
              ? w(
                  'div',
                  {
                    key: x,
                    class: `${f}-hook-holder`,
                    ref: (E) => {
                      typeof x > 'u' || (E ? (i.set(x, E), O(E, y)) : i.delete(x))
                    },
                  },
                  null
                )
              : w(Xu, me(me({}, y), {}, { class: De(y.class, e.hashId) }), {
                  default: () => [typeof H == 'function' ? H({ prefixCls: f }) : H],
                })
          }),
          m = { [f]: 1, [n.class]: !!n.class, [e.hashId]: !0 }
        return w('div', { class: m, style: n.style || { top: '65px', left: '50%' } }, [
          w(Lc, me({ tag: 'div' }, a.value), { default: () => [p] }),
        ])
      }
    )
  },
})
ro.newInstance = function (t, n) {
  const r = t || {},
    {
      name: o = 'notification',
      getContainer: i,
      appContext: s,
      prefixCls: a,
      rootPrefixCls: l,
      transitionName: u,
      hasTransitionName: c,
      useStyle: f,
    } = r,
    d = Dm(r, [
      'name',
      'getContainer',
      'appContext',
      'prefixCls',
      'rootPrefixCls',
      'transitionName',
      'hasTransitionName',
      'useStyle',
    ]),
    p = document.createElement('div')
  i ? i().appendChild(p) : document.body.appendChild(p)
  const v = w(
    be({
      compatConfig: { MODE: 3 },
      name: 'NotificationWrapper',
      setup(b, C) {
        let { attrs: O } = C
        const P = We(),
          x = L(() => xe.getPrefixCls(o, a)),
          [, _] = f(x)
        return (
          pr(() => {
            n({
              notice(H) {
                var y
                ;(y = P.value) === null || y === void 0 || y.add(H)
              },
              removeNotice(H) {
                var y
                ;(y = P.value) === null || y === void 0 || y.remove(H)
              },
              destroy() {
                ;(fa(null, p), p.parentNode && p.parentNode.removeChild(p))
              },
              component: P,
            })
          }),
          () => {
            const H = xe,
              y = H.getRootPrefixCls(l, x.value),
              E = c ? u : `${x.value}-${u}`
            return w(tr, me(me({}, H), {}, { prefixCls: y }), {
              default: () => [
                w(
                  ro,
                  me(
                    me({ ref: P }, O),
                    {},
                    { prefixCls: x.value, transitionName: E, hashId: _.value }
                  ),
                  null
                ),
              ],
            })
          }
        )
      },
    }),
    d
  )
  ;((v.appContext = s || v.appContext), fa(v, p))
}
let ol = 0
const zm = Date.now()
function il() {
  const e = ol
  return ((ol += 1), `rcNotification_${zm}_${e}`)
}
const Wm = be({
  name: 'HookNotification',
  inheritAttrs: !1,
  props: [
    'prefixCls',
    'transitionName',
    'animation',
    'maxCount',
    'closeIcon',
    'hashId',
    'remove',
    'notices',
    'getStyles',
    'getClassName',
    'onAllRemoved',
    'getContainer',
  ],
  setup(e, t) {
    let { attrs: n, slots: r } = t
    const o = new Map(),
      i = L(() => e.notices),
      s = L(() => {
        let c = e.transitionName
        if (!c && e.animation)
          switch (typeof e.animation) {
            case 'string':
              c = e.animation
              break
            case 'function':
              c = e.animation().name
              break
            case 'object':
              c = e.animation.name
              break
            default:
              c = `${e.prefixCls}-fade`
              break
          }
        return ku(c)
      }),
      a = (c) => e.remove(c),
      l = qe({})
    Fe(i, () => {
      const c = {}
      ;(Object.keys(l.value).forEach((f) => {
        c[f] = []
      }),
        e.notices.forEach((f) => {
          const { placement: d = 'topRight' } = f.notice
          d && ((c[d] = c[d] || []), c[d].push(f))
        }),
        (l.value = c))
    })
    const u = L(() => Object.keys(l.value))
    return () => {
      var c
      const {
          prefixCls: f,
          closeIcon: d = (c = r.closeIcon) === null || c === void 0
            ? void 0
            : c.call(r, { prefixCls: f }),
        } = e,
        p = u.value.map((m) => {
          var v, b
          const C = l.value[m],
            O = (v = e.getClassName) === null || v === void 0 ? void 0 : v.call(e, m),
            P = (b = e.getStyles) === null || b === void 0 ? void 0 : b.call(e, m),
            x = C.map((y, E) => {
              let { notice: $, holderCallback: W } = y
              const Y = E === i.value.length - 1 ? $.updateMark : void 0,
                { key: k, userPassKey: ee } = $,
                { content: ae } = $,
                M = T(
                  T(
                    T(
                      { prefixCls: f, closeIcon: typeof d == 'function' ? d({ prefixCls: f }) : d },
                      $
                    ),
                    $.props
                  ),
                  {
                    key: k,
                    noticeKey: ee || k,
                    updateMark: Y,
                    onClose: (B) => {
                      var V
                      ;(a(B), (V = $.onClose) === null || V === void 0 || V.call($))
                    },
                    onClick: $.onClick,
                  }
                )
              return W
                ? w(
                    'div',
                    {
                      key: k,
                      class: `${f}-hook-holder`,
                      ref: (B) => {
                        typeof k > 'u' || (B ? (o.set(k, B), W(B, M)) : o.delete(k))
                      },
                    },
                    null
                  )
                : w(Xu, me(me({}, M), {}, { class: De(M.class, e.hashId) }), {
                    default: () => [typeof ae == 'function' ? ae({ prefixCls: f }) : ae],
                  })
            }),
            _ = { [f]: 1, [`${f}-${m}`]: 1, [n.class]: !!n.class, [e.hashId]: !0, [O]: !!O }
          function H() {
            var y
            C.length > 0 ||
              (Reflect.deleteProperty(l.value, m),
              (y = e.onAllRemoved) === null || y === void 0 || y.call(e))
          }
          return w(
            'div',
            { key: m, class: _, style: n.style || P || { top: '65px', left: '50%' } },
            [
              w(Lc, me(me({ tag: 'div' }, s.value), {}, { onAfterLeave: H }), {
                default: () => [x],
              }),
            ]
          )
        })
      return w(F0, { getContainer: e.getContainer }, { default: () => [p] })
    }
  },
})
var Vm = function (e, t) {
  var n = {}
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
  if (e != null && typeof Object.getOwnPropertySymbols == 'function')
    for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
      t.indexOf(r[o]) < 0 &&
        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
        (n[r[o]] = e[r[o]])
  return n
}
const Um = () => document.body
let sl = 0
function Gm() {
  const e = {}
  for (var t = arguments.length, n = new Array(t), r = 0; r < t; r++) n[r] = arguments[r]
  return (
    n.forEach((o) => {
      o &&
        Object.keys(o).forEach((i) => {
          const s = o[i]
          s !== void 0 && (e[i] = s)
        })
    }),
    e
  )
}
function qu() {
  let e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {}
  const {
      getContainer: t = Um,
      motion: n,
      prefixCls: r,
      maxCount: o,
      getClassName: i,
      getStyles: s,
      onAllRemoved: a,
    } = e,
    l = Vm(e, [
      'getContainer',
      'motion',
      'prefixCls',
      'maxCount',
      'getClassName',
      'getStyles',
      'onAllRemoved',
    ]),
    u = We([]),
    c = We(),
    f = (C, O) => {
      const P = C.key || il(),
        x = T(T({}, C), { key: P }),
        _ = u.value.map((y) => y.notice.key).indexOf(P),
        H = u.value.concat()
      ;(_ !== -1
        ? H.splice(_, 1, { notice: x, holderCallback: O })
        : (o &&
            u.value.length >= o &&
            ((x.key = H[0].notice.key), (x.updateMark = il()), (x.userPassKey = P), H.shift()),
          H.push({ notice: x, holderCallback: O })),
        (u.value = H))
    },
    d = (C) => {
      u.value = u.value.filter((O) => {
        let {
          notice: { key: P, userPassKey: x },
        } = O
        return (x || P) !== C
      })
    },
    p = () => {
      u.value = []
    },
    m = () =>
      w(
        Wm,
        {
          ref: c,
          prefixCls: r,
          maxCount: o,
          notices: u.value,
          remove: d,
          getClassName: i,
          getStyles: s,
          animation: n,
          hashId: e.hashId,
          onAllRemoved: a,
          getContainer: t,
        },
        null
      ),
    v = We([]),
    b = {
      open: (C) => {
        const O = Gm(l, C)
        ;((O.key === null || O.key === void 0) && ((O.key = `vc-notification-${sl}`), (sl += 1)),
          (v.value = [...v.value, { type: 'open', config: O }]))
      },
      close: (C) => {
        v.value = [...v.value, { type: 'close', key: C }]
      },
      destroy: () => {
        v.value = [...v.value, { type: 'destroy' }]
      },
    }
  return (
    Fe(v, () => {
      v.value.length &&
        (v.value.forEach((C) => {
          switch (C.type) {
            case 'open':
              f(C.config)
              break
            case 'close':
              d(C.key)
              break
            case 'destroy':
              p()
              break
          }
        }),
        (v.value = []))
    }),
    [b, m]
  )
}
const Km = (e) => {
    const {
        componentCls: t,
        iconCls: n,
        boxShadowSecondary: r,
        colorBgElevated: o,
        colorSuccess: i,
        colorError: s,
        colorWarning: a,
        colorInfo: l,
        fontSizeLG: u,
        motionEaseInOutCirc: c,
        motionDurationSlow: f,
        marginXS: d,
        paddingXS: p,
        borderRadiusLG: m,
        zIndexPopup: v,
        messageNoticeContentPadding: b,
      } = e,
      C = new Yt('MessageMoveIn', {
        '0%': { padding: 0, transform: 'translateY(-100%)', opacity: 0 },
        '100%': { padding: p, transform: 'translateY(0)', opacity: 1 },
      }),
      O = new Yt('MessageMoveOut', {
        '0%': { maxHeight: e.height, padding: p, opacity: 1 },
        '100%': { maxHeight: 0, padding: 0, opacity: 0 },
      })
    return [
      {
        [t]: T(T({}, xu(e)), {
          position: 'fixed',
          top: d,
          left: '50%',
          transform: 'translateX(-50%)',
          width: '100%',
          pointerEvents: 'none',
          zIndex: v,
          [`${t}-move-up`]: { animationFillMode: 'forwards' },
          [`
        ${t}-move-up-appear,
        ${t}-move-up-enter
      `]: {
            animationName: C,
            animationDuration: f,
            animationPlayState: 'paused',
            animationTimingFunction: c,
          },
          [`
        ${t}-move-up-appear${t}-move-up-appear-active,
        ${t}-move-up-enter${t}-move-up-enter-active
      `]: { animationPlayState: 'running' },
          [`${t}-move-up-leave`]: {
            animationName: O,
            animationDuration: f,
            animationPlayState: 'paused',
            animationTimingFunction: c,
          },
          [`${t}-move-up-leave${t}-move-up-leave-active`]: { animationPlayState: 'running' },
          '&-rtl': { direction: 'rtl', span: { direction: 'rtl' } },
        }),
      },
      {
        [`${t}-notice`]: {
          padding: p,
          textAlign: 'center',
          [n]: { verticalAlign: 'text-bottom', marginInlineEnd: d, fontSize: u },
          [`${t}-notice-content`]: {
            display: 'inline-block',
            padding: b,
            background: o,
            borderRadius: m,
            boxShadow: r,
            pointerEvents: 'all',
          },
          [`${t}-success ${n}`]: { color: i },
          [`${t}-error ${n}`]: { color: s },
          [`${t}-warning ${n}`]: { color: a },
          [`
        ${t}-info ${n},
        ${t}-loading ${n}`]: { color: l },
        },
      },
      { [`${t}-notice-pure-panel`]: { padding: 0, textAlign: 'start' } },
    ]
  },
  Yu = ds(
    'Message',
    (e) => {
      const t = Oo(e, {
        messageNoticeContentPadding: `${(e.controlHeightLG - e.fontSize * e.lineHeight) / 2}px ${e.paddingSM}px`,
      })
      return [Km(t)]
    },
    (e) => ({ height: 150, zIndexPopup: e.zIndexPopupBase + 10 })
  ),
  Xm = {
    info: w(Rn, null, null),
    success: w(In, null, null),
    error: w(Mn, null, null),
    warning: w(jn, null, null),
    loading: w(mr, null, null),
  },
  qm = be({
    name: 'PureContent',
    inheritAttrs: !1,
    props: ['prefixCls', 'type', 'icon'],
    setup(e, t) {
      let { slots: n } = t
      return () => {
        var r
        return w(
          'div',
          { class: De(`${e.prefixCls}-custom-content`, `${e.prefixCls}-${e.type}`) },
          [
            e.icon || Xm[e.type],
            w('span', null, [(r = n.default) === null || r === void 0 ? void 0 : r.call(n)]),
          ]
        )
      }
    },
  })
var Ym = function (e, t) {
  var n = {}
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
  if (e != null && typeof Object.getOwnPropertySymbols == 'function')
    for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
      t.indexOf(r[o]) < 0 &&
        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
        (n[r[o]] = e[r[o]])
  return n
}
const Jm = 8,
  Qm = 3,
  Zm = be({
    name: 'Holder',
    inheritAttrs: !1,
    props: [
      'top',
      'prefixCls',
      'getContainer',
      'maxCount',
      'duration',
      'rtl',
      'transitionName',
      'onAllRemoved',
      'animation',
      'staticGetContainer',
    ],
    setup(e, t) {
      let { expose: n } = t
      var r, o
      const { getPrefixCls: i, getPopupContainer: s } = $o('message', e),
        a = L(() => i('message', e.prefixCls)),
        [, l] = Yu(a),
        u = () => {
          var v
          const b = (v = e.top) !== null && v !== void 0 ? v : Jm
          return {
            left: '50%',
            transform: 'translateX(-50%)',
            top: typeof b == 'number' ? `${b}px` : b,
          }
        },
        c = () => De(l.value, e.rtl ? `${a.value}-rtl` : ''),
        f = () => {
          var v
          return R0({
            prefixCls: a.value,
            animation: (v = e.animation) !== null && v !== void 0 ? v : 'move-up',
            transitionName: e.transitionName,
          })
        },
        d = w('span', { class: `${a.value}-close-x` }, [
          w(vr, { class: `${a.value}-close-icon` }, null),
        ]),
        [p, m] = qu({
          getStyles: u,
          prefixCls: a.value,
          getClassName: c,
          motion: f,
          closable: !1,
          closeIcon: d,
          duration: (r = e.duration) !== null && r !== void 0 ? r : Qm,
          getContainer: (o = e.staticGetContainer) !== null && o !== void 0 ? o : s.value,
          maxCount: e.maxCount,
          onAllRemoved: e.onAllRemoved,
        })
      return (n(T(T({}, p), { prefixCls: a, hashId: l })), m)
    },
  })
let al = 0
function ev(e) {
  const t = We(null),
    n = Symbol('messageHolderKey'),
    r = (l) => {
      var u
      ;(u = t.value) === null || u === void 0 || u.close(l)
    },
    o = (l) => {
      if (!t.value) {
        const _ = () => {}
        return ((_.then = () => {}), _)
      }
      const { open: u, prefixCls: c, hashId: f } = t.value,
        d = `${c}-notice`,
        { content: p, icon: m, type: v, key: b, class: C, onClose: O } = l,
        P = Ym(l, ['content', 'icon', 'type', 'key', 'class', 'onClose'])
      let x = b
      return (
        x == null && ((al += 1), (x = `antd-message-${al}`)),
        vh(
          (_) => (
            u(
              T(T({}, P), {
                key: x,
                content: () =>
                  w(
                    qm,
                    { prefixCls: c, type: v, icon: typeof m == 'function' ? m() : m },
                    { default: () => [typeof p == 'function' ? p() : p] }
                  ),
                placement: 'top',
                class: De(v && `${d}-${v}`, f, C),
                onClose: () => {
                  ;(O?.(), _())
                },
              })
            ),
            () => {
              r(x)
            }
          )
        )
      )
    },
    s = {
      open: o,
      destroy: (l) => {
        var u
        l !== void 0 ? r(l) : (u = t.value) === null || u === void 0 || u.destroy()
      },
    }
  return (
    ['info', 'success', 'warning', 'error', 'loading'].forEach((l) => {
      const u = (c, f, d) => {
        let p
        c && typeof c == 'object' && 'content' in c ? (p = c) : (p = { content: c })
        let m, v
        typeof f == 'function' ? (v = f) : ((m = f), (v = d))
        const b = T(T({ onClose: v, duration: m }, p), { type: l })
        return o(b)
      }
      s[l] = u
    }),
    [s, () => w(Zm, me(me({ key: n }, e), {}, { ref: t }), null)]
  )
}
function tv(e) {
  return ev(e)
}
let Ju = 3,
  Qu,
  $e,
  nv = 1,
  Zu = '',
  ef = 'move-up',
  tf = !1,
  nf = () => document.body,
  rf,
  of = !1
function rv() {
  return nv++
}
function ov(e) {
  ;(e.top !== void 0 && ((Qu = e.top), ($e = null)),
    e.duration !== void 0 && (Ju = e.duration),
    e.prefixCls !== void 0 && (Zu = e.prefixCls),
    e.getContainer !== void 0 && ((nf = e.getContainer), ($e = null)),
    e.transitionName !== void 0 && ((ef = e.transitionName), ($e = null), (tf = !0)),
    e.maxCount !== void 0 && ((rf = e.maxCount), ($e = null)),
    e.rtl !== void 0 && (of = e.rtl))
}
function iv(e, t) {
  if ($e) {
    t($e)
    return
  }
  ro.newInstance(
    {
      appContext: e.appContext,
      prefixCls: e.prefixCls || Zu,
      rootPrefixCls: e.rootPrefixCls,
      transitionName: ef,
      hasTransitionName: tf,
      style: { top: Qu },
      getContainer: nf || e.getPopupContainer,
      maxCount: rf,
      name: 'message',
      useStyle: Yu,
    },
    (n) => {
      if ($e) {
        t($e)
        return
      }
      ;(($e = n), t(n))
    }
  )
}
const sf = { info: Rn, success: In, error: Mn, warning: jn, loading: mr },
  sv = Object.keys(sf)
function av(e) {
  const t = e.duration !== void 0 ? e.duration : Ju,
    n = e.key || rv(),
    r = new Promise((i) => {
      const s = () => (typeof e.onClose == 'function' && e.onClose(), i(!0))
      iv(e, (a) => {
        a.notice({
          key: n,
          duration: t,
          style: e.style || {},
          class: e.class,
          content: (l) => {
            let { prefixCls: u } = l
            const c = sf[e.type],
              f = c ? w(c, null, null) : '',
              d = De(`${u}-custom-content`, { [`${u}-${e.type}`]: e.type, [`${u}-rtl`]: of === !0 })
            return w('div', { class: d }, [
              typeof e.icon == 'function' ? e.icon() : e.icon || f,
              w('span', null, [typeof e.content == 'function' ? e.content() : e.content]),
            ])
          },
          onClose: s,
          onClick: e.onClick,
        })
      })
    }),
    o = () => {
      $e && $e.removeNotice(n)
    }
  return ((o.then = (i, s) => r.then(i, s)), (o.promise = r), o)
}
function lv(e) {
  return Object.prototype.toString.call(e) === '[object Object]' && !!e.content
}
const fr = {
  open: av,
  config: ov,
  destroy(e) {
    if ($e)
      if (e) {
        const { removeNotice: t } = $e
        t(e)
      } else {
        const { destroy: t } = $e
        ;(t(), ($e = null))
      }
  },
}
function cv(e, t) {
  e[t] = (n, r, o) =>
    lv(n)
      ? e.open(T(T({}, n), { type: t }))
      : (typeof r == 'function' && ((o = r), (r = void 0)),
        e.open({ content: n, duration: r, type: t, onClose: o }))
}
sv.forEach((e) => cv(fr, e))
fr.warn = fr.warning
fr.useMessage = tv
const uv = (e) => {
    const { componentCls: t, width: n, notificationMarginEdge: r } = e,
      o = new Yt('antNotificationTopFadeIn', {
        '0%': { marginTop: '-100%', opacity: 0 },
        '100%': { marginTop: 0, opacity: 1 },
      }),
      i = new Yt('antNotificationBottomFadeIn', {
        '0%': { marginBottom: '-100%', opacity: 0 },
        '100%': { marginBottom: 0, opacity: 1 },
      }),
      s = new Yt('antNotificationLeftFadeIn', {
        '0%': { right: { _skip_check_: !0, value: n }, opacity: 0 },
        '100%': { right: { _skip_check_: !0, value: 0 }, opacity: 1 },
      })
    return {
      [`&${t}-top, &${t}-bottom`]: { marginInline: 0 },
      [`&${t}-top`]: {
        [`${t}-fade-enter${t}-fade-enter-active, ${t}-fade-appear${t}-fade-appear-active`]: {
          animationName: o,
        },
      },
      [`&${t}-bottom`]: {
        [`${t}-fade-enter${t}-fade-enter-active, ${t}-fade-appear${t}-fade-appear-active`]: {
          animationName: i,
        },
      },
      [`&${t}-topLeft, &${t}-bottomLeft`]: {
        marginInlineEnd: 0,
        marginInlineStart: r,
        [`${t}-fade-enter${t}-fade-enter-active, ${t}-fade-appear${t}-fade-appear-active`]: {
          animationName: s,
        },
      },
    }
  },
  fv = (e) => {
    const {
        iconCls: t,
        componentCls: n,
        boxShadowSecondary: r,
        fontSizeLG: o,
        notificationMarginBottom: i,
        borderRadiusLG: s,
        colorSuccess: a,
        colorInfo: l,
        colorWarning: u,
        colorError: c,
        colorTextHeading: f,
        notificationBg: d,
        notificationPadding: p,
        notificationMarginEdge: m,
        motionDurationMid: v,
        motionEaseInOut: b,
        fontSize: C,
        lineHeight: O,
        width: P,
        notificationIconSize: x,
      } = e,
      _ = `${n}-notice`,
      H = new Yt('antNotificationFadeIn', {
        '0%': { left: { _skip_check_: !0, value: P }, opacity: 0 },
        '100%': { left: { _skip_check_: !0, value: 0 }, opacity: 1 },
      }),
      y = new Yt('antNotificationFadeOut', {
        '0%': { maxHeight: e.animationMaxHeight, marginBottom: i, opacity: 1 },
        '100%': { maxHeight: 0, marginBottom: 0, paddingTop: 0, paddingBottom: 0, opacity: 0 },
      })
    return [
      {
        [n]: T(
          T(
            T(T({}, xu(e)), {
              position: 'fixed',
              zIndex: e.zIndexPopup,
              marginInlineEnd: m,
              [`${n}-hook-holder`]: { position: 'relative' },
              [`&${n}-top, &${n}-bottom`]: { [`${n}-notice`]: { marginInline: 'auto auto' } },
              [`&${n}-topLeft, &${n}-bottomLeft`]: {
                [`${n}-notice`]: { marginInlineEnd: 'auto', marginInlineStart: 0 },
              },
              [`${n}-fade-enter, ${n}-fade-appear`]: {
                animationDuration: e.motionDurationMid,
                animationTimingFunction: b,
                animationFillMode: 'both',
                opacity: 0,
                animationPlayState: 'paused',
              },
              [`${n}-fade-leave`]: {
                animationTimingFunction: b,
                animationFillMode: 'both',
                animationDuration: v,
                animationPlayState: 'paused',
              },
              [`${n}-fade-enter${n}-fade-enter-active, ${n}-fade-appear${n}-fade-appear-active`]: {
                animationName: H,
                animationPlayState: 'running',
              },
              [`${n}-fade-leave${n}-fade-leave-active`]: {
                animationName: y,
                animationPlayState: 'running',
              },
            }),
            uv(e)
          ),
          { '&-rtl': { direction: 'rtl', [`${n}-notice-btn`]: { float: 'left' } } }
        ),
      },
      {
        [_]: {
          position: 'relative',
          width: P,
          maxWidth: `calc(100vw - ${m * 2}px)`,
          marginBottom: i,
          marginInlineStart: 'auto',
          padding: p,
          overflow: 'hidden',
          lineHeight: O,
          wordWrap: 'break-word',
          background: d,
          borderRadius: s,
          boxShadow: r,
          [`${n}-close-icon`]: { fontSize: C, cursor: 'pointer' },
          [`${_}-message`]: {
            marginBottom: e.marginXS,
            color: f,
            fontSize: o,
            lineHeight: e.lineHeightLG,
          },
          [`${_}-description`]: { fontSize: C },
          [`&${_}-closable ${_}-message`]: { paddingInlineEnd: e.paddingLG },
          [`${_}-with-icon ${_}-message`]: {
            marginBottom: e.marginXS,
            marginInlineStart: e.marginSM + x,
            fontSize: o,
          },
          [`${_}-with-icon ${_}-description`]: { marginInlineStart: e.marginSM + x, fontSize: C },
          [`${_}-icon`]: {
            position: 'absolute',
            fontSize: x,
            lineHeight: 0,
            [`&-success${t}`]: { color: a },
            [`&-info${t}`]: { color: l },
            [`&-warning${t}`]: { color: u },
            [`&-error${t}`]: { color: c },
          },
          [`${_}-close`]: {
            position: 'absolute',
            top: e.notificationPaddingVertical,
            insetInlineEnd: e.notificationPaddingHorizontal,
            color: e.colorIcon,
            outline: 'none',
            width: e.notificationCloseButtonSize,
            height: e.notificationCloseButtonSize,
            borderRadius: e.borderRadiusSM,
            transition: `background-color ${e.motionDurationMid}, color ${e.motionDurationMid}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            '&:hover': {
              color: e.colorIconHover,
              backgroundColor: e.wireframe ? 'transparent' : e.colorFillContent,
            },
          },
          [`${_}-btn`]: { float: 'right', marginTop: e.marginSM },
        },
      },
      { [`${_}-pure-panel`]: { margin: 0 } },
    ]
  },
  af = ds(
    'Notification',
    (e) => {
      const t = e.paddingMD,
        n = e.paddingLG,
        r = Oo(e, {
          notificationBg: e.colorBgElevated,
          notificationPaddingVertical: t,
          notificationPaddingHorizontal: n,
          notificationPadding: `${e.paddingMD}px ${e.paddingContentHorizontalLG}px`,
          notificationMarginBottom: e.margin,
          notificationMarginEdge: e.marginLG,
          animationMaxHeight: 150,
          notificationIconSize: e.fontSizeLG * e.lineHeightLG,
          notificationCloseButtonSize: e.controlHeightLG * 0.55,
        })
      return [fv(r)]
    },
    (e) => ({ zIndexPopup: e.zIndexPopupBase + 50, width: 384 })
  )
function dv(e, t) {
  return t || w('span', { class: `${e}-close-x` }, [w(vr, { class: `${e}-close-icon` }, null)])
}
;(w(Rn, null, null), w(In, null, null), w(Mn, null, null), w(jn, null, null), w(mr, null, null))
const pv = { success: In, info: Rn, error: Mn, warning: jn }
function hv(e) {
  let { prefixCls: t, icon: n, type: r, message: o, description: i, btn: s } = e,
    a = null
  if (n) a = w('span', { class: `${t}-icon` }, [un(n)])
  else if (r) {
    const l = pv[r]
    a = w(l, { class: `${t}-icon ${t}-icon-${r}` }, null)
  }
  return w('div', { class: De({ [`${t}-with-icon`]: a }), role: 'alert' }, [
    a,
    w('div', { class: `${t}-message` }, [o]),
    w('div', { class: `${t}-description` }, [i]),
    s && w('div', { class: `${t}-btn` }, [s]),
  ])
}
function lf(e, t, n) {
  let r
  switch (
    ((t = typeof t == 'number' ? `${t}px` : t), (n = typeof n == 'number' ? `${n}px` : n), e)
  ) {
    case 'top':
      r = { left: '50%', transform: 'translateX(-50%)', right: 'auto', top: t, bottom: 'auto' }
      break
    case 'topLeft':
      r = { left: 0, top: t, bottom: 'auto' }
      break
    case 'topRight':
      r = { right: 0, top: t, bottom: 'auto' }
      break
    case 'bottom':
      r = { left: '50%', transform: 'translateX(-50%)', right: 'auto', top: 'auto', bottom: n }
      break
    case 'bottomLeft':
      r = { left: 0, top: 'auto', bottom: n }
      break
    default:
      r = { right: 0, top: 'auto', bottom: n }
      break
  }
  return r
}
function gv(e) {
  return { name: `${e}-fade` }
}
var mv = function (e, t) {
  var n = {}
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
  if (e != null && typeof Object.getOwnPropertySymbols == 'function')
    for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
      t.indexOf(r[o]) < 0 &&
        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
        (n[r[o]] = e[r[o]])
  return n
}
const ll = 24,
  vv = 4.5,
  yv = be({
    name: 'Holder',
    inheritAttrs: !1,
    props: ['prefixCls', 'class', 'type', 'icon', 'content', 'onAllRemoved'],
    setup(e, t) {
      let { expose: n } = t
      const { getPrefixCls: r, getPopupContainer: o } = $o('notification', e),
        i = L(() => e.prefixCls || r('notification')),
        s = (d) => {
          var p, m
          return lf(
            d,
            (p = e.top) !== null && p !== void 0 ? p : ll,
            (m = e.bottom) !== null && m !== void 0 ? m : ll
          )
        },
        [, a] = af(i),
        l = () => De(a.value, { [`${i.value}-rtl`]: e.rtl }),
        u = () => gv(i.value),
        [c, f] = qu({
          prefixCls: i.value,
          getStyles: s,
          getClassName: l,
          motion: u,
          closable: !0,
          closeIcon: dv(i.value),
          duration: vv,
          getContainer: () => {
            var d, p
            return (
              ((d = e.getPopupContainer) === null || d === void 0 ? void 0 : d.call(e)) ||
              ((p = o.value) === null || p === void 0 ? void 0 : p.call(o)) ||
              document.body
            )
          },
          maxCount: e.maxCount,
          hashId: a.value,
          onAllRemoved: e.onAllRemoved,
        })
      return (n(T(T({}, c), { prefixCls: i.value, hashId: a })), f)
    },
  })
function bv(e) {
  const t = We(null),
    n = Symbol('notificationHolderKey'),
    r = (a) => {
      if (!t.value) return
      const { open: l, prefixCls: u, hashId: c } = t.value,
        f = `${u}-notice`,
        { message: d, description: p, icon: m, type: v, btn: b, class: C } = a,
        O = mv(a, ['message', 'description', 'icon', 'type', 'btn', 'class'])
      return l(
        T(T({ placement: 'topRight' }, O), {
          content: () =>
            w(
              hv,
              {
                prefixCls: f,
                icon: typeof m == 'function' ? m() : m,
                type: v,
                message: typeof d == 'function' ? d() : d,
                description: typeof p == 'function' ? p() : p,
                btn: typeof b == 'function' ? b() : b,
              },
              null
            ),
          class: De(v && `${f}-${v}`, c, C),
        })
      )
    },
    i = {
      open: r,
      destroy: (a) => {
        var l, u
        a !== void 0
          ? (l = t.value) === null || l === void 0 || l.close(a)
          : (u = t.value) === null || u === void 0 || u.destroy()
      },
    }
  return (
    ['success', 'info', 'warning', 'error'].forEach((a) => {
      i[a] = (l) => r(T(T({}, l), { type: a }))
    }),
    [i, () => w(yv, me(me({ key: n }, e), {}, { ref: t }), null)]
  )
}
function Cv(e) {
  return bv(e)
}
const Vt = {}
let cf = 4.5,
  uf = '24px',
  ff = '24px',
  Ii = '',
  df = 'topRight',
  pf = () => document.body,
  hf = null,
  ji = !1,
  gf
function xv(e) {
  const {
    duration: t,
    placement: n,
    bottom: r,
    top: o,
    getContainer: i,
    closeIcon: s,
    prefixCls: a,
  } = e
  ;(a !== void 0 && (Ii = a),
    t !== void 0 && (cf = t),
    n !== void 0 && (df = n),
    r !== void 0 && (ff = typeof r == 'number' ? `${r}px` : r),
    o !== void 0 && (uf = typeof o == 'number' ? `${o}px` : o),
    i !== void 0 && (pf = i),
    s !== void 0 && (hf = s),
    e.rtl !== void 0 && (ji = e.rtl),
    e.maxCount !== void 0 && (gf = e.maxCount))
}
function Sv(e, t) {
  let {
    prefixCls: n,
    placement: r = df,
    getContainer: o = pf,
    top: i,
    bottom: s,
    closeIcon: a = hf,
    appContext: l,
  } = e
  const { getPrefixCls: u } = Rv(),
    c = u('notification', n || Ii),
    f = `${c}-${r}-${ji}`,
    d = Vt[f]
  if (d) {
    Promise.resolve(d).then((m) => {
      t(m)
    })
    return
  }
  const p = De(`${c}-${r}`, { [`${c}-rtl`]: ji === !0 })
  ro.newInstance(
    {
      name: 'notification',
      prefixCls: n || Ii,
      useStyle: af,
      class: p,
      style: lf(r, i ?? uf, s ?? ff),
      appContext: l,
      getContainer: o,
      closeIcon: (m) => {
        let { prefixCls: v } = m
        return w('span', { class: `${v}-close-x` }, [
          un(a, {}, w(vr, { class: `${v}-close-icon` }, null)),
        ])
      },
      maxCount: gf,
      hasTransitionName: !0,
    },
    (m) => {
      ;((Vt[f] = m), t(m))
    }
  )
}
const _v = { success: ys, info: Cs, error: xs, warning: bs }
function wv(e) {
  const { icon: t, type: n, description: r, message: o, btn: i } = e,
    s = e.duration === void 0 ? cf : e.duration
  Sv(e, (a) => {
    a.notice({
      content: (l) => {
        let { prefixCls: u } = l
        const c = `${u}-notice`
        let f = null
        if (t) f = () => w('span', { class: `${c}-icon` }, [un(t)])
        else if (n) {
          const d = _v[n]
          f = () => w(d, { class: `${c}-icon ${c}-icon-${n}` }, null)
        }
        return w('div', { class: f ? `${c}-with-icon` : '' }, [
          f && f(),
          w('div', { class: `${c}-message` }, [
            !r && f ? w('span', { class: `${c}-message-single-line-auto-margin` }, null) : null,
            un(o),
          ]),
          w('div', { class: `${c}-description` }, [un(r)]),
          i ? w('span', { class: `${c}-btn` }, [un(i)]) : null,
        ])
      },
      duration: s,
      closable: !0,
      onClose: e.onClose,
      onClick: e.onClick,
      key: e.key,
      style: e.style || {},
      class: e.class,
    })
  })
}
const $n = {
    open: wv,
    close(e) {
      Object.keys(Vt).forEach((t) =>
        Promise.resolve(Vt[t]).then((n) => {
          n.removeNotice(e)
        })
      )
    },
    config: xv,
    destroy() {
      Object.keys(Vt).forEach((e) => {
        ;(Promise.resolve(Vt[e]).then((t) => {
          t.destroy()
        }),
          delete Vt[e])
      })
    },
  },
  Ov = ['success', 'info', 'warning', 'error']
Ov.forEach((e) => {
  $n[e] = (t) => $n.open(T(T({}, t), { type: e }))
})
$n.warn = $n.warning
$n.useNotification = Cv
const Tv = `-ant-${Date.now()}-${Math.random()}`
function $v(e, t) {
  const n = {},
    r = (s, a) => {
      let l = s.clone()
      return ((l = a?.(l) || l), l.toRgbString())
    },
    o = (s, a) => {
      const l = new ve(s),
        u = en(l.toRgbString())
      ;((n[`${a}-color`] = r(l)),
        (n[`${a}-color-disabled`] = u[1]),
        (n[`${a}-color-hover`] = u[4]),
        (n[`${a}-color-active`] = u[6]),
        (n[`${a}-color-outline`] = l.clone().setAlpha(0.2).toRgbString()),
        (n[`${a}-color-deprecated-bg`] = u[0]),
        (n[`${a}-color-deprecated-border`] = u[2]))
    }
  if (t.primaryColor) {
    o(t.primaryColor, 'primary')
    const s = new ve(t.primaryColor),
      a = en(s.toRgbString())
    ;(a.forEach((u, c) => {
      n[`primary-${c + 1}`] = u
    }),
      (n['primary-color-deprecated-l-35'] = r(s, (u) => u.lighten(35))),
      (n['primary-color-deprecated-l-20'] = r(s, (u) => u.lighten(20))),
      (n['primary-color-deprecated-t-20'] = r(s, (u) => u.tint(20))),
      (n['primary-color-deprecated-t-50'] = r(s, (u) => u.tint(50))),
      (n['primary-color-deprecated-f-12'] = r(s, (u) => u.setAlpha(u.getAlpha() * 0.12))))
    const l = new ve(a[0])
    ;((n['primary-color-active-deprecated-f-30'] = r(l, (u) => u.setAlpha(u.getAlpha() * 0.3))),
      (n['primary-color-active-deprecated-d-02'] = r(l, (u) => u.darken(2))))
  }
  return (
    t.successColor && o(t.successColor, 'success'),
    t.warningColor && o(t.warningColor, 'warning'),
    t.errorColor && o(t.errorColor, 'error'),
    t.infoColor && o(t.infoColor, 'info'),
    `
  :root {
    ${Object.keys(n).map((s) => `--${e}-${s}: ${n[s]};`).join(`
`)}
  }
  `.trim()
  )
}
function Pv(e, t) {
  const n = $v(e, t)
  En() && eo(n, `${Tv}-dynamic-theme`)
}
const Ev = (e) => {
  const [t, n] = To()
  return _i(
    L(() => ({ theme: t.value, token: n.value, hashId: '', path: ['ant-design-icons', e.value] })),
    () => [
      {
        [`.${e.value}`]: T(T({}, Zg()), { [`.${e.value} .${e.value}-icon`]: { display: 'block' } }),
      },
    ]
  )
}
function Av(e, t) {
  const n = L(() => e?.value || {}),
    r = L(() => (n.value.inherit === !1 || !t?.value ? _u : t.value))
  return L(() => {
    if (!e?.value) return t?.value
    const i = T({}, r.value.components)
    return (
      Object.keys(e.value.components || {}).forEach((s) => {
        i[s] = T(T({}, i[s]), e.value.components[s])
      }),
      T(T(T({}, r.value), n.value), {
        token: T(T({}, r.value.token), n.value.token),
        components: i,
      })
    )
  })
}
var Mv = function (e, t) {
  var n = {}
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
  if (e != null && typeof Object.getOwnPropertySymbols == 'function')
    for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
      t.indexOf(r[o]) < 0 &&
        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
        (n[r[o]] = e[r[o]])
  return n
}
const Iv = 'ant'
function yn() {
  return xe.prefixCls || Iv
}
function mf() {
  return xe.iconPrefixCls || as
}
const Ss = ct({}),
  xe = ct({})
mo(() => {
  ;(T(xe, Ss),
    (xe.prefixCls = yn()),
    (xe.iconPrefixCls = mf()),
    (xe.getPrefixCls = (e, t) => t || (e ? `${xe.prefixCls}-${e}` : xe.prefixCls)),
    (xe.getRootPrefixCls = () => (xe.prefixCls ? xe.prefixCls : yn())))
})
let ei
const jv = (e) => {
    ;(ei && ei(),
      (ei = mo(() => {
        ;(T(Ss, ct(e)), T(xe, ct(e)))
      })),
      e.theme && Pv(yn(), e.theme))
  },
  Rv = () => ({
    getPrefixCls: (e, t) => t || (e ? `${yn()}-${e}` : yn()),
    getIconPrefixCls: mf,
    getRootPrefixCls: () => (xe.prefixCls ? xe.prefixCls : yn()),
  }),
  tr = be({
    compatConfig: { MODE: 3 },
    name: 'AConfigProvider',
    inheritAttrs: !1,
    props: Th(),
    setup(e, t) {
      let { slots: n } = t
      const r = Uc(),
        o = (M, B) => {
          const { prefixCls: V = 'ant' } = e
          if (B) return B
          const Q = V || r.getPrefixCls('')
          return M ? `${Q}-${M}` : Q
        },
        i = L(() => e.iconPrefixCls || r.iconPrefixCls.value || as),
        s = L(() => i.value !== r.iconPrefixCls.value),
        a = L(() => {
          var M
          return e.csp || ((M = r.csp) === null || M === void 0 ? void 0 : M.value)
        }),
        l = Ev(i),
        u = Av(
          L(() => e.theme),
          L(() => {
            var M
            return (M = r.theme) === null || M === void 0 ? void 0 : M.value
          })
        ),
        c = (M) => (e.renderEmpty || n.renderEmpty || r.renderEmpty || d0)(M),
        f = L(() => {
          var M, B
          return (M = e.autoInsertSpaceInButton) !== null && M !== void 0
            ? M
            : (B = r.autoInsertSpaceInButton) === null || B === void 0
              ? void 0
              : B.value
        }),
        d = L(() => {
          var M
          return e.locale || ((M = r.locale) === null || M === void 0 ? void 0 : M.value)
        })
      Fe(
        d,
        () => {
          Ss.locale = d.value
        },
        { immediate: !0 }
      )
      const p = L(() => {
          var M
          return e.direction || ((M = r.direction) === null || M === void 0 ? void 0 : M.value)
        }),
        m = L(() => {
          var M, B
          return (M = e.space) !== null && M !== void 0
            ? M
            : (B = r.space) === null || B === void 0
              ? void 0
              : B.value
        }),
        v = L(() => {
          var M, B
          return (M = e.virtual) !== null && M !== void 0
            ? M
            : (B = r.virtual) === null || B === void 0
              ? void 0
              : B.value
        }),
        b = L(() => {
          var M, B
          return (M = e.dropdownMatchSelectWidth) !== null && M !== void 0
            ? M
            : (B = r.dropdownMatchSelectWidth) === null || B === void 0
              ? void 0
              : B.value
        }),
        C = L(() => {
          var M
          return e.getTargetContainer !== void 0
            ? e.getTargetContainer
            : (M = r.getTargetContainer) === null || M === void 0
              ? void 0
              : M.value
        }),
        O = L(() => {
          var M
          return e.getPopupContainer !== void 0
            ? e.getPopupContainer
            : (M = r.getPopupContainer) === null || M === void 0
              ? void 0
              : M.value
        }),
        P = L(() => {
          var M
          return e.pageHeader !== void 0
            ? e.pageHeader
            : (M = r.pageHeader) === null || M === void 0
              ? void 0
              : M.value
        }),
        x = L(() => {
          var M
          return e.input !== void 0
            ? e.input
            : (M = r.input) === null || M === void 0
              ? void 0
              : M.value
        }),
        _ = L(() => {
          var M
          return e.pagination !== void 0
            ? e.pagination
            : (M = r.pagination) === null || M === void 0
              ? void 0
              : M.value
        }),
        H = L(() => {
          var M
          return e.form !== void 0
            ? e.form
            : (M = r.form) === null || M === void 0
              ? void 0
              : M.value
        }),
        y = L(() => {
          var M
          return e.select !== void 0
            ? e.select
            : (M = r.select) === null || M === void 0
              ? void 0
              : M.value
        }),
        E = L(() => e.componentSize),
        $ = L(() => e.componentDisabled),
        W = L(() => {
          var M, B
          return (M = e.wave) !== null && M !== void 0
            ? M
            : (B = r.wave) === null || B === void 0
              ? void 0
              : B.value
        }),
        Y = {
          csp: a,
          autoInsertSpaceInButton: f,
          locale: d,
          direction: p,
          space: m,
          virtual: v,
          dropdownMatchSelectWidth: b,
          getPrefixCls: o,
          iconPrefixCls: i,
          theme: L(() => {
            var M, B
            return (M = u.value) !== null && M !== void 0
              ? M
              : (B = r.theme) === null || B === void 0
                ? void 0
                : B.value
          }),
          renderEmpty: c,
          getTargetContainer: C,
          getPopupContainer: O,
          pageHeader: P,
          input: x,
          pagination: _,
          form: H,
          select: y,
          componentSize: E,
          componentDisabled: $,
          transformCellText: L(() => e.transformCellText),
          wave: W,
        },
        k = L(() => {
          const M = u.value || {},
            { algorithm: B, token: V } = M,
            Q = Mv(M, ['algorithm', 'token']),
            Ge = B && (!Array.isArray(B) || B.length > 0) ? au(B) : void 0
          return T(T({}, Q), { theme: Ge, token: T(T({}, wo), V) })
        }),
        ee = L(() => {
          var M, B
          let V = {}
          return (
            d.value &&
              (V =
                ((M = d.value.Form) === null || M === void 0
                  ? void 0
                  : M.defaultValidateMessages) ||
                ((B = xn.Form) === null || B === void 0 ? void 0 : B.defaultValidateMessages) ||
                {}),
            e.form && e.form.validateMessages && (V = T(T({}, V), e.form.validateMessages)),
            V
          )
        })
      ;($h(Y), Oh({ validateMessages: ee }), p0(E), Ph($))
      const ae = (M) => {
        var B, V
        let Q = s.value
          ? l((B = n.default) === null || B === void 0 ? void 0 : B.call(n))
          : (V = n.default) === null || V === void 0
            ? void 0
            : V.call(n)
        if (e.theme) {
          const Ge = (function () {
            return Q
          })()
          Q = w(a0, { value: k.value }, { default: () => [Ge] })
        }
        return w(Nm, { locale: d.value || M, ANT_MARK__: Mi }, { default: () => [Q] })
      }
      return (
        mo(() => {
          p.value && (fr.config({ rtl: p.value === 'rtl' }), $n.config({ rtl: p.value === 'rtl' }))
        }),
        () => w(qc, { children: (M, B, V) => ae(V) }, null)
      )
    },
  })
tr.config = jv
tr.install = function (e) {
  e.component(tr.name, tr)
}
const ky = (e, t) => {
    const n = e.__vccOpts || e
    for (const [r, o] of t) n[r] = o
    return n
  },
  Lv = 'useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict'
let Ny = (e = 21) => {
  let t = '',
    n = crypto.getRandomValues(new Uint8Array((e |= 0)))
  for (; e--; ) t += Lv[n[e] & 63]
  return t
}
var Hv = ((e) => (
    (e.InterruptSpeech = 'InterruptSpeech'),
    (e.ErrorReceived = 'ErrorReceived'),
    (e.MessageReceived = 'MessageReceived'),
    (e.SignalReceived = 'SignalReceived'),
    (e.StartSpeech = 'StartSpeech'),
    (e.EndSpeech = 'EndSpeech'),
    (e.StateChanged = 'StateChanged'),
    e
  ))(Hv || {}),
  Fv = ((e) => (
    (e.InitializeAvatarSession = 'InitializeAvatarSession'),
    (e.SendHumanAudio = 'SendHumanAudio'),
    (e.SendHumanVideo = 'SendHumanVideo'),
    (e.SendHumanText = 'SendHumanText'),
    (e.TriggerHeartbeat = 'TriggerHeartbeat'),
    (e.Interrupt = 'Interrupt'),
    (e.EndSpeech = 'EndSpeech'),
    (e.AvatarSessionInitialized = 'AvatarSessionInitialized'),
    (e.EchoHumanText = 'EchoHumanText'),
    (e.EchoAvatarText = 'EchoAvatarText'),
    (e.EchoAvatarAudio = 'EchoAvatarAudio'),
    (e.EchoHumanAudio = 'EchoHumanAudio'),
    (e.AvatarHeartbeat = 'AvatarHeartbeat'),
    (e.MotionDataWelcome = 'MotionDataWelcome'),
    (e.MotionData = 'MotionData'),
    (e.Error = 'Error'),
    (e.InterruptAccepted = 'InterruptAccepted'),
    (e.InterruptNotification = 'InterruptNotification'),
    (e.ChatSignal = 'ChatSignal'),
    e
  ))(Fv || {}),
  cn = ((e) => (
    (e.WS_CLOSE = 'WS_CLOSE'),
    (e.WS_ERROR = 'WS_ERROR'),
    (e.WS_MESSAGE = 'WS_MESSAGE'),
    (e.WS_OPEN = 'WS_OPEN'),
    e
  ))(cn || {}),
  kv = ((e) => (
    (e.Player_EndSpeaking = 'Player_EndSpeaking'),
    (e.Player_NoLegacy = 'Player_NoLegacy'),
    (e.Player_StartSpeaking = 'Player_StartSpeaking'),
    (e.Player_WaitNextAudioClip = 'Player_WaitNextAudioClip'),
    e
  ))(kv || {}),
  Nv = ((e) => (
    (e.Change_Status = 'Change_Status'),
    (e.Chat_BinsizeError = 'Chat_BinsizeError'),
    e
  ))(Nv || {}),
  ti = { exports: {} },
  cl
function Dv() {
  return (
    cl ||
      ((cl = 1),
      (function (e) {
        var t = Object.prototype.hasOwnProperty,
          n = '~'
        function r() {}
        Object.create && ((r.prototype = Object.create(null)), new r().__proto__ || (n = !1))
        function o(l, u, c) {
          ;((this.fn = l), (this.context = u), (this.once = c || !1))
        }
        function i(l, u, c, f, d) {
          if (typeof c != 'function') throw new TypeError('The listener must be a function')
          var p = new o(c, f || l, d),
            m = n ? n + u : u
          return (
            l._events[m]
              ? l._events[m].fn
                ? (l._events[m] = [l._events[m], p])
                : l._events[m].push(p)
              : ((l._events[m] = p), l._eventsCount++),
            l
          )
        }
        function s(l, u) {
          --l._eventsCount === 0 ? (l._events = new r()) : delete l._events[u]
        }
        function a() {
          ;((this._events = new r()), (this._eventsCount = 0))
        }
        ;((a.prototype.eventNames = function () {
          var u = [],
            c,
            f
          if (this._eventsCount === 0) return u
          for (f in (c = this._events)) t.call(c, f) && u.push(n ? f.slice(1) : f)
          return Object.getOwnPropertySymbols ? u.concat(Object.getOwnPropertySymbols(c)) : u
        }),
          (a.prototype.listeners = function (u) {
            var c = n ? n + u : u,
              f = this._events[c]
            if (!f) return []
            if (f.fn) return [f.fn]
            for (var d = 0, p = f.length, m = new Array(p); d < p; d++) m[d] = f[d].fn
            return m
          }),
          (a.prototype.listenerCount = function (u) {
            var c = n ? n + u : u,
              f = this._events[c]
            return f ? (f.fn ? 1 : f.length) : 0
          }),
          (a.prototype.emit = function (u, c, f, d, p, m) {
            var v = n ? n + u : u
            if (!this._events[v]) return !1
            var b = this._events[v],
              C = arguments.length,
              O,
              P
            if (b.fn) {
              switch ((b.once && this.removeListener(u, b.fn, void 0, !0), C)) {
                case 1:
                  return (b.fn.call(b.context), !0)
                case 2:
                  return (b.fn.call(b.context, c), !0)
                case 3:
                  return (b.fn.call(b.context, c, f), !0)
                case 4:
                  return (b.fn.call(b.context, c, f, d), !0)
                case 5:
                  return (b.fn.call(b.context, c, f, d, p), !0)
                case 6:
                  return (b.fn.call(b.context, c, f, d, p, m), !0)
              }
              for (P = 1, O = new Array(C - 1); P < C; P++) O[P - 1] = arguments[P]
              b.fn.apply(b.context, O)
            } else {
              var x = b.length,
                _
              for (P = 0; P < x; P++)
                switch ((b[P].once && this.removeListener(u, b[P].fn, void 0, !0), C)) {
                  case 1:
                    b[P].fn.call(b[P].context)
                    break
                  case 2:
                    b[P].fn.call(b[P].context, c)
                    break
                  case 3:
                    b[P].fn.call(b[P].context, c, f)
                    break
                  case 4:
                    b[P].fn.call(b[P].context, c, f, d)
                    break
                  default:
                    if (!O) for (_ = 1, O = new Array(C - 1); _ < C; _++) O[_ - 1] = arguments[_]
                    b[P].fn.apply(b[P].context, O)
                }
            }
            return !0
          }),
          (a.prototype.on = function (u, c, f) {
            return i(this, u, c, f, !1)
          }),
          (a.prototype.once = function (u, c, f) {
            return i(this, u, c, f, !0)
          }),
          (a.prototype.removeListener = function (u, c, f, d) {
            var p = n ? n + u : u
            if (!this._events[p]) return this
            if (!c) return (s(this, p), this)
            var m = this._events[p]
            if (m.fn) m.fn === c && (!d || m.once) && (!f || m.context === f) && s(this, p)
            else {
              for (var v = 0, b = [], C = m.length; v < C; v++)
                (m[v].fn !== c || (d && !m[v].once) || (f && m[v].context !== f)) && b.push(m[v])
              b.length ? (this._events[p] = b.length === 1 ? b[0] : b) : s(this, p)
            }
            return this
          }),
          (a.prototype.removeAllListeners = function (u) {
            var c
            return (
              u
                ? ((c = n ? n + u : u), this._events[c] && s(this, c))
                : ((this._events = new r()), (this._eventsCount = 0)),
              this
            )
          }),
          (a.prototype.off = a.prototype.removeListener),
          (a.prototype.addListener = a.prototype.on),
          (a.prefixed = n),
          (a.EventEmitter = a),
          (e.exports = a))
      })(ti)),
    ti.exports
  )
}
var Bv = Dv()
const zv = Fm(Bv)
class vf extends zv {
  engine
  _inited = !1
  constructor(t) {
    ;(super(), this._init(t))
  }
  _init(t) {
    this._inited ||
      ((this._inited = !0),
      (this.engine = new WebSocket(t)),
      this.engine.addEventListener('error', (n) => {
        this.emit(cn.WS_ERROR, n)
      }),
      this.engine.addEventListener('open', () => {
        this.emit(cn.WS_OPEN)
      }),
      this.engine.addEventListener('message', (n) => {
        this.emit(cn.WS_MESSAGE, n.data)
      }),
      this.engine.addEventListener('close', () => {
        this.emit(cn.WS_CLOSE)
      }))
  }
  send(t) {
    this.engine?.send(t)
  }
  stop() {
    ;(this.emit(cn.WS_CLOSE), (this._inited = !1), this.engine?.close())
  }
}
const Pn = location.protocol === 'https:'
console.log(Pn, void 0, !1)
const Wv = location.hostname,
  Vv = location.port,
  Eo = `${Wv}:${Vv}`,
  Uv = Pn === void 0 ? location.protocol : Pn ? 'https' : 'http',
  yf = `${Uv}://${Eo}`
function bf(e, t) {
  const n = localStorage.getItem('auth_openavatarchat'),
    r = new Headers(t?.headers || {})
  n && r.set('Authorization', `Bearer ${n}`)
  const o = { ...t, headers: r }
  return window.fetch(`${yf}${e}`, o)
}
function Dy() {
  return bf('/openavatarchat/initconfig')
}
function By(e) {
  return bf('/webrtc/offer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(e),
  })
}
function zy(e, t) {
  const n = localStorage.getItem('auth_openavatarchat')
  let r = `${Pn ? 'wss' : 'ws'}://${Eo}${e}/${t}`
  return (n && n && (r += `?token=${encodeURIComponent(n)}`), new vf(r))
}
function Wy() {
  const e = localStorage.getItem('auth_openavatarchat')
  let t = `${Pn ? 'wss' : 'ws'}://${Eo}/ws/manager/data_tool`
  return (e && (t += `?token=${encodeURIComponent(e)}`), new vf(t))
}
function Vy(e) {
  return e.startsWith('http') ? e : `${yf}${e}`
}
function Uy(e) {
  return `${Pn ? 'https' : 'http'}://${Eo}/download/manager/data_tool/file?file_path=${encodeURIComponent(e)}`
}
export {
  zy as $,
  ky as A,
  Cl as B,
  qe as C,
  L as D,
  le as E,
  Zt as F,
  ue as G,
  Lt as H,
  Ae as I,
  Ee as J,
  Yt as K,
  Ji as L,
  xn as M,
  Dy as N,
  Vy as O,
  Fu as P,
  Hv as Q,
  Ny as R,
  zv as S,
  hr as T,
  Fm as U,
  kv as V,
  Nv as W,
  cn as X,
  Fv as Y,
  By as Z,
  T as _,
  me as a,
  Mn as a$,
  di as a0,
  Qv as a1,
  ki as a2,
  sy as a3,
  gy as a4,
  Zv as a5,
  ay as a6,
  fy as a7,
  Ni as a8,
  ey as a9,
  wy as aA,
  by as aB,
  _y as aC,
  Ot as aD,
  L0 as aE,
  Sh as aF,
  He as aG,
  $y as aH,
  Ty as aI,
  Ly as aJ,
  Oy as aK,
  ss as aL,
  Ey as aM,
  mr as aN,
  jy as aO,
  To as aP,
  Kc as aQ,
  Iy as aR,
  Ay as aS,
  va as aT,
  _h as aU,
  Zg as aV,
  vy as aW,
  zc as aX,
  my as aY,
  vr as aZ,
  wd as a_,
  Yv as aa,
  po as ab,
  vd as ac,
  tr as ad,
  dy as ae,
  py as af,
  ct as ag,
  qi as ah,
  xy as ai,
  R0 as aj,
  cy as ak,
  mn as al,
  De as am,
  iu as an,
  fa as ao,
  Lh as ap,
  cd as aq,
  Ry as ar,
  Sy as as,
  mo as at,
  En as au,
  eo as av,
  ou as aw,
  Vo as ax,
  F0 as ay,
  Cy as az,
  Py as b,
  yi as b0,
  My as b1,
  jn as b2,
  In as b3,
  Rn as b4,
  xe as b5,
  Fy as b6,
  Uc as b7,
  Hy as b8,
  Wy as b9,
  Uy as ba,
  yf as bb,
  Pn as bc,
  ii as bd,
  xl as be,
  Lf as bf,
  ny as bg,
  ty as bh,
  oy as bi,
  nc as bj,
  ly as bk,
  sd as bl,
  Xv as bm,
  Jv as bn,
  Kv as bo,
  ry as bp,
  up as bq,
  Gi as br,
  zn as bs,
  w as c,
  be as d,
  ut as e,
  Wc as f,
  ds as g,
  Rt as h,
  yy as i,
  hy as j,
  fr as k,
  pr as l,
  Oo as m,
  qv as n,
  Yi as o,
  iy as p,
  fi as q,
  xu as r,
  We as s,
  _c as t,
  $o as u,
  uy as v,
  Fe as w,
  cp as x,
  Jt as y,
  Rf as z,
}

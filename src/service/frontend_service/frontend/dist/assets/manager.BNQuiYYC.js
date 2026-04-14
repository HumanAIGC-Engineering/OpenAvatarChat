var WS = (e, t) => () => (t || e((t = { exports: {} }).exports, t), t.exports)
import {
  d as te,
  ag as Ko,
  l as Me,
  ah as Zo,
  L as Jo,
  w as me,
  ai as At,
  H as Qe,
  _ as D,
  P as Q,
  aj as o_,
  c as F,
  ak as Qt,
  a as oe,
  n as Lr,
  a5 as US,
  C as de,
  al as Xn,
  am as xe,
  s as ce,
  o as je,
  D as X,
  f as Fr,
  h as i_,
  an as tf,
  ao as Ln,
  ap as un,
  ab as Ne,
  aq as Oe,
  ar as nf,
  v as Qo,
  a7 as dh,
  as as YS,
  at as Et,
  au as Cr,
  av as XS,
  aw as fh,
  ax as Xe,
  ay as KS,
  az as ZS,
  aA as hh,
  G as Re,
  aB as JS,
  aC as QS,
  aD as St,
  aE as a_,
  J as xt,
  I as kr,
  g as en,
  u as Ge,
  aF as To,
  K as Ye,
  b as ex,
  aG as st,
  m as ot,
  r as Kn,
  i as tn,
  aH as rf,
  aI as tx,
  aJ as Er,
  aK as nx,
  aL as rx,
  aM as $r,
  aN as ph,
  aO as s_,
  aP as ox,
  aQ as of,
  T as ix,
  aR as l_,
  aS as vr,
  aT as Oo,
  aU as Cd,
  aV as ax,
  aW as sx,
  aX as lx,
  aY as ux,
  aZ as u_,
  a_ as cx,
  a$ as af,
  b0 as on,
  b1 as sf,
  b2 as dx,
  b3 as fx,
  b4 as hx,
  b5 as px,
  b6 as vx,
  ad as gx,
  b7 as mx,
  M as yx,
  y as K,
  E as ei,
  b8 as Qr,
  U as bx,
  j as _x,
  b9 as wx,
  X as eo,
  k as Po,
  R as Sx,
  ba as vh,
  p as ve,
  q as ee,
  t as he,
  ac as Ve,
  x as Xt,
  a8 as ct,
  z as ze,
  A as xn,
  a2 as Ct,
  bb as xx,
  bc as Cx,
  bd as c_,
  be as lf,
  bf as gr,
  a6 as Pe,
  a9 as yn,
  a0 as ke,
  B as d_,
  bg as Ex,
  bh as bt,
  bi as $x,
  bj as Tx,
  bk as Ox,
  bl as Px,
  bm as Ix,
  bn as f_,
  F as Ce,
  bo as Ee,
  bp as Ax,
  bq as h_,
  a1 as Nx,
  br as bo,
  a4 as uf,
  a3 as Rx,
  bs as Mx,
  ae as Dx,
  af as Bx,
} from './index.l6nW9Nb8.js'
var tF = WS((Mt, Dt) => {
  var p_ = (function () {
      if (typeof Map < 'u') return Map
      function e(t, n) {
        var r = -1
        return (
          t.some(function (o, i) {
            return o[0] === n ? ((r = i), !0) : !1
          }),
          r
        )
      }
      return (function () {
        function t() {
          this.__entries__ = []
        }
        return (
          Object.defineProperty(t.prototype, 'size', {
            get: function () {
              return this.__entries__.length
            },
            enumerable: !0,
            configurable: !0,
          }),
          (t.prototype.get = function (n) {
            var r = e(this.__entries__, n),
              o = this.__entries__[r]
            return o && o[1]
          }),
          (t.prototype.set = function (n, r) {
            var o = e(this.__entries__, n)
            ~o ? (this.__entries__[o][1] = r) : this.__entries__.push([n, r])
          }),
          (t.prototype.delete = function (n) {
            var r = this.__entries__,
              o = e(r, n)
            ~o && r.splice(o, 1)
          }),
          (t.prototype.has = function (n) {
            return !!~e(this.__entries__, n)
          }),
          (t.prototype.clear = function () {
            this.__entries__.splice(0)
          }),
          (t.prototype.forEach = function (n, r) {
            r === void 0 && (r = null)
            for (var o = 0, i = this.__entries__; o < i.length; o++) {
              var a = i[o]
              n.call(r, a[1], a[0])
            }
          }),
          t
        )
      })()
    })(),
    Ed = typeof window < 'u' && typeof document < 'u' && window.document === document,
    Io = (function () {
      return typeof global < 'u' && global.Math === Math
        ? global
        : typeof self < 'u' && self.Math === Math
          ? self
          : typeof window < 'u' && window.Math === Math
            ? window
            : Function('return this')()
    })(),
    qx = (function () {
      return typeof requestAnimationFrame == 'function'
        ? requestAnimationFrame.bind(Io)
        : function (e) {
            return setTimeout(function () {
              return e(Date.now())
            }, 1e3 / 60)
          }
    })(),
    zx = 2
  function Lx(e, t) {
    var n = !1,
      r = !1,
      o = 0
    function i() {
      ;(n && ((n = !1), e()), r && s())
    }
    function a() {
      qx(i)
    }
    function s() {
      var l = Date.now()
      if (n) {
        if (l - o < zx) return
        r = !0
      } else ((n = !0), (r = !1), setTimeout(a, t))
      o = l
    }
    return s
  }
  var Fx = 20,
    kx = ['top', 'right', 'bottom', 'left', 'width', 'height', 'size', 'weight'],
    Hx = typeof MutationObserver < 'u',
    jx = (function () {
      function e() {
        ;((this.connected_ = !1),
          (this.mutationEventsAdded_ = !1),
          (this.mutationsObserver_ = null),
          (this.observers_ = []),
          (this.onTransitionEnd_ = this.onTransitionEnd_.bind(this)),
          (this.refresh = Lx(this.refresh.bind(this), Fx)))
      }
      return (
        (e.prototype.addObserver = function (t) {
          ;(~this.observers_.indexOf(t) || this.observers_.push(t),
            this.connected_ || this.connect_())
        }),
        (e.prototype.removeObserver = function (t) {
          var n = this.observers_,
            r = n.indexOf(t)
          ;(~r && n.splice(r, 1), !n.length && this.connected_ && this.disconnect_())
        }),
        (e.prototype.refresh = function () {
          var t = this.updateObservers_()
          t && this.refresh()
        }),
        (e.prototype.updateObservers_ = function () {
          var t = this.observers_.filter(function (n) {
            return (n.gatherActive(), n.hasActive())
          })
          return (
            t.forEach(function (n) {
              return n.broadcastActive()
            }),
            t.length > 0
          )
        }),
        (e.prototype.connect_ = function () {
          !Ed ||
            this.connected_ ||
            (document.addEventListener('transitionend', this.onTransitionEnd_),
            window.addEventListener('resize', this.refresh),
            Hx
              ? ((this.mutationsObserver_ = new MutationObserver(this.refresh)),
                this.mutationsObserver_.observe(document, {
                  attributes: !0,
                  childList: !0,
                  characterData: !0,
                  subtree: !0,
                }))
              : (document.addEventListener('DOMSubtreeModified', this.refresh),
                (this.mutationEventsAdded_ = !0)),
            (this.connected_ = !0))
        }),
        (e.prototype.disconnect_ = function () {
          !Ed ||
            !this.connected_ ||
            (document.removeEventListener('transitionend', this.onTransitionEnd_),
            window.removeEventListener('resize', this.refresh),
            this.mutationsObserver_ && this.mutationsObserver_.disconnect(),
            this.mutationEventsAdded_ &&
              document.removeEventListener('DOMSubtreeModified', this.refresh),
            (this.mutationsObserver_ = null),
            (this.mutationEventsAdded_ = !1),
            (this.connected_ = !1))
        }),
        (e.prototype.onTransitionEnd_ = function (t) {
          var n = t.propertyName,
            r = n === void 0 ? '' : n,
            o = kx.some(function (i) {
              return !!~r.indexOf(i)
            })
          o && this.refresh()
        }),
        (e.getInstance = function () {
          return (this.instance_ || (this.instance_ = new e()), this.instance_)
        }),
        (e.instance_ = null),
        e
      )
    })(),
    v_ = function (e, t) {
      for (var n = 0, r = Object.keys(t); n < r.length; n++) {
        var o = r[n]
        Object.defineProperty(e, o, { value: t[o], enumerable: !1, writable: !1, configurable: !0 })
      }
      return e
    },
    Fn = function (e) {
      var t = e && e.ownerDocument && e.ownerDocument.defaultView
      return t || Io
    },
    g_ = ti(0, 0, 0, 0)
  function Ao(e) {
    return parseFloat(e) || 0
  }
  function gh(e) {
    for (var t = [], n = 1; n < arguments.length; n++) t[n - 1] = arguments[n]
    return t.reduce(function (r, o) {
      var i = e['border-' + o + '-width']
      return r + Ao(i)
    }, 0)
  }
  function Vx(e) {
    for (var t = ['top', 'right', 'bottom', 'left'], n = {}, r = 0, o = t; r < o.length; r++) {
      var i = o[r],
        a = e['padding-' + i]
      n[i] = Ao(a)
    }
    return n
  }
  function Gx(e) {
    var t = e.getBBox()
    return ti(0, 0, t.width, t.height)
  }
  function Wx(e) {
    var t = e.clientWidth,
      n = e.clientHeight
    if (!t && !n) return g_
    var r = Fn(e).getComputedStyle(e),
      o = Vx(r),
      i = o.left + o.right,
      a = o.top + o.bottom,
      s = Ao(r.width),
      l = Ao(r.height)
    if (
      (r.boxSizing === 'border-box' &&
        (Math.round(s + i) !== t && (s -= gh(r, 'left', 'right') + i),
        Math.round(l + a) !== n && (l -= gh(r, 'top', 'bottom') + a)),
      !Yx(e))
    ) {
      var u = Math.round(s + i) - t,
        c = Math.round(l + a) - n
      ;(Math.abs(u) !== 1 && (s -= u), Math.abs(c) !== 1 && (l -= c))
    }
    return ti(o.left, o.top, s, l)
  }
  var Ux = (function () {
    return typeof SVGGraphicsElement < 'u'
      ? function (e) {
          return e instanceof Fn(e).SVGGraphicsElement
        }
      : function (e) {
          return e instanceof Fn(e).SVGElement && typeof e.getBBox == 'function'
        }
  })()
  function Yx(e) {
    return e === Fn(e).document.documentElement
  }
  function Xx(e) {
    return Ed ? (Ux(e) ? Gx(e) : Wx(e)) : g_
  }
  function Kx(e) {
    var t = e.x,
      n = e.y,
      r = e.width,
      o = e.height,
      i = typeof DOMRectReadOnly < 'u' ? DOMRectReadOnly : Object,
      a = Object.create(i.prototype)
    return (
      v_(a, { x: t, y: n, width: r, height: o, top: n, right: t + r, bottom: o + n, left: t }),
      a
    )
  }
  function ti(e, t, n, r) {
    return { x: e, y: t, width: n, height: r }
  }
  var Zx = (function () {
      function e(t) {
        ;((this.broadcastWidth = 0),
          (this.broadcastHeight = 0),
          (this.contentRect_ = ti(0, 0, 0, 0)),
          (this.target = t))
      }
      return (
        (e.prototype.isActive = function () {
          var t = Xx(this.target)
          return (
            (this.contentRect_ = t),
            t.width !== this.broadcastWidth || t.height !== this.broadcastHeight
          )
        }),
        (e.prototype.broadcastRect = function () {
          var t = this.contentRect_
          return ((this.broadcastWidth = t.width), (this.broadcastHeight = t.height), t)
        }),
        e
      )
    })(),
    Jx = (function () {
      function e(t, n) {
        var r = Kx(n)
        v_(this, { target: t, contentRect: r })
      }
      return e
    })(),
    Qx = (function () {
      function e(t, n, r) {
        if (
          ((this.activeObservations_ = []), (this.observations_ = new p_()), typeof t != 'function')
        )
          throw new TypeError('The callback provided as parameter 1 is not a function.')
        ;((this.callback_ = t), (this.controller_ = n), (this.callbackCtx_ = r))
      }
      return (
        (e.prototype.observe = function (t) {
          if (!arguments.length) throw new TypeError('1 argument required, but only 0 present.')
          if (!(typeof Element > 'u' || !(Element instanceof Object))) {
            if (!(t instanceof Fn(t).Element))
              throw new TypeError('parameter 1 is not of type "Element".')
            var n = this.observations_
            n.has(t) ||
              (n.set(t, new Zx(t)), this.controller_.addObserver(this), this.controller_.refresh())
          }
        }),
        (e.prototype.unobserve = function (t) {
          if (!arguments.length) throw new TypeError('1 argument required, but only 0 present.')
          if (!(typeof Element > 'u' || !(Element instanceof Object))) {
            if (!(t instanceof Fn(t).Element))
              throw new TypeError('parameter 1 is not of type "Element".')
            var n = this.observations_
            n.has(t) && (n.delete(t), n.size || this.controller_.removeObserver(this))
          }
        }),
        (e.prototype.disconnect = function () {
          ;(this.clearActive(), this.observations_.clear(), this.controller_.removeObserver(this))
        }),
        (e.prototype.gatherActive = function () {
          var t = this
          ;(this.clearActive(),
            this.observations_.forEach(function (n) {
              n.isActive() && t.activeObservations_.push(n)
            }))
        }),
        (e.prototype.broadcastActive = function () {
          if (this.hasActive()) {
            var t = this.callbackCtx_,
              n = this.activeObservations_.map(function (r) {
                return new Jx(r.target, r.broadcastRect())
              })
            ;(this.callback_.call(t, n, t), this.clearActive())
          }
        }),
        (e.prototype.clearActive = function () {
          this.activeObservations_.splice(0)
        }),
        (e.prototype.hasActive = function () {
          return this.activeObservations_.length > 0
        }),
        e
      )
    })(),
    m_ = typeof WeakMap < 'u' ? new WeakMap() : new p_(),
    y_ = (function () {
      function e(t) {
        if (!(this instanceof e)) throw new TypeError('Cannot call a class as a function.')
        if (!arguments.length) throw new TypeError('1 argument required, but only 0 present.')
        var n = jx.getInstance(),
          r = new Qx(t, n, this)
        m_.set(this, r)
      }
      return e
    })()
  ;['observe', 'unobserve', 'disconnect'].forEach(function (e) {
    y_.prototype[e] = function () {
      var t
      return (t = m_.get(this))[e].apply(t, arguments)
    }
  })
  var b_ = (function () {
    return typeof Io.ResizeObserver < 'u' ? Io.ResizeObserver : y_
  })()
  const eC = te({
    compatConfig: { MODE: 3 },
    name: 'ResizeObserver',
    props: { disabled: Boolean, onResize: Function },
    emits: ['resize'],
    setup(e, t) {
      let { slots: n } = t
      const r = Ko({ width: 0, height: 0, offsetHeight: 0, offsetWidth: 0 })
      let o = null,
        i = null
      const a = () => {
          i && (i.disconnect(), (i = null))
        },
        s = (c) => {
          const { onResize: d } = e,
            f = c[0].target,
            { width: h, height: g } = f.getBoundingClientRect(),
            { offsetWidth: m, offsetHeight: v } = f,
            b = Math.floor(h),
            y = Math.floor(g)
          if (r.width !== b || r.height !== y || r.offsetWidth !== m || r.offsetHeight !== v) {
            const p = { width: b, height: y, offsetWidth: m, offsetHeight: v }
            ;(D(r, p),
              d &&
                Promise.resolve().then(() => {
                  d(D(D({}, p), { offsetWidth: m, offsetHeight: v }), f)
                }))
          }
        },
        l = Qe(),
        u = () => {
          const { disabled: c } = e
          if (c) {
            a()
            return
          }
          const d = At(l)
          ;(d !== o && (a(), (o = d)), !i && d && ((i = new b_(s)), i.observe(d)))
        }
      return (
        Me(() => {
          u()
        }),
        Zo(() => {
          u()
        }),
        Jo(() => {
          a()
        }),
        me(
          () => e.disabled,
          () => {
            u()
          },
          { flush: 'post' }
        ),
        () => {
          var c
          return (c = n.default) === null || c === void 0 ? void 0 : c.call(n)[0]
        }
      )
    },
  })
  let __ = (e) => setTimeout(e, 16),
    w_ = (e) => clearTimeout(e)
  typeof window < 'u' &&
    'requestAnimationFrame' in window &&
    ((__ = (e) => window.requestAnimationFrame(e)), (w_ = (e) => window.cancelAnimationFrame(e)))
  let mh = 0
  const cf = new Map()
  function S_(e) {
    cf.delete(e)
  }
  function He(e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1
    mh += 1
    const n = mh
    function r(o) {
      if (o === 0) (S_(n), e())
      else {
        const i = __(() => {
          r(o - 1)
        })
        cf.set(n, i)
      }
    }
    return (r(t), n)
  }
  He.cancel = (e) => {
    const t = cf.get(e)
    return (S_(t), w_(t))
  }
  let fn = !1
  try {
    const e = Object.defineProperty({}, 'passive', {
      get() {
        fn = !0
      },
    })
    ;(window.addEventListener('testPassive', null, e),
      window.removeEventListener('testPassive', null, e))
  } catch {}
  function Rn(e, t, n, r) {
    if (e && e.addEventListener) {
      let o = r
      ;(o === void 0 &&
        fn &&
        (t === 'touchstart' || t === 'touchmove' || t === 'wheel') &&
        (o = { passive: !1 }),
        e.addEventListener(t, n, o))
    }
    return {
      remove: () => {
        e && e.removeEventListener && e.removeEventListener(t, n)
      },
    }
  }
  let yh = {}
  function tC(e, t) {}
  function nC(e, t, n) {
    !t && !yh[n] && (yh[n] = !0)
  }
  function rC(e, t) {
    nC(tC, e, t)
  }
  const No = [
      'blue',
      'purple',
      'cyan',
      'green',
      'magenta',
      'pink',
      'red',
      'orange',
      'yellow',
      'volcano',
      'geekblue',
      'lime',
      'gold',
    ],
    oC = (e, t, n, r, o) => {
      const i = e / 2,
        a = 0,
        s = i,
        l = (n * 1) / Math.sqrt(2),
        u = i - n * (1 - 1 / Math.sqrt(2)),
        c = i - t * (1 / Math.sqrt(2)),
        d = n * (Math.sqrt(2) - 1) + t * (1 / Math.sqrt(2)),
        f = 2 * i - c,
        h = d,
        g = 2 * i - l,
        m = u,
        v = 2 * i - a,
        b = s,
        y = i * Math.sqrt(2) + n * (Math.sqrt(2) - 2),
        p = n * (Math.sqrt(2) - 1)
      return {
        pointerEvents: 'none',
        width: e,
        height: e,
        overflow: 'hidden',
        '&::after': {
          content: '""',
          position: 'absolute',
          width: y,
          height: y,
          bottom: 0,
          insetInline: 0,
          margin: 'auto',
          borderRadius: { _skip_check_: !0, value: `0 0 ${t}px 0` },
          transform: 'translateY(50%) rotate(-135deg)',
          boxShadow: o,
          zIndex: 0,
          background: 'transparent',
        },
        '&::before': {
          position: 'absolute',
          bottom: 0,
          insetInlineStart: 0,
          width: e,
          height: e / 2,
          background: r,
          clipPath: {
            _multi_value_: !0,
            value: [
              `polygon(${p}px 100%, 50% ${p}px, ${2 * i - p}px 100%, ${p}px 100%)`,
              `path('M ${a} ${s} A ${n} ${n} 0 0 0 ${l} ${u} L ${c} ${d} A ${t} ${t} 0 0 1 ${f} ${h} L ${g} ${m} A ${n} ${n} 0 0 0 ${v} ${b} Z')`,
            ],
          },
          content: '""',
        },
      }
    }
  function x_(e, t) {
    return No.reduce((n, r) => {
      const o = e[`${r}-1`],
        i = e[`${r}-3`],
        a = e[`${r}-6`],
        s = e[`${r}-7`]
      return D(D({}, n), t(r, { lightColor: o, lightBorderColor: i, darkColor: a, textColor: s }))
    }, {})
  }
  function dt(e, t) {
    const n = D({}, e)
    for (let r = 0; r < t.length; r += 1) {
      const o = t[r]
      delete n[o]
    }
    return n
  }
  const df = (e, t, n) => {
    rC(e, `[ant-design-vue: ${t}] ${n}`)
  }
  function iC() {
    return ''
  }
  function aC(e) {
    return e ? e.ownerDocument : window.document
  }
  function C_() {}
  const sC = () => ({
      action: Q.oneOfType([Q.string, Q.arrayOf(Q.string)]).def([]),
      showAction: Q.any.def([]),
      hideAction: Q.any.def([]),
      getPopupClassNameFromAlign: Q.any.def(iC),
      onPopupVisibleChange: Function,
      afterPopupVisibleChange: Q.func.def(C_),
      popup: Q.any,
      arrow: Q.bool.def(!0),
      popupStyle: { type: Object, default: void 0 },
      prefixCls: Q.string.def('rc-trigger-popup'),
      popupClassName: Q.string.def(''),
      popupPlacement: String,
      builtinPlacements: Q.object,
      popupTransitionName: String,
      popupAnimation: Q.any,
      mouseEnterDelay: Q.number.def(0),
      mouseLeaveDelay: Q.number.def(0.1),
      zIndex: Number,
      focusDelay: Q.number.def(0),
      blurDelay: Q.number.def(0.15),
      getPopupContainer: Function,
      getDocument: Q.func.def(aC),
      forceRender: { type: Boolean, default: void 0 },
      destroyPopupOnHide: { type: Boolean, default: !1 },
      mask: { type: Boolean, default: !1 },
      maskClosable: { type: Boolean, default: !0 },
      popupAlign: Q.object.def(() => ({})),
      popupVisible: { type: Boolean, default: void 0 },
      defaultPopupVisible: { type: Boolean, default: !1 },
      maskTransitionName: String,
      maskAnimation: String,
      stretch: String,
      alignPoint: { type: Boolean, default: void 0 },
      autoDestroy: { type: Boolean, default: !1 },
      mobile: Object,
      getTriggerDOMNode: Function,
    }),
    ff = {
      visible: Boolean,
      prefixCls: String,
      zIndex: Number,
      destroyPopupOnHide: Boolean,
      forceRender: Boolean,
      arrow: { type: Boolean, default: !0 },
      animation: [String, Object],
      transitionName: String,
      stretch: { type: String },
      align: { type: Object },
      point: { type: Object },
      getRootDomNode: { type: Function },
      getClassNameFromAlign: { type: Function },
      onAlign: { type: Function },
      onMouseenter: { type: Function },
      onMouseleave: { type: Function },
      onMousedown: { type: Function },
      onTouchstart: { type: Function },
    },
    lC = D(D({}, ff), { mobile: { type: Object } }),
    uC = D(D({}, ff), {
      mask: Boolean,
      mobile: { type: Object },
      maskAnimation: String,
      maskTransitionName: String,
    })
  function E_(e) {
    const {
      prefixCls: t,
      visible: n,
      zIndex: r,
      mask: o,
      maskAnimation: i,
      maskTransitionName: a,
    } = e
    if (!o) return null
    let s = {}
    return (
      (a || i) && (s = o_({ prefixCls: t, transitionName: a, animation: i })),
      F(Qt, oe({ appear: !0 }, s), {
        default: () => [
          Lr(F('div', { style: { zIndex: r }, class: `${t}-mask` }, null), [[US('if'), n]]),
        ],
      })
    )
  }
  E_.displayName = 'Mask'
  const cC = te({
    compatConfig: { MODE: 3 },
    name: 'MobilePopupInner',
    inheritAttrs: !1,
    props: lC,
    emits: ['mouseenter', 'mouseleave', 'mousedown', 'touchstart', 'align'],
    setup(e, t) {
      let { expose: n, slots: r } = t
      const o = de()
      return (
        n({ forceAlign: () => {}, getElement: () => o.value }),
        () => {
          var i
          const {
              zIndex: a,
              visible: s,
              prefixCls: l,
              mobile: {
                popupClassName: u,
                popupStyle: c,
                popupMotion: d = {},
                popupRender: f,
              } = {},
            } = e,
            h = D({ zIndex: a }, c)
          let g = Xn((i = r.default) === null || i === void 0 ? void 0 : i.call(r))
          ;(g.length > 1 && (g = F('div', { class: `${l}-content` }, [g])), f && (g = f(g)))
          const m = xe(l, u)
          return F(Qt, oe({ ref: o }, d), {
            default: () => [s ? F('div', { class: m, style: h }, [g]) : null],
          })
        }
      )
    },
  })
  var dC = function (e, t, n, r) {
    function o(i) {
      return i instanceof n
        ? i
        : new n(function (a) {
            a(i)
          })
    }
    return new (n || (n = Promise))(function (i, a) {
      function s(c) {
        try {
          u(r.next(c))
        } catch (d) {
          a(d)
        }
      }
      function l(c) {
        try {
          u(r.throw(c))
        } catch (d) {
          a(d)
        }
      }
      function u(c) {
        c.done ? i(c.value) : o(c.value).then(s, l)
      }
      u((r = r.apply(e, t || [])).next())
    })
  }
  const bh = ['measure', 'align', null, 'motion'],
    fC = (e, t) => {
      const n = ce(null),
        r = ce(),
        o = ce(!1)
      function i(l) {
        o.value || (n.value = l)
      }
      function a() {
        He.cancel(r.value)
      }
      function s(l) {
        ;(a(),
          (r.value = He(() => {
            let u = n.value
            switch (n.value) {
              case 'align':
                u = 'motion'
                break
              case 'motion':
                u = 'stable'
                break
            }
            ;(i(u), l?.())
          })))
      }
      return (
        me(
          e,
          () => {
            i('measure')
          },
          { immediate: !0, flush: 'post' }
        ),
        Me(() => {
          me(
            n,
            () => {
              switch (n.value) {
                case 'measure':
                  t()
                  break
              }
              n.value &&
                (r.value = He(() =>
                  dC(void 0, void 0, void 0, function* () {
                    const l = bh.indexOf(n.value),
                      u = bh[l + 1]
                    u && l !== -1 && i(u)
                  })
                ))
            },
            { immediate: !0, flush: 'post' }
          )
        }),
        je(() => {
          ;((o.value = !0), a())
        }),
        [n, s]
      )
    },
    hC = (e) => {
      const t = ce({ width: 0, height: 0 })
      function n(o) {
        t.value = { width: o.offsetWidth, height: o.offsetHeight }
      }
      return [
        X(() => {
          const o = {}
          if (e.value) {
            const { width: i, height: a } = t.value
            ;(e.value.indexOf('height') !== -1 && a
              ? (o.height = `${a}px`)
              : e.value.indexOf('minHeight') !== -1 && a && (o.minHeight = `${a}px`),
              e.value.indexOf('width') !== -1 && i
                ? (o.width = `${i}px`)
                : e.value.indexOf('minWidth') !== -1 && i && (o.minWidth = `${i}px`))
          }
          return o
        }),
        n,
      ]
    }
  function _h(e, t) {
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
  function wh(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t] != null ? arguments[t] : {}
      t % 2
        ? _h(Object(n), !0).forEach(function (r) {
            pC(e, r, n[r])
          })
        : Object.getOwnPropertyDescriptors
          ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n))
          : _h(Object(n)).forEach(function (r) {
              Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(n, r))
            })
    }
    return e
  }
  function $d(e) {
    '@babel/helpers - typeof'
    return (
      ($d =
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
      $d(e)
    )
  }
  function pC(e, t, n) {
    return (
      t in e
        ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
        : (e[t] = n),
      e
    )
  }
  var or,
    vC = { Webkit: '-webkit-', Moz: '-moz-', ms: '-ms-', O: '-o-' }
  function Ro() {
    if (or !== void 0) return or
    or = ''
    var e = document.createElement('p').style,
      t = 'Transform'
    for (var n in vC) n + t in e && (or = n)
    return or
  }
  function $_() {
    return Ro() ? ''.concat(Ro(), 'TransitionProperty') : 'transitionProperty'
  }
  function ni() {
    return Ro() ? ''.concat(Ro(), 'Transform') : 'transform'
  }
  function Sh(e, t) {
    var n = $_()
    n && ((e.style[n] = t), n !== 'transitionProperty' && (e.style.transitionProperty = t))
  }
  function Bi(e, t) {
    var n = ni()
    n && ((e.style[n] = t), n !== 'transform' && (e.style.transform = t))
  }
  function gC(e) {
    return e.style.transitionProperty || e.style[$_()]
  }
  function mC(e) {
    var t = window.getComputedStyle(e, null),
      n = t.getPropertyValue('transform') || t.getPropertyValue(ni())
    if (n && n !== 'none') {
      var r = n.replace(/[^0-9\-.,]/g, '').split(',')
      return { x: parseFloat(r[12] || r[4], 0), y: parseFloat(r[13] || r[5], 0) }
    }
    return { x: 0, y: 0 }
  }
  var yC = /matrix\((.*)\)/,
    bC = /matrix3d\((.*)\)/
  function _C(e, t) {
    var n = window.getComputedStyle(e, null),
      r = n.getPropertyValue('transform') || n.getPropertyValue(ni())
    if (r && r !== 'none') {
      var o,
        i = r.match(yC)
      if (i)
        ((i = i[1]),
          (o = i.split(',').map(function (s) {
            return parseFloat(s, 10)
          })),
          (o[4] = t.x),
          (o[5] = t.y),
          Bi(e, 'matrix('.concat(o.join(','), ')')))
      else {
        var a = r.match(bC)[1]
        ;((o = a.split(',').map(function (s) {
          return parseFloat(s, 10)
        })),
          (o[12] = t.x),
          (o[13] = t.y),
          Bi(e, 'matrix3d('.concat(o.join(','), ')')))
      }
    } else Bi(e, 'translateX('.concat(t.x, 'px) translateY(').concat(t.y, 'px) translateZ(0)'))
  }
  var wC = /[\-+]?(?:\d*\.|)\d+(?:[eE][\-+]?\d+|)/.source,
    Hr
  function xh(e) {
    var t = e.style.display
    ;((e.style.display = 'none'), e.offsetHeight, (e.style.display = t))
  }
  function Mn(e, t, n) {
    var r = n
    if ($d(t) === 'object') {
      for (var o in t) t.hasOwnProperty(o) && Mn(e, o, t[o])
      return
    }
    if (typeof r < 'u') {
      ;(typeof r == 'number' && (r = ''.concat(r, 'px')), (e.style[t] = r))
      return
    }
    return Hr(e, t)
  }
  function SC(e) {
    var t,
      n,
      r,
      o = e.ownerDocument,
      i = o.body,
      a = o && o.documentElement
    return (
      (t = e.getBoundingClientRect()),
      (n = Math.floor(t.left)),
      (r = Math.floor(t.top)),
      (n -= a.clientLeft || i.clientLeft || 0),
      (r -= a.clientTop || i.clientTop || 0),
      { left: n, top: r }
    )
  }
  function T_(e, t) {
    var n = e['page'.concat(t ? 'Y' : 'X', 'Offset')],
      r = 'scroll'.concat(t ? 'Top' : 'Left')
    if (typeof n != 'number') {
      var o = e.document
      ;((n = o.documentElement[r]), typeof n != 'number' && (n = o.body[r]))
    }
    return n
  }
  function O_(e) {
    return T_(e)
  }
  function P_(e) {
    return T_(e, !0)
  }
  function Tr(e) {
    var t = SC(e),
      n = e.ownerDocument,
      r = n.defaultView || n.parentWindow
    return ((t.left += O_(r)), (t.top += P_(r)), t)
  }
  function hf(e) {
    return e != null && e == e.window
  }
  function I_(e) {
    return hf(e) ? e.document : e.nodeType === 9 ? e : e.ownerDocument
  }
  function xC(e, t, n) {
    var r = n,
      o = '',
      i = I_(e)
    return (
      (r = r || i.defaultView.getComputedStyle(e, null)),
      r && (o = r.getPropertyValue(t) || r[t]),
      o
    )
  }
  var CC = new RegExp('^('.concat(wC, ')(?!px)[a-z%]+$'), 'i'),
    EC = /^(top|right|bottom|left)$/,
    qi = 'currentStyle',
    zi = 'runtimeStyle',
    an = 'left',
    $C = 'px'
  function TC(e, t) {
    var n = e[qi] && e[qi][t]
    if (CC.test(n) && !EC.test(t)) {
      var r = e.style,
        o = r[an],
        i = e[zi][an]
      ;((e[zi][an] = e[qi][an]),
        (r[an] = t === 'fontSize' ? '1em' : n || 0),
        (n = r.pixelLeft + $C),
        (r[an] = o),
        (e[zi][an] = i))
    }
    return n === '' ? 'auto' : n
  }
  typeof window < 'u' && (Hr = window.getComputedStyle ? xC : TC)
  function to(e, t) {
    return e === 'left' ? (t.useCssRight ? 'right' : e) : t.useCssBottom ? 'bottom' : e
  }
  function Ch(e) {
    if (e === 'left') return 'right'
    if (e === 'right') return 'left'
    if (e === 'top') return 'bottom'
    if (e === 'bottom') return 'top'
  }
  function Eh(e, t, n) {
    Mn(e, 'position') === 'static' && (e.style.position = 'relative')
    var r = -999,
      o = -999,
      i = to('left', n),
      a = to('top', n),
      s = Ch(i),
      l = Ch(a)
    ;(i !== 'left' && (r = 999), a !== 'top' && (o = 999))
    var u = '',
      c = Tr(e)
    ;(('left' in t || 'top' in t) && ((u = gC(e) || ''), Sh(e, 'none')),
      'left' in t && ((e.style[s] = ''), (e.style[i] = ''.concat(r, 'px'))),
      'top' in t && ((e.style[l] = ''), (e.style[a] = ''.concat(o, 'px'))),
      xh(e))
    var d = Tr(e),
      f = {}
    for (var h in t)
      if (t.hasOwnProperty(h)) {
        var g = to(h, n),
          m = h === 'left' ? r : o,
          v = c[h] - d[h]
        g === h ? (f[g] = m + v) : (f[g] = m - v)
      }
    ;(Mn(e, f), xh(e), ('left' in t || 'top' in t) && Sh(e, u))
    var b = {}
    for (var y in t)
      if (t.hasOwnProperty(y)) {
        var p = to(y, n),
          _ = t[y] - c[y]
        y === p ? (b[p] = f[p] + _) : (b[p] = f[p] - _)
      }
    Mn(e, b)
  }
  function OC(e, t) {
    var n = Tr(e),
      r = mC(e),
      o = { x: r.x, y: r.y }
    ;('left' in t && (o.x = r.x + t.left - n.left),
      'top' in t && (o.y = r.y + t.top - n.top),
      _C(e, o))
  }
  function PC(e, t, n) {
    if (n.ignoreShake) {
      var r = Tr(e),
        o = r.left.toFixed(0),
        i = r.top.toFixed(0),
        a = t.left.toFixed(0),
        s = t.top.toFixed(0)
      if (o === a && i === s) return
    }
    n.useCssRight || n.useCssBottom
      ? Eh(e, t, n)
      : n.useCssTransform && ni() in document.body.style
        ? OC(e, t)
        : Eh(e, t, n)
  }
  function pf(e, t) {
    for (var n = 0; n < e.length; n++) t(e[n])
  }
  function A_(e) {
    return Hr(e, 'boxSizing') === 'border-box'
  }
  var IC = ['margin', 'border', 'padding'],
    Td = -1,
    AC = 2,
    Od = 1,
    NC = 0
  function RC(e, t, n) {
    var r = {},
      o = e.style,
      i
    for (i in t) t.hasOwnProperty(i) && ((r[i] = o[i]), (o[i] = t[i]))
    n.call(e)
    for (i in t) t.hasOwnProperty(i) && (o[i] = r[i])
  }
  function lr(e, t, n) {
    var r = 0,
      o,
      i,
      a
    for (i = 0; i < t.length; i++)
      if (((o = t[i]), o))
        for (a = 0; a < n.length; a++) {
          var s = void 0
          ;(o === 'border' ? (s = ''.concat(o).concat(n[a], 'Width')) : (s = o + n[a]),
            (r += parseFloat(Hr(e, s)) || 0))
        }
    return r
  }
  var yt = {
    getParent: function (t) {
      var n = t
      do n.nodeType === 11 && n.host ? (n = n.host) : (n = n.parentNode)
      while (n && n.nodeType !== 1 && n.nodeType !== 9)
      return n
    },
  }
  pf(['Width', 'Height'], function (e) {
    ;((yt['doc'.concat(e)] = function (t) {
      var n = t.document
      return Math.max(
        n.documentElement['scroll'.concat(e)],
        n.body['scroll'.concat(e)],
        yt['viewport'.concat(e)](n)
      )
    }),
      (yt['viewport'.concat(e)] = function (t) {
        var n = 'client'.concat(e),
          r = t.document,
          o = r.body,
          i = r.documentElement,
          a = i[n]
        return (r.compatMode === 'CSS1Compat' && a) || (o && o[n]) || a
      }))
  })
  function $h(e, t, n) {
    var r = n
    if (hf(e)) return t === 'width' ? yt.viewportWidth(e) : yt.viewportHeight(e)
    if (e.nodeType === 9) return t === 'width' ? yt.docWidth(e) : yt.docHeight(e)
    var o = t === 'width' ? ['Left', 'Right'] : ['Top', 'Bottom'],
      i = Math.floor(
        t === 'width' ? e.getBoundingClientRect().width : e.getBoundingClientRect().height
      ),
      a = A_(e),
      s = 0
    ;((i == null || i <= 0) &&
      ((i = void 0),
      (s = Hr(e, t)),
      (s == null || Number(s) < 0) && (s = e.style[t] || 0),
      (s = Math.floor(parseFloat(s)) || 0)),
      r === void 0 && (r = a ? Od : Td))
    var l = i !== void 0 || a,
      u = i || s
    return r === Td
      ? l
        ? u - lr(e, ['border', 'padding'], o)
        : s
      : l
        ? r === Od
          ? u
          : u + (r === AC ? -lr(e, ['border'], o) : lr(e, ['margin'], o))
        : s + lr(e, IC.slice(r), o)
  }
  var MC = { position: 'absolute', visibility: 'hidden', display: 'block' }
  function Th() {
    for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++) t[n] = arguments[n]
    var r,
      o = t[0]
    return (
      o.offsetWidth !== 0
        ? (r = $h.apply(void 0, t))
        : RC(o, MC, function () {
            r = $h.apply(void 0, t)
          }),
      r
    )
  }
  pf(['width', 'height'], function (e) {
    var t = e.charAt(0).toUpperCase() + e.slice(1)
    yt['outer'.concat(t)] = function (r, o) {
      return r && Th(r, e, o ? NC : Od)
    }
    var n = e === 'width' ? ['Left', 'Right'] : ['Top', 'Bottom']
    yt[e] = function (r, o) {
      var i = o
      if (i !== void 0) {
        if (r) {
          var a = A_(r)
          return (a && (i += lr(r, ['padding', 'border'], n)), Mn(r, e, i))
        }
        return
      }
      return r && Th(r, e, Td)
    }
  })
  function N_(e, t) {
    for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n])
    return e
  }
  var we = {
    getWindow: function (t) {
      if (t && t.document && t.setTimeout) return t
      var n = t.ownerDocument || t
      return n.defaultView || n.parentWindow
    },
    getDocument: I_,
    offset: function (t, n, r) {
      if (typeof n < 'u') PC(t, n, r || {})
      else return Tr(t)
    },
    isWindow: hf,
    each: pf,
    css: Mn,
    clone: function (t) {
      var n,
        r = {}
      for (n in t) t.hasOwnProperty(n) && (r[n] = t[n])
      var o = t.overflow
      if (o) for (n in t) t.hasOwnProperty(n) && (r.overflow[n] = t.overflow[n])
      return r
    },
    mix: N_,
    getWindowScrollLeft: function (t) {
      return O_(t)
    },
    getWindowScrollTop: function (t) {
      return P_(t)
    },
    merge: function () {
      for (var t = {}, n = 0; n < arguments.length; n++)
        we.mix(t, n < 0 || arguments.length <= n ? void 0 : arguments[n])
      return t
    },
    viewportWidth: 0,
    viewportHeight: 0,
  }
  N_(we, yt)
  var Li = we.getParent
  function Pd(e) {
    if (we.isWindow(e) || e.nodeType === 9) return null
    var t = we.getDocument(e),
      n = t.body,
      r,
      o = we.css(e, 'position'),
      i = o === 'fixed' || o === 'absolute'
    if (!i) return e.nodeName.toLowerCase() === 'html' ? null : Li(e)
    for (r = Li(e); r && r !== n && r.nodeType !== 9; r = Li(r))
      if (((o = we.css(r, 'position')), o !== 'static')) return r
    return null
  }
  var Oh = we.getParent
  function DC(e) {
    if (we.isWindow(e) || e.nodeType === 9) return !1
    var t = we.getDocument(e),
      n = t.body,
      r = null
    for (r = Oh(e); r && r !== n && r !== t; r = Oh(r)) {
      var o = we.css(r, 'position')
      if (o === 'fixed') return !0
    }
    return !1
  }
  function vf(e, t) {
    for (
      var n = { left: 0, right: 1 / 0, top: 0, bottom: 1 / 0 },
        r = Pd(e),
        o = we.getDocument(e),
        i = o.defaultView || o.parentWindow,
        a = o.body,
        s = o.documentElement;
      r;

    ) {
      if (
        (navigator.userAgent.indexOf('MSIE') === -1 || r.clientWidth !== 0) &&
        r !== a &&
        r !== s &&
        we.css(r, 'overflow') !== 'visible'
      ) {
        var l = we.offset(r)
        ;((l.left += r.clientLeft),
          (l.top += r.clientTop),
          (n.top = Math.max(n.top, l.top)),
          (n.right = Math.min(n.right, l.left + r.clientWidth)),
          (n.bottom = Math.min(n.bottom, l.top + r.clientHeight)),
          (n.left = Math.max(n.left, l.left)))
      } else if (r === a || r === s) break
      r = Pd(r)
    }
    var u = null
    if (!we.isWindow(e) && e.nodeType !== 9) {
      u = e.style.position
      var c = we.css(e, 'position')
      c === 'absolute' && (e.style.position = 'fixed')
    }
    var d = we.getWindowScrollLeft(i),
      f = we.getWindowScrollTop(i),
      h = we.viewportWidth(i),
      g = we.viewportHeight(i),
      m = s.scrollWidth,
      v = s.scrollHeight,
      b = window.getComputedStyle(a)
    if (
      (b.overflowX === 'hidden' && (m = i.innerWidth),
      b.overflowY === 'hidden' && (v = i.innerHeight),
      e.style && (e.style.position = u),
      t || DC(e))
    )
      ((n.left = Math.max(n.left, d)),
        (n.top = Math.max(n.top, f)),
        (n.right = Math.min(n.right, d + h)),
        (n.bottom = Math.min(n.bottom, f + g)))
    else {
      var y = Math.max(m, d + h)
      n.right = Math.min(n.right, y)
      var p = Math.max(v, f + g)
      n.bottom = Math.min(n.bottom, p)
    }
    return n.top >= 0 && n.left >= 0 && n.bottom > n.top && n.right > n.left ? n : null
  }
  function BC(e, t, n, r) {
    var o = we.clone(e),
      i = { width: t.width, height: t.height }
    return (
      r.adjustX && o.left < n.left && (o.left = n.left),
      r.resizeWidth &&
        o.left >= n.left &&
        o.left + i.width > n.right &&
        (i.width -= o.left + i.width - n.right),
      r.adjustX && o.left + i.width > n.right && (o.left = Math.max(n.right - i.width, n.left)),
      r.adjustY && o.top < n.top && (o.top = n.top),
      r.resizeHeight &&
        o.top >= n.top &&
        o.top + i.height > n.bottom &&
        (i.height -= o.top + i.height - n.bottom),
      r.adjustY && o.top + i.height > n.bottom && (o.top = Math.max(n.bottom - i.height, n.top)),
      we.mix(o, i)
    )
  }
  function gf(e) {
    var t, n, r
    if (!we.isWindow(e) && e.nodeType !== 9)
      ((t = we.offset(e)), (n = we.outerWidth(e)), (r = we.outerHeight(e)))
    else {
      var o = we.getWindow(e)
      ;((t = { left: we.getWindowScrollLeft(o), top: we.getWindowScrollTop(o) }),
        (n = we.viewportWidth(o)),
        (r = we.viewportHeight(o)))
    }
    return ((t.width = n), (t.height = r), t)
  }
  function Ph(e, t) {
    var n = t.charAt(0),
      r = t.charAt(1),
      o = e.width,
      i = e.height,
      a = e.left,
      s = e.top
    return (
      n === 'c' ? (s += i / 2) : n === 'b' && (s += i),
      r === 'c' ? (a += o / 2) : r === 'r' && (a += o),
      { left: a, top: s }
    )
  }
  function no(e, t, n, r, o) {
    var i = Ph(t, n[1]),
      a = Ph(e, n[0]),
      s = [a.left - i.left, a.top - i.top]
    return {
      left: Math.round(e.left - s[0] + r[0] - o[0]),
      top: Math.round(e.top - s[1] + r[1] - o[1]),
    }
  }
  function Ih(e, t, n) {
    return e.left < n.left || e.left + t.width > n.right
  }
  function Ah(e, t, n) {
    return e.top < n.top || e.top + t.height > n.bottom
  }
  function qC(e, t, n) {
    return e.left > n.right || e.left + t.width < n.left
  }
  function zC(e, t, n) {
    return e.top > n.bottom || e.top + t.height < n.top
  }
  function ro(e, t, n) {
    var r = []
    return (
      we.each(e, function (o) {
        r.push(
          o.replace(t, function (i) {
            return n[i]
          })
        )
      }),
      r
    )
  }
  function oo(e, t) {
    return ((e[t] = -e[t]), e)
  }
  function Nh(e, t) {
    var n
    return (
      /%$/.test(e)
        ? (n = (parseInt(e.substring(0, e.length - 1), 10) / 100) * t)
        : (n = parseInt(e, 10)),
      n || 0
    )
  }
  function Rh(e, t) {
    ;((e[0] = Nh(e[0], t.width)), (e[1] = Nh(e[1], t.height)))
  }
  function R_(e, t, n, r) {
    var o = n.points,
      i = n.offset || [0, 0],
      a = n.targetOffset || [0, 0],
      s = n.overflow,
      l = n.source || e
    ;((i = [].concat(i)), (a = [].concat(a)), (s = s || {}))
    var u = {},
      c = 0,
      d = !!(s && s.alwaysByViewport),
      f = vf(l, d),
      h = gf(l)
    ;(Rh(i, h), Rh(a, t))
    var g = no(h, t, o, i, a),
      m = we.merge(h, g)
    if (f && (s.adjustX || s.adjustY) && r) {
      if (s.adjustX && Ih(g, h, f)) {
        var v = ro(o, /[lr]/gi, { l: 'r', r: 'l' }),
          b = oo(i, 0),
          y = oo(a, 0),
          p = no(h, t, v, b, y)
        qC(p, h, f) || ((c = 1), (o = v), (i = b), (a = y))
      }
      if (s.adjustY && Ah(g, h, f)) {
        var _ = ro(o, /[tb]/gi, { t: 'b', b: 't' }),
          x = oo(i, 1),
          S = oo(a, 1),
          w = no(h, t, _, x, S)
        zC(w, h, f) || ((c = 1), (o = _), (i = x), (a = S))
      }
      c && ((g = no(h, t, o, i, a)), we.mix(m, g))
      var T = Ih(g, h, f),
        A = Ah(g, h, f)
      if (T || A) {
        var $ = o
        ;(T && ($ = ro(o, /[lr]/gi, { l: 'r', r: 'l' })),
          A && ($ = ro(o, /[tb]/gi, { t: 'b', b: 't' })),
          (o = $),
          (i = n.offset || [0, 0]),
          (a = n.targetOffset || [0, 0]))
      }
      ;((u.adjustX = s.adjustX && T),
        (u.adjustY = s.adjustY && A),
        (u.adjustX || u.adjustY) && (m = BC(g, h, f, u)))
    }
    return (
      m.width !== h.width && we.css(l, 'width', we.width(l) + m.width - h.width),
      m.height !== h.height && we.css(l, 'height', we.height(l) + m.height - h.height),
      we.offset(
        l,
        { left: m.left, top: m.top },
        {
          useCssRight: n.useCssRight,
          useCssBottom: n.useCssBottom,
          useCssTransform: n.useCssTransform,
          ignoreShake: n.ignoreShake,
        }
      ),
      { points: o, offset: i, targetOffset: a, overflow: u }
    )
  }
  function LC(e, t) {
    var n = vf(e, t),
      r = gf(e)
    return (
      !n ||
      r.left + r.width <= n.left ||
      r.top + r.height <= n.top ||
      r.left >= n.right ||
      r.top >= n.bottom
    )
  }
  function mf(e, t, n) {
    var r = n.target || t,
      o = gf(r),
      i = !LC(r, n.overflow && n.overflow.alwaysByViewport)
    return R_(e, o, n, i)
  }
  mf.__getOffsetParent = Pd
  mf.__getVisibleRectForElement = vf
  function FC(e, t, n) {
    var r,
      o,
      i = we.getDocument(e),
      a = i.defaultView || i.parentWindow,
      s = we.getWindowScrollLeft(a),
      l = we.getWindowScrollTop(a),
      u = we.viewportWidth(a),
      c = we.viewportHeight(a)
    ;('pageX' in t ? (r = t.pageX) : (r = s + t.clientX),
      'pageY' in t ? (o = t.pageY) : (o = l + t.clientY))
    var d = { left: r, top: o, width: 0, height: 0 },
      f = r >= 0 && r <= s + u && o >= 0 && o <= l + c,
      h = [n.points[0], 'cc']
    return R_(e, d, wh(wh({}, n), {}, { points: h }), f)
  }
  function Ke(e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {},
      n = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : !0,
      r = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : !1,
      o = e
    if ((Array.isArray(e) && (o = Fr(e)[0]), !o)) return null
    const i = i_(o, t, r)
    return ((i.props = n ? D(D({}, i.props), t) : i.props), tf(typeof i.props.class != 'object'), i)
  }
  function kC(e, t, n) {
    Ln(i_(e, D({}, t)), n)
  }
  const M_ = (e) => {
    if (!e) return !1
    if (e.offsetParent) return !0
    if (e.getBBox) {
      const t = e.getBBox()
      if (t.width || t.height) return !0
    }
    if (e.getBoundingClientRect) {
      const t = e.getBoundingClientRect()
      if (t.width || t.height) return !0
    }
    return !1
  }
  function HC(e, t) {
    return e === t
      ? !0
      : !e || !t
        ? !1
        : 'pageX' in t && 'pageY' in t
          ? e.pageX === t.pageX && e.pageY === t.pageY
          : 'clientX' in t && 'clientY' in t
            ? e.clientX === t.clientX && e.clientY === t.clientY
            : !1
  }
  function jC(e, t) {
    e !== document.activeElement && un(t, e) && typeof e.focus == 'function' && e.focus()
  }
  function Mh(e, t) {
    let n = null,
      r = null
    function o(a) {
      let [{ target: s }] = a
      if (!document.documentElement.contains(s)) return
      const { width: l, height: u } = s.getBoundingClientRect(),
        c = Math.floor(l),
        d = Math.floor(u)
      ;((n !== c || r !== d) &&
        Promise.resolve().then(() => {
          t({ width: c, height: d })
        }),
        (n = c),
        (r = d))
    }
    const i = new b_(o)
    return (
      e && i.observe(e),
      () => {
        i.disconnect()
      }
    )
  }
  const VC = (e, t) => {
    let n = !1,
      r = null
    function o() {
      clearTimeout(r)
    }
    function i(a) {
      if (!n || a === !0) {
        if (e() === !1) return
        ;((n = !0),
          o(),
          (r = setTimeout(() => {
            n = !1
          }, t.value)))
      } else
        (o(),
          (r = setTimeout(() => {
            ;((n = !1), i())
          }, t.value)))
    }
    return [
      i,
      () => {
        ;((n = !1), o())
      },
    ]
  }
  function GC() {
    ;((this.__data__ = []), (this.size = 0))
  }
  function D_(e, t) {
    return e === t || (e !== e && t !== t)
  }
  function ri(e, t) {
    for (var n = e.length; n--; ) if (D_(e[n][0], t)) return n
    return -1
  }
  var WC = Array.prototype,
    UC = WC.splice
  function YC(e) {
    var t = this.__data__,
      n = ri(t, e)
    if (n < 0) return !1
    var r = t.length - 1
    return (n == r ? t.pop() : UC.call(t, n, 1), --this.size, !0)
  }
  function XC(e) {
    var t = this.__data__,
      n = ri(t, e)
    return n < 0 ? void 0 : t[n][1]
  }
  function KC(e) {
    return ri(this.__data__, e) > -1
  }
  function ZC(e, t) {
    var n = this.__data__,
      r = ri(n, e)
    return (r < 0 ? (++this.size, n.push([e, t])) : (n[r][1] = t), this)
  }
  function zt(e) {
    var t = -1,
      n = e == null ? 0 : e.length
    for (this.clear(); ++t < n; ) {
      var r = e[t]
      this.set(r[0], r[1])
    }
  }
  zt.prototype.clear = GC
  zt.prototype.delete = YC
  zt.prototype.get = XC
  zt.prototype.has = KC
  zt.prototype.set = ZC
  function JC() {
    ;((this.__data__ = new zt()), (this.size = 0))
  }
  function QC(e) {
    var t = this.__data__,
      n = t.delete(e)
    return ((this.size = t.size), n)
  }
  function eE(e) {
    return this.__data__.get(e)
  }
  function tE(e) {
    return this.__data__.has(e)
  }
  var B_ = typeof global == 'object' && global && global.Object === Object && global,
    nE = typeof self == 'object' && self && self.Object === Object && self,
    Lt = B_ || nE || Function('return this')(),
    kn = Lt.Symbol,
    q_ = Object.prototype,
    rE = q_.hasOwnProperty,
    oE = q_.toString,
    ir = kn ? kn.toStringTag : void 0
  function iE(e) {
    var t = rE.call(e, ir),
      n = e[ir]
    try {
      e[ir] = void 0
      var r = !0
    } catch {}
    var o = oE.call(e)
    return (r && (t ? (e[ir] = n) : delete e[ir]), o)
  }
  var aE = Object.prototype,
    sE = aE.toString
  function lE(e) {
    return sE.call(e)
  }
  var uE = '[object Null]',
    cE = '[object Undefined]',
    Dh = kn ? kn.toStringTag : void 0
  function Zn(e) {
    return e == null ? (e === void 0 ? cE : uE) : Dh && Dh in Object(e) ? iE(e) : lE(e)
  }
  function z_(e) {
    var t = typeof e
    return e != null && (t == 'object' || t == 'function')
  }
  var dE = '[object AsyncFunction]',
    fE = '[object Function]',
    hE = '[object GeneratorFunction]',
    pE = '[object Proxy]'
  function L_(e) {
    if (!z_(e)) return !1
    var t = Zn(e)
    return t == fE || t == hE || t == dE || t == pE
  }
  var Fi = Lt['__core-js_shared__'],
    Bh = (function () {
      var e = /[^.]+$/.exec((Fi && Fi.keys && Fi.keys.IE_PROTO) || '')
      return e ? 'Symbol(src)_1.' + e : ''
    })()
  function vE(e) {
    return !!Bh && Bh in e
  }
  var gE = Function.prototype,
    mE = gE.toString
  function Cn(e) {
    if (e != null) {
      try {
        return mE.call(e)
      } catch {}
      try {
        return e + ''
      } catch {}
    }
    return ''
  }
  var yE = /[\\^$.*+?()[\]{}|]/g,
    bE = /^\[object .+?Constructor\]$/,
    _E = Function.prototype,
    wE = Object.prototype,
    SE = _E.toString,
    xE = wE.hasOwnProperty,
    CE = RegExp(
      '^' +
        SE.call(xE)
          .replace(yE, '\\$&')
          .replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, '$1.*?') +
        '$'
    )
  function EE(e) {
    if (!z_(e) || vE(e)) return !1
    var t = L_(e) ? CE : bE
    return t.test(Cn(e))
  }
  function $E(e, t) {
    return e?.[t]
  }
  function Jn(e, t) {
    var n = $E(e, t)
    return EE(n) ? n : void 0
  }
  var Or = Jn(Lt, 'Map'),
    Pr = Jn(Object, 'create')
  function TE() {
    ;((this.__data__ = Pr ? Pr(null) : {}), (this.size = 0))
  }
  function OE(e) {
    var t = this.has(e) && delete this.__data__[e]
    return ((this.size -= t ? 1 : 0), t)
  }
  var PE = '__lodash_hash_undefined__',
    IE = Object.prototype,
    AE = IE.hasOwnProperty
  function NE(e) {
    var t = this.__data__
    if (Pr) {
      var n = t[e]
      return n === PE ? void 0 : n
    }
    return AE.call(t, e) ? t[e] : void 0
  }
  var RE = Object.prototype,
    ME = RE.hasOwnProperty
  function DE(e) {
    var t = this.__data__
    return Pr ? t[e] !== void 0 : ME.call(t, e)
  }
  var BE = '__lodash_hash_undefined__'
  function qE(e, t) {
    var n = this.__data__
    return ((this.size += this.has(e) ? 0 : 1), (n[e] = Pr && t === void 0 ? BE : t), this)
  }
  function bn(e) {
    var t = -1,
      n = e == null ? 0 : e.length
    for (this.clear(); ++t < n; ) {
      var r = e[t]
      this.set(r[0], r[1])
    }
  }
  bn.prototype.clear = TE
  bn.prototype.delete = OE
  bn.prototype.get = NE
  bn.prototype.has = DE
  bn.prototype.set = qE
  function zE() {
    ;((this.size = 0),
      (this.__data__ = { hash: new bn(), map: new (Or || zt)(), string: new bn() }))
  }
  function LE(e) {
    var t = typeof e
    return t == 'string' || t == 'number' || t == 'symbol' || t == 'boolean'
      ? e !== '__proto__'
      : e === null
  }
  function oi(e, t) {
    var n = e.__data__
    return LE(t) ? n[typeof t == 'string' ? 'string' : 'hash'] : n.map
  }
  function FE(e) {
    var t = oi(this, e).delete(e)
    return ((this.size -= t ? 1 : 0), t)
  }
  function kE(e) {
    return oi(this, e).get(e)
  }
  function HE(e) {
    return oi(this, e).has(e)
  }
  function jE(e, t) {
    var n = oi(this, e),
      r = n.size
    return (n.set(e, t), (this.size += n.size == r ? 0 : 1), this)
  }
  function En(e) {
    var t = -1,
      n = e == null ? 0 : e.length
    for (this.clear(); ++t < n; ) {
      var r = e[t]
      this.set(r[0], r[1])
    }
  }
  En.prototype.clear = zE
  En.prototype.delete = FE
  En.prototype.get = kE
  En.prototype.has = HE
  En.prototype.set = jE
  var VE = 200
  function GE(e, t) {
    var n = this.__data__
    if (n instanceof zt) {
      var r = n.__data__
      if (!Or || r.length < VE - 1) return (r.push([e, t]), (this.size = ++n.size), this)
      n = this.__data__ = new En(r)
    }
    return (n.set(e, t), (this.size = n.size), this)
  }
  function Kt(e) {
    var t = (this.__data__ = new zt(e))
    this.size = t.size
  }
  Kt.prototype.clear = JC
  Kt.prototype.delete = QC
  Kt.prototype.get = eE
  Kt.prototype.has = tE
  Kt.prototype.set = GE
  var WE = '__lodash_hash_undefined__'
  function UE(e) {
    return (this.__data__.set(e, WE), this)
  }
  function YE(e) {
    return this.__data__.has(e)
  }
  function Mo(e) {
    var t = -1,
      n = e == null ? 0 : e.length
    for (this.__data__ = new En(); ++t < n; ) this.add(e[t])
  }
  Mo.prototype.add = Mo.prototype.push = UE
  Mo.prototype.has = YE
  function XE(e, t) {
    for (var n = -1, r = e == null ? 0 : e.length; ++n < r; ) if (t(e[n], n, e)) return !0
    return !1
  }
  function KE(e, t) {
    return e.has(t)
  }
  var ZE = 1,
    JE = 2
  function F_(e, t, n, r, o, i) {
    var a = n & ZE,
      s = e.length,
      l = t.length
    if (s != l && !(a && l > s)) return !1
    var u = i.get(e),
      c = i.get(t)
    if (u && c) return u == t && c == e
    var d = -1,
      f = !0,
      h = n & JE ? new Mo() : void 0
    for (i.set(e, t), i.set(t, e); ++d < s; ) {
      var g = e[d],
        m = t[d]
      if (r) var v = a ? r(m, g, d, t, e, i) : r(g, m, d, e, t, i)
      if (v !== void 0) {
        if (v) continue
        f = !1
        break
      }
      if (h) {
        if (
          !XE(t, function (b, y) {
            if (!KE(h, y) && (g === b || o(g, b, n, r, i))) return h.push(y)
          })
        ) {
          f = !1
          break
        }
      } else if (!(g === m || o(g, m, n, r, i))) {
        f = !1
        break
      }
    }
    return (i.delete(e), i.delete(t), f)
  }
  var qh = Lt.Uint8Array
  function QE(e) {
    var t = -1,
      n = Array(e.size)
    return (
      e.forEach(function (r, o) {
        n[++t] = [o, r]
      }),
      n
    )
  }
  function e$(e) {
    var t = -1,
      n = Array(e.size)
    return (
      e.forEach(function (r) {
        n[++t] = r
      }),
      n
    )
  }
  var t$ = 1,
    n$ = 2,
    r$ = '[object Boolean]',
    o$ = '[object Date]',
    i$ = '[object Error]',
    a$ = '[object Map]',
    s$ = '[object Number]',
    l$ = '[object RegExp]',
    u$ = '[object Set]',
    c$ = '[object String]',
    d$ = '[object Symbol]',
    f$ = '[object ArrayBuffer]',
    h$ = '[object DataView]',
    zh = kn ? kn.prototype : void 0,
    ki = zh ? zh.valueOf : void 0
  function p$(e, t, n, r, o, i, a) {
    switch (n) {
      case h$:
        if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset) return !1
        ;((e = e.buffer), (t = t.buffer))
      case f$:
        return !(e.byteLength != t.byteLength || !i(new qh(e), new qh(t)))
      case r$:
      case o$:
      case s$:
        return D_(+e, +t)
      case i$:
        return e.name == t.name && e.message == t.message
      case l$:
      case c$:
        return e == t + ''
      case a$:
        var s = QE
      case u$:
        var l = r & t$
        if ((s || (s = e$), e.size != t.size && !l)) return !1
        var u = a.get(e)
        if (u) return u == t
        ;((r |= n$), a.set(e, t))
        var c = F_(s(e), s(t), r, o, i, a)
        return (a.delete(e), c)
      case d$:
        if (ki) return ki.call(e) == ki.call(t)
    }
    return !1
  }
  function v$(e, t) {
    for (var n = -1, r = t.length, o = e.length; ++n < r; ) e[o + n] = t[n]
    return e
  }
  var Ir = Array.isArray
  function g$(e, t, n) {
    var r = t(e)
    return Ir(e) ? r : v$(r, n(e))
  }
  function m$(e, t) {
    for (var n = -1, r = e == null ? 0 : e.length, o = 0, i = []; ++n < r; ) {
      var a = e[n]
      t(a, n, e) && (i[o++] = a)
    }
    return i
  }
  function y$() {
    return []
  }
  var b$ = Object.prototype,
    _$ = b$.propertyIsEnumerable,
    Lh = Object.getOwnPropertySymbols,
    w$ = Lh
      ? function (e) {
          return e == null
            ? []
            : ((e = Object(e)),
              m$(Lh(e), function (t) {
                return _$.call(e, t)
              }))
        }
      : y$
  function S$(e, t) {
    for (var n = -1, r = Array(e); ++n < e; ) r[n] = t(n)
    return r
  }
  function Hn(e) {
    return e != null && typeof e == 'object'
  }
  var x$ = '[object Arguments]'
  function Fh(e) {
    return Hn(e) && Zn(e) == x$
  }
  var k_ = Object.prototype,
    C$ = k_.hasOwnProperty,
    E$ = k_.propertyIsEnumerable,
    H_ = Fh(
      (function () {
        return arguments
      })()
    )
      ? Fh
      : function (e) {
          return Hn(e) && C$.call(e, 'callee') && !E$.call(e, 'callee')
        }
  function $$() {
    return !1
  }
  var j_ = typeof Mt == 'object' && Mt && !Mt.nodeType && Mt,
    kh = j_ && typeof Dt == 'object' && Dt && !Dt.nodeType && Dt,
    T$ = kh && kh.exports === j_,
    Hh = T$ ? Lt.Buffer : void 0,
    O$ = Hh ? Hh.isBuffer : void 0,
    Do = O$ || $$,
    P$ = 9007199254740991,
    I$ = /^(?:0|[1-9]\d*)$/
  function A$(e, t) {
    var n = typeof e
    return (
      (t = t ?? P$),
      !!t && (n == 'number' || (n != 'symbol' && I$.test(e))) && e > -1 && e % 1 == 0 && e < t
    )
  }
  var N$ = 9007199254740991
  function V_(e) {
    return typeof e == 'number' && e > -1 && e % 1 == 0 && e <= N$
  }
  var R$ = '[object Arguments]',
    M$ = '[object Array]',
    D$ = '[object Boolean]',
    B$ = '[object Date]',
    q$ = '[object Error]',
    z$ = '[object Function]',
    L$ = '[object Map]',
    F$ = '[object Number]',
    k$ = '[object Object]',
    H$ = '[object RegExp]',
    j$ = '[object Set]',
    V$ = '[object String]',
    G$ = '[object WeakMap]',
    W$ = '[object ArrayBuffer]',
    U$ = '[object DataView]',
    Y$ = '[object Float32Array]',
    X$ = '[object Float64Array]',
    K$ = '[object Int8Array]',
    Z$ = '[object Int16Array]',
    J$ = '[object Int32Array]',
    Q$ = '[object Uint8Array]',
    eT = '[object Uint8ClampedArray]',
    tT = '[object Uint16Array]',
    nT = '[object Uint32Array]',
    Te = {}
  Te[Y$] = Te[X$] = Te[K$] = Te[Z$] = Te[J$] = Te[Q$] = Te[eT] = Te[tT] = Te[nT] = !0
  Te[R$] =
    Te[M$] =
    Te[W$] =
    Te[D$] =
    Te[U$] =
    Te[B$] =
    Te[q$] =
    Te[z$] =
    Te[L$] =
    Te[F$] =
    Te[k$] =
    Te[H$] =
    Te[j$] =
    Te[V$] =
    Te[G$] =
      !1
  function rT(e) {
    return Hn(e) && V_(e.length) && !!Te[Zn(e)]
  }
  function oT(e) {
    return function (t) {
      return e(t)
    }
  }
  var G_ = typeof Mt == 'object' && Mt && !Mt.nodeType && Mt,
    mr = G_ && typeof Dt == 'object' && Dt && !Dt.nodeType && Dt,
    iT = mr && mr.exports === G_,
    Hi = iT && B_.process,
    jh = (function () {
      try {
        var e = mr && mr.require && mr.require('util').types
        return e || (Hi && Hi.binding && Hi.binding('util'))
      } catch {}
    })(),
    Vh = jh && jh.isTypedArray,
    yf = Vh ? oT(Vh) : rT,
    aT = Object.prototype,
    sT = aT.hasOwnProperty
  function lT(e, t) {
    var n = Ir(e),
      r = !n && H_(e),
      o = !n && !r && Do(e),
      i = !n && !r && !o && yf(e),
      a = n || r || o || i,
      s = a ? S$(e.length, String) : [],
      l = s.length
    for (var u in e)
      sT.call(e, u) &&
        !(
          a &&
          (u == 'length' ||
            (o && (u == 'offset' || u == 'parent')) ||
            (i && (u == 'buffer' || u == 'byteLength' || u == 'byteOffset')) ||
            A$(u, l))
        ) &&
        s.push(u)
    return s
  }
  var uT = Object.prototype
  function W_(e) {
    var t = e && e.constructor,
      n = (typeof t == 'function' && t.prototype) || uT
    return e === n
  }
  function U_(e, t) {
    return function (n) {
      return e(t(n))
    }
  }
  var cT = U_(Object.keys, Object),
    dT = Object.prototype,
    fT = dT.hasOwnProperty
  function Y_(e) {
    if (!W_(e)) return cT(e)
    var t = []
    for (var n in Object(e)) fT.call(e, n) && n != 'constructor' && t.push(n)
    return t
  }
  function X_(e) {
    return e != null && V_(e.length) && !L_(e)
  }
  function hT(e) {
    return X_(e) ? lT(e) : Y_(e)
  }
  function Gh(e) {
    return g$(e, hT, w$)
  }
  var pT = 1,
    vT = Object.prototype,
    gT = vT.hasOwnProperty
  function mT(e, t, n, r, o, i) {
    var a = n & pT,
      s = Gh(e),
      l = s.length,
      u = Gh(t),
      c = u.length
    if (l != c && !a) return !1
    for (var d = l; d--; ) {
      var f = s[d]
      if (!(a ? f in t : gT.call(t, f))) return !1
    }
    var h = i.get(e),
      g = i.get(t)
    if (h && g) return h == t && g == e
    var m = !0
    ;(i.set(e, t), i.set(t, e))
    for (var v = a; ++d < l; ) {
      f = s[d]
      var b = e[f],
        y = t[f]
      if (r) var p = a ? r(y, b, f, t, e, i) : r(b, y, f, e, t, i)
      if (!(p === void 0 ? b === y || o(b, y, n, r, i) : p)) {
        m = !1
        break
      }
      v || (v = f == 'constructor')
    }
    if (m && !v) {
      var _ = e.constructor,
        x = t.constructor
      _ != x &&
        'constructor' in e &&
        'constructor' in t &&
        !(typeof _ == 'function' && _ instanceof _ && typeof x == 'function' && x instanceof x) &&
        (m = !1)
    }
    return (i.delete(e), i.delete(t), m)
  }
  var Id = Jn(Lt, 'DataView'),
    Ad = Jn(Lt, 'Promise'),
    Nd = Jn(Lt, 'Set'),
    Rd = Jn(Lt, 'WeakMap'),
    Wh = '[object Map]',
    yT = '[object Object]',
    Uh = '[object Promise]',
    Yh = '[object Set]',
    Xh = '[object WeakMap]',
    Kh = '[object DataView]',
    bT = Cn(Id),
    _T = Cn(Or),
    wT = Cn(Ad),
    ST = Cn(Nd),
    xT = Cn(Rd),
    Pt = Zn
  ;((Id && Pt(new Id(new ArrayBuffer(1))) != Kh) ||
    (Or && Pt(new Or()) != Wh) ||
    (Ad && Pt(Ad.resolve()) != Uh) ||
    (Nd && Pt(new Nd()) != Yh) ||
    (Rd && Pt(new Rd()) != Xh)) &&
    (Pt = function (e) {
      var t = Zn(e),
        n = t == yT ? e.constructor : void 0,
        r = n ? Cn(n) : ''
      if (r)
        switch (r) {
          case bT:
            return Kh
          case _T:
            return Wh
          case wT:
            return Uh
          case ST:
            return Yh
          case xT:
            return Xh
        }
      return t
    })
  var CT = 1,
    Zh = '[object Arguments]',
    Jh = '[object Array]',
    io = '[object Object]',
    ET = Object.prototype,
    Qh = ET.hasOwnProperty
  function $T(e, t, n, r, o, i) {
    var a = Ir(e),
      s = Ir(t),
      l = a ? Jh : Pt(e),
      u = s ? Jh : Pt(t)
    ;((l = l == Zh ? io : l), (u = u == Zh ? io : u))
    var c = l == io,
      d = u == io,
      f = l == u
    if (f && Do(e)) {
      if (!Do(t)) return !1
      ;((a = !0), (c = !1))
    }
    if (f && !c)
      return (i || (i = new Kt()), a || yf(e) ? F_(e, t, n, r, o, i) : p$(e, t, l, n, r, o, i))
    if (!(n & CT)) {
      var h = c && Qh.call(e, '__wrapped__'),
        g = d && Qh.call(t, '__wrapped__')
      if (h || g) {
        var m = h ? e.value() : e,
          v = g ? t.value() : t
        return (i || (i = new Kt()), o(m, v, n, r, i))
      }
    }
    return f ? (i || (i = new Kt()), mT(e, t, n, r, o, i)) : !1
  }
  function K_(e, t, n, r, o) {
    return e === t
      ? !0
      : e == null || t == null || (!Hn(e) && !Hn(t))
        ? e !== e && t !== t
        : $T(e, t, n, r, K_, o)
  }
  function TT(e, t) {
    return K_(e, t)
  }
  const OT = {
    align: Object,
    target: [Object, Function],
    onAlign: Function,
    monitorBufferTime: Number,
    monitorWindowResize: Boolean,
    disabled: Boolean,
  }
  function ep(e) {
    return typeof e != 'function' ? null : e()
  }
  function tp(e) {
    return typeof e != 'object' || !e ? null : e
  }
  const PT = te({
      compatConfig: { MODE: 3 },
      name: 'Align',
      props: OT,
      emits: ['align'],
      setup(e, t) {
        let { expose: n, slots: r } = t
        const o = de({}),
          i = de(),
          [a, s] = VC(
            () => {
              const { disabled: f, target: h, align: g, onAlign: m } = e
              if (!f && h && i.value) {
                const v = i.value
                let b
                const y = ep(h),
                  p = tp(h)
                ;((o.value.element = y), (o.value.point = p), (o.value.align = g))
                const { activeElement: _ } = document
                return (
                  y && M_(y) ? (b = mf(v, y, g)) : p && (b = FC(v, p, g)),
                  jC(_, v),
                  m && b && m(v, b),
                  !0
                )
              }
              return !1
            },
            X(() => e.monitorBufferTime)
          ),
          l = de({ cancel: () => {} }),
          u = de({ cancel: () => {} }),
          c = () => {
            const f = e.target,
              h = ep(f),
              g = tp(f)
            ;(i.value !== u.value.element &&
              (u.value.cancel(), (u.value.element = i.value), (u.value.cancel = Mh(i.value, a))),
              (o.value.element !== h || !HC(o.value.point, g) || !TT(o.value.align, e.align)) &&
                (a(),
                l.value.element !== h &&
                  (l.value.cancel(), (l.value.element = h), (l.value.cancel = Mh(h, a)))))
          }
        ;(Me(() => {
          Ne(() => {
            c()
          })
        }),
          Zo(() => {
            Ne(() => {
              c()
            })
          }),
          me(
            () => e.disabled,
            (f) => {
              f ? s() : a()
            },
            { immediate: !0, flush: 'post' }
          ))
        const d = de(null)
        return (
          me(
            () => e.monitorWindowResize,
            (f) => {
              f
                ? d.value || (d.value = Rn(window, 'resize', a))
                : d.value && (d.value.remove(), (d.value = null))
            },
            { flush: 'post' }
          ),
          Jo(() => {
            ;(l.value.cancel(), u.value.cancel(), d.value && d.value.remove(), s())
          }),
          n({ forceAlign: () => a(!0) }),
          () => {
            const f = r?.default()
            return f ? Ke(f[0], { ref: i }, !0, !0) : null
          }
        )
      },
    }),
    IT = te({
      compatConfig: { MODE: 3 },
      name: 'PopupInner',
      inheritAttrs: !1,
      props: ff,
      emits: ['mouseenter', 'mouseleave', 'mousedown', 'touchstart', 'align'],
      setup(e, t) {
        let { expose: n, attrs: r, slots: o } = t
        const i = ce(),
          a = ce(),
          s = ce(),
          [l, u] = hC(Oe(e, 'stretch')),
          c = () => {
            e.stretch && u(e.getRootDomNode())
          },
          d = ce(!1)
        let f
        me(
          () => e.visible,
          (S) => {
            ;(clearTimeout(f),
              S
                ? (f = setTimeout(() => {
                    d.value = e.visible
                  }))
                : (d.value = !1))
          },
          { immediate: !0 }
        )
        const [h, g] = fC(d, c),
          m = ce(),
          v = () => (e.point ? e.point : e.getRootDomNode),
          b = () => {
            var S
            ;(S = i.value) === null || S === void 0 || S.forceAlign()
          },
          y = (S, w) => {
            var T
            const A = e.getClassNameFromAlign(w),
              $ = s.value
            ;(s.value !== A && (s.value = A),
              h.value === 'align' &&
                ($ !== A
                  ? Promise.resolve().then(() => {
                      b()
                    })
                  : g(() => {
                      var P
                      ;(P = m.value) === null || P === void 0 || P.call(m)
                    }),
                (T = e.onAlign) === null || T === void 0 || T.call(e, S, w)))
          },
          p = X(() => {
            const S = typeof e.animation == 'object' ? e.animation : o_(e)
            return (
              ['onAfterEnter', 'onAfterLeave'].forEach((w) => {
                const T = S[w]
                S[w] = (A) => {
                  ;(g(), (h.value = 'stable'), T?.(A))
                }
              }),
              S
            )
          }),
          _ = () =>
            new Promise((S) => {
              m.value = S
            })
        ;(me(
          [p, h],
          () => {
            !p.value && h.value === 'motion' && g()
          },
          { immediate: !0 }
        ),
          n({ forceAlign: b, getElement: () => a.value.$el || a.value }))
        const x = X(() => {
          var S
          return !(
            !((S = e.align) === null || S === void 0) &&
            S.points &&
            (h.value === 'align' || h.value === 'stable')
          )
        })
        return () => {
          var S
          const {
              zIndex: w,
              align: T,
              prefixCls: A,
              destroyPopupOnHide: $,
              onMouseenter: P,
              onMouseleave: E,
              onTouchstart: z = () => {},
              onMousedown: C,
            } = e,
            R = h.value,
            N = [
              D(D({}, l.value), {
                zIndex: w,
                opacity: R === 'motion' || R === 'stable' || !d.value ? null : 0,
                pointerEvents: !d.value && R !== 'stable' ? 'none' : null,
              }),
              r.style,
            ]
          let j = Xn(
            (S = o.default) === null || S === void 0 ? void 0 : S.call(o, { visible: e.visible })
          )
          j.length > 1 && (j = F('div', { class: `${A}-content` }, [j]))
          const V = xe(A, r.class, s.value, !e.arrow && `${A}-arrow-hidden`),
            G = d.value || !e.visible ? nf(p.value.name, p.value) : {}
          return F(Qt, oe(oe({ ref: a }, G), {}, { onBeforeEnter: _ }), {
            default: () =>
              !$ || e.visible
                ? Lr(
                    F(
                      PT,
                      {
                        target: v(),
                        key: 'popup',
                        ref: i,
                        monitorWindowResize: !0,
                        disabled: x.value,
                        align: T,
                        onAlign: y,
                      },
                      {
                        default: () =>
                          F(
                            'div',
                            {
                              class: V,
                              onMouseenter: P,
                              onMouseleave: E,
                              onMousedown: dh(C, ['capture']),
                              [fn ? 'onTouchstartPassive' : 'onTouchstart']: dh(z, ['capture']),
                              style: N,
                            },
                            [j]
                          ),
                      }
                    ),
                    [[Qo, d.value]]
                  )
                : null,
          })
        }
      },
    }),
    AT = te({
      compatConfig: { MODE: 3 },
      name: 'Popup',
      inheritAttrs: !1,
      props: uC,
      setup(e, t) {
        let { attrs: n, slots: r, expose: o } = t
        const i = ce(!1),
          a = ce(!1),
          s = ce(),
          l = ce()
        return (
          me(
            [() => e.visible, () => e.mobile],
            () => {
              ;((i.value = e.visible), e.visible && e.mobile && (a.value = !0))
            },
            { immediate: !0, flush: 'post' }
          ),
          o({
            forceAlign: () => {
              var u
              ;(u = s.value) === null || u === void 0 || u.forceAlign()
            },
            getElement: () => {
              var u
              return (u = s.value) === null || u === void 0 ? void 0 : u.getElement()
            },
          }),
          () => {
            const u = D(D(D({}, e), n), { visible: i.value }),
              c = a.value
                ? F(cC, oe(oe({}, u), {}, { mobile: e.mobile, ref: s }), { default: r.default })
                : F(IT, oe(oe({}, u), {}, { ref: s }), { default: r.default })
            return F('div', { ref: l }, [F(E_, u, null), c])
          }
        )
      },
    })
  function NT(e, t, n) {
    return n ? e[0] === t[0] : e[0] === t[0] && e[1] === t[1]
  }
  function np(e, t, n) {
    const r = e[t] || {}
    return D(D({}, r), n)
  }
  function RT(e, t, n, r) {
    const { points: o } = n,
      i = Object.keys(e)
    for (let a = 0; a < i.length; a += 1) {
      const s = i[a]
      if (NT(e[s].points, o, r)) return `${t}-placement-${s}`
    }
    return ''
  }
  const MT = {
    methods: {
      setState() {
        let e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {},
          t = arguments.length > 1 ? arguments[1] : void 0,
          n = typeof e == 'function' ? e(this.$data, this.$props) : e
        if (this.getDerivedStateFromProps) {
          const r = this.getDerivedStateFromProps(YS(this), D(D({}, this.$data), n))
          if (r === null) return
          n = D(D({}, n), r || {})
        }
        ;(D(this.$data, n),
          this._.isMounted && this.$forceUpdate(),
          Ne(() => {
            t && t()
          }))
      },
      __emit() {
        const e = [].slice.call(arguments, 0)
        let t = e[0]
        t = `on${t[0].toUpperCase()}${t.substring(1)}`
        const n = this.$props[t] || this.$attrs[t]
        if (e.length && n)
          if (Array.isArray(n)) for (let r = 0, o = n.length; r < o; r++) n[r](...e.slice(1))
          else n(...e.slice(1))
      },
    },
  }
  let ji
  function DT(e) {
    if (typeof document > 'u') return 0
    if (ji === void 0) {
      const t = document.createElement('div')
      ;((t.style.width = '100%'), (t.style.height = '200px'))
      const n = document.createElement('div'),
        r = n.style
      ;((r.position = 'absolute'),
        (r.top = '0'),
        (r.left = '0'),
        (r.pointerEvents = 'none'),
        (r.visibility = 'hidden'),
        (r.width = '200px'),
        (r.height = '150px'),
        (r.overflow = 'hidden'),
        n.appendChild(t),
        document.body.appendChild(n))
      const o = t.offsetWidth
      n.style.overflow = 'scroll'
      let i = t.offsetWidth
      ;(o === i && (i = n.clientWidth), document.body.removeChild(n), (ji = o - i))
    }
    return ji
  }
  const BT = `vc-util-locker-${Date.now()}`
  let rp = 0
  function qT() {
    return (
      document.body.scrollHeight > (window.innerHeight || document.documentElement.clientHeight) &&
      window.innerWidth > document.body.offsetWidth
    )
  }
  function zT(e) {
    const t = X(() => !!e && !!e.value)
    rp += 1
    const n = `${BT}_${rp}`
    Et(
      (r) => {
        if (Cr()) {
          if (t.value) {
            const o = DT(),
              i = qT()
            XS(
              `
html body {
  overflow-y: hidden;
  ${i ? `width: calc(100% - ${o}px);` : ''}
}`,
              n
            )
          } else fh(n)
          r(() => {
            fh(n)
          })
        }
      },
      { flush: 'post' }
    )
  }
  let sn = 0
  const _o = Cr(),
    op = (e) => {
      if (!_o) return null
      if (e) {
        if (typeof e == 'string') return document.querySelectorAll(e)[0]
        if (typeof e == 'function') return e()
        if (typeof e == 'object' && e instanceof window.HTMLElement) return e
      }
      return document.body
    },
    Z_ = te({
      compatConfig: { MODE: 3 },
      name: 'PortalWrapper',
      inheritAttrs: !1,
      props: {
        wrapperClassName: String,
        forceRender: { type: Boolean, default: void 0 },
        getContainer: Q.any,
        visible: { type: Boolean, default: void 0 },
        autoLock: Xe(),
        didUpdate: Function,
      },
      setup(e, t) {
        let { slots: n } = t
        const r = ce(),
          o = ce(),
          i = ce(),
          a = ce(1),
          s = Cr() && document.createElement('div'),
          l = () => {
            var h, g
            ;(r.value === s &&
              ((g = (h = r.value) === null || h === void 0 ? void 0 : h.parentNode) === null ||
                g === void 0 ||
                g.removeChild(r.value)),
              (r.value = null))
          }
        let u = null
        const c = function () {
            return (arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : !1) ||
              (r.value && !r.value.parentNode)
              ? ((u = op(e.getContainer)), u ? (u.appendChild(r.value), !0) : !1)
              : !0
          },
          d = () => (_o ? (r.value || ((r.value = s), c(!0)), f(), r.value) : null),
          f = () => {
            const { wrapperClassName: h } = e
            r.value && h && h !== r.value.className && (r.value.className = h)
          }
        return (
          Zo(() => {
            ;(f(), c())
          }),
          zT(
            X(() => e.autoLock && e.visible && Cr() && (r.value === document.body || r.value === s))
          ),
          Me(() => {
            let h = !1
            ;(me(
              [() => e.visible, () => e.getContainer],
              (g, m) => {
                let [v, b] = g,
                  [y, p] = m
                ;(_o &&
                  ((u = op(e.getContainer)),
                  u === document.body && (v && !y ? (sn += 1) : h && (sn -= 1))),
                  h &&
                    (typeof b == 'function' && typeof p == 'function'
                      ? b.toString() !== p.toString()
                      : b !== p) &&
                    l(),
                  (h = !0))
              },
              { immediate: !0, flush: 'post' }
            ),
              Ne(() => {
                c() ||
                  (i.value = He(() => {
                    a.value += 1
                  }))
              }))
          }),
          je(() => {
            const { visible: h } = e
            ;(_o && u === document.body && (sn = h && sn ? sn - 1 : sn), l(), He.cancel(i.value))
          }),
          () => {
            const { forceRender: h, visible: g } = e
            let m = null
            const v = { getOpenCount: () => sn, getContainer: d }
            return (
              a.value &&
                (h || g || o.value) &&
                (m = F(
                  KS,
                  { getContainer: d, ref: o, didUpdate: e.didUpdate },
                  {
                    default: () => {
                      var b
                      return (b = n.default) === null || b === void 0 ? void 0 : b.call(n, v)
                    },
                  }
                )),
              m
            )
          }
        )
      },
    }),
    LT = [
      'onClick',
      'onMousedown',
      'onTouchstart',
      'onMouseenter',
      'onMouseleave',
      'onFocus',
      'onBlur',
      'onContextmenu',
    ],
    FT = te({
      compatConfig: { MODE: 3 },
      name: 'Trigger',
      mixins: [MT],
      inheritAttrs: !1,
      props: sC(),
      setup(e) {
        const t = X(() => {
            const { popupPlacement: o, popupAlign: i, builtinPlacements: a } = e
            return o && a ? np(a, o, i) : i
          }),
          n = ce(null),
          r = (o) => {
            n.value = o
          }
        return {
          vcTriggerContext: xt('vcTriggerContext', {}),
          popupRef: n,
          setPopupRef: r,
          triggerRef: ce(null),
          align: t,
          focusTime: null,
          clickOutsideHandler: null,
          contextmenuOutsideHandler1: null,
          contextmenuOutsideHandler2: null,
          touchOutsideHandler: null,
          attachId: null,
          delayTimer: null,
          hasPopupMouseDown: !1,
          preClickTime: null,
          preTouchTime: null,
          mouseDownTimeout: null,
          childOriginEvents: {},
        }
      },
      data() {
        const e = this.$props
        let t
        return (
          this.popupVisible !== void 0 ? (t = !!e.popupVisible) : (t = !!e.defaultPopupVisible),
          LT.forEach((n) => {
            this[`fire${n}`] = (r) => {
              this.fireEvents(n, r)
            }
          }),
          { prevPopupVisible: t, sPopupVisible: t, point: null }
        )
      },
      watch: {
        popupVisible(e) {
          e !== void 0 && ((this.prevPopupVisible = this.sPopupVisible), (this.sPopupVisible = e))
        },
      },
      created() {
        ;(St('vcTriggerContext', {
          onPopupMouseDown: this.onPopupMouseDown,
          onPopupMouseenter: this.onPopupMouseenter,
          onPopupMouseleave: this.onPopupMouseleave,
        }),
          a_(this))
      },
      deactivated() {
        this.setPopupVisible(!1)
      },
      mounted() {
        this.$nextTick(() => {
          this.updatedCal()
        })
      },
      updated() {
        this.$nextTick(() => {
          this.updatedCal()
        })
      },
      beforeUnmount() {
        ;(this.clearDelayTimer(),
          this.clearOutsideHandler(),
          clearTimeout(this.mouseDownTimeout),
          He.cancel(this.attachId))
      },
      methods: {
        updatedCal() {
          const e = this.$props
          if (this.$data.sPopupVisible) {
            let n
            ;(!this.clickOutsideHandler &&
              (this.isClickToHide() || this.isContextmenuToShow()) &&
              ((n = e.getDocument(this.getRootDomNode())),
              (this.clickOutsideHandler = Rn(n, 'mousedown', this.onDocumentClick))),
              this.touchOutsideHandler ||
                ((n = n || e.getDocument(this.getRootDomNode())),
                (this.touchOutsideHandler = Rn(
                  n,
                  'touchstart',
                  this.onDocumentClick,
                  fn ? { passive: !1 } : !1
                ))),
              !this.contextmenuOutsideHandler1 &&
                this.isContextmenuToShow() &&
                ((n = n || e.getDocument(this.getRootDomNode())),
                (this.contextmenuOutsideHandler1 = Rn(n, 'scroll', this.onContextmenuClose))),
              !this.contextmenuOutsideHandler2 &&
                this.isContextmenuToShow() &&
                (this.contextmenuOutsideHandler2 = Rn(window, 'blur', this.onContextmenuClose)))
          } else this.clearOutsideHandler()
        },
        onMouseenter(e) {
          const { mouseEnterDelay: t } = this.$props
          ;(this.fireEvents('onMouseenter', e), this.delaySetPopupVisible(!0, t, t ? null : e))
        },
        onMouseMove(e) {
          ;(this.fireEvents('onMousemove', e), this.setPoint(e))
        },
        onMouseleave(e) {
          ;(this.fireEvents('onMouseleave', e),
            this.delaySetPopupVisible(!1, this.$props.mouseLeaveDelay))
        },
        onPopupMouseenter() {
          const { vcTriggerContext: e = {} } = this
          ;(e.onPopupMouseenter && e.onPopupMouseenter(), this.clearDelayTimer())
        },
        onPopupMouseleave(e) {
          var t
          if (
            e &&
            e.relatedTarget &&
            !e.relatedTarget.setTimeout &&
            un(
              (t = this.popupRef) === null || t === void 0 ? void 0 : t.getElement(),
              e.relatedTarget
            )
          )
            return
          this.isMouseLeaveToHide() && this.delaySetPopupVisible(!1, this.$props.mouseLeaveDelay)
          const { vcTriggerContext: n = {} } = this
          n.onPopupMouseleave && n.onPopupMouseleave(e)
        },
        onFocus(e) {
          ;(this.fireEvents('onFocus', e),
            this.clearDelayTimer(),
            this.isFocusToShow() &&
              ((this.focusTime = Date.now()),
              this.delaySetPopupVisible(!0, this.$props.focusDelay)))
        },
        onMousedown(e) {
          ;(this.fireEvents('onMousedown', e), (this.preClickTime = Date.now()))
        },
        onTouchstart(e) {
          ;(this.fireEvents('onTouchstart', e), (this.preTouchTime = Date.now()))
        },
        onBlur(e) {
          un(e.target, e.relatedTarget || document.activeElement) ||
            (this.fireEvents('onBlur', e),
            this.clearDelayTimer(),
            this.isBlurToHide() && this.delaySetPopupVisible(!1, this.$props.blurDelay))
        },
        onContextmenu(e) {
          ;(e.preventDefault(), this.fireEvents('onContextmenu', e), this.setPopupVisible(!0, e))
        },
        onContextmenuClose() {
          this.isContextmenuToShow() && this.close()
        },
        onClick(e) {
          if ((this.fireEvents('onClick', e), this.focusTime)) {
            let n
            if (
              (this.preClickTime && this.preTouchTime
                ? (n = Math.min(this.preClickTime, this.preTouchTime))
                : this.preClickTime
                  ? (n = this.preClickTime)
                  : this.preTouchTime && (n = this.preTouchTime),
              Math.abs(n - this.focusTime) < 20)
            )
              return
            this.focusTime = 0
          }
          ;((this.preClickTime = 0),
            (this.preTouchTime = 0),
            this.isClickToShow() &&
              (this.isClickToHide() || this.isBlurToHide()) &&
              e &&
              e.preventDefault &&
              e.preventDefault(),
            e && e.domEvent && e.domEvent.preventDefault())
          const t = !this.$data.sPopupVisible
          ;((this.isClickToHide() && !t) || (t && this.isClickToShow())) &&
            this.setPopupVisible(!this.$data.sPopupVisible, e)
        },
        onPopupMouseDown() {
          const { vcTriggerContext: e = {} } = this
          ;((this.hasPopupMouseDown = !0),
            clearTimeout(this.mouseDownTimeout),
            (this.mouseDownTimeout = setTimeout(() => {
              this.hasPopupMouseDown = !1
            }, 0)),
            e.onPopupMouseDown && e.onPopupMouseDown(...arguments))
        },
        onDocumentClick(e) {
          if (this.$props.mask && !this.$props.maskClosable) return
          const t = e.target,
            n = this.getRootDomNode(),
            r = this.getPopupDomNode()
          ;(!un(n, t) || this.isContextMenuOnly()) &&
            !un(r, t) &&
            !this.hasPopupMouseDown &&
            this.delaySetPopupVisible(!1, 0.1)
        },
        getPopupDomNode() {
          var e
          return ((e = this.popupRef) === null || e === void 0 ? void 0 : e.getElement()) || null
        },
        getRootDomNode() {
          var e, t, n, r
          const { getTriggerDOMNode: o } = this.$props
          if (o) {
            const i =
              ((t = (e = this.triggerRef) === null || e === void 0 ? void 0 : e.$el) === null ||
              t === void 0
                ? void 0
                : t.nodeName) === '#comment'
                ? null
                : At(this.triggerRef)
            return At(o(i))
          }
          try {
            const i =
              ((r = (n = this.triggerRef) === null || n === void 0 ? void 0 : n.$el) === null ||
              r === void 0
                ? void 0
                : r.nodeName) === '#comment'
                ? null
                : At(this.triggerRef)
            if (i) return i
          } catch {}
          return At(this)
        },
        handleGetPopupClassFromAlign(e) {
          const t = [],
            n = this.$props,
            {
              popupPlacement: r,
              builtinPlacements: o,
              prefixCls: i,
              alignPoint: a,
              getPopupClassNameFromAlign: s,
            } = n
          return (r && o && t.push(RT(o, i, e, a)), s && t.push(s(e)), t.join(' '))
        },
        getPopupAlign() {
          const e = this.$props,
            { popupPlacement: t, popupAlign: n, builtinPlacements: r } = e
          return t && r ? np(r, t, n) : n
        },
        getComponent() {
          const e = {}
          ;(this.isMouseEnterToShow() && (e.onMouseenter = this.onPopupMouseenter),
            this.isMouseLeaveToHide() && (e.onMouseleave = this.onPopupMouseleave),
            (e.onMousedown = this.onPopupMouseDown),
            (e[fn ? 'onTouchstartPassive' : 'onTouchstart'] = this.onPopupMouseDown))
          const { handleGetPopupClassFromAlign: t, getRootDomNode: n, $attrs: r } = this,
            {
              prefixCls: o,
              destroyPopupOnHide: i,
              popupClassName: a,
              popupAnimation: s,
              popupTransitionName: l,
              popupStyle: u,
              mask: c,
              maskAnimation: d,
              maskTransitionName: f,
              zIndex: h,
              stretch: g,
              alignPoint: m,
              mobile: v,
              arrow: b,
              forceRender: y,
            } = this.$props,
            { sPopupVisible: p, point: _ } = this.$data,
            x = D(
              D(
                {
                  prefixCls: o,
                  arrow: b,
                  destroyPopupOnHide: i,
                  visible: p,
                  point: m ? _ : null,
                  align: this.align,
                  animation: s,
                  getClassNameFromAlign: t,
                  stretch: g,
                  getRootDomNode: n,
                  mask: c,
                  zIndex: h,
                  transitionName: l,
                  maskAnimation: d,
                  maskTransitionName: f,
                  class: a,
                  style: u,
                  onAlign: r.onPopupAlign || C_,
                },
                e
              ),
              { ref: this.setPopupRef, mobile: v, forceRender: y }
            )
          return F(AT, x, { default: this.$slots.popup || (() => QS(this, 'popup')) })
        },
        attachParent(e) {
          He.cancel(this.attachId)
          const { getPopupContainer: t, getDocument: n } = this.$props,
            r = this.getRootDomNode()
          let o
          ;(t ? (r || t.length === 0) && (o = t(r)) : (o = n(this.getRootDomNode()).body),
            o
              ? o.appendChild(e)
              : (this.attachId = He(() => {
                  this.attachParent(e)
                })))
        },
        getContainer() {
          const { $props: e } = this,
            { getDocument: t } = e,
            n = t(this.getRootDomNode()).createElement('div')
          return (
            (n.style.position = 'absolute'),
            (n.style.top = '0'),
            (n.style.left = '0'),
            (n.style.width = '100%'),
            this.attachParent(n),
            n
          )
        },
        setPopupVisible(e, t) {
          const { alignPoint: n, sPopupVisible: r, onPopupVisibleChange: o } = this
          ;(this.clearDelayTimer(),
            r !== e &&
              (JS(this, 'popupVisible') || this.setState({ sPopupVisible: e, prevPopupVisible: r }),
              o && o(e)),
            n && t && e && this.setPoint(t))
        },
        setPoint(e) {
          const { alignPoint: t } = this.$props
          !t || !e || this.setState({ point: { pageX: e.pageX, pageY: e.pageY } })
        },
        handlePortalUpdate() {
          this.prevPopupVisible !== this.sPopupVisible &&
            this.afterPopupVisibleChange(this.sPopupVisible)
        },
        delaySetPopupVisible(e, t, n) {
          const r = t * 1e3
          if ((this.clearDelayTimer(), r)) {
            const o = n ? { pageX: n.pageX, pageY: n.pageY } : null
            this.delayTimer = setTimeout(() => {
              ;(this.setPopupVisible(e, o), this.clearDelayTimer())
            }, r)
          } else this.setPopupVisible(e, n)
        },
        clearDelayTimer() {
          this.delayTimer && (clearTimeout(this.delayTimer), (this.delayTimer = null))
        },
        clearOutsideHandler() {
          ;(this.clickOutsideHandler &&
            (this.clickOutsideHandler.remove(), (this.clickOutsideHandler = null)),
            this.contextmenuOutsideHandler1 &&
              (this.contextmenuOutsideHandler1.remove(), (this.contextmenuOutsideHandler1 = null)),
            this.contextmenuOutsideHandler2 &&
              (this.contextmenuOutsideHandler2.remove(), (this.contextmenuOutsideHandler2 = null)),
            this.touchOutsideHandler &&
              (this.touchOutsideHandler.remove(), (this.touchOutsideHandler = null)))
        },
        createTwoChains(e) {
          let t = () => {}
          const n = hh(this)
          return this.childOriginEvents[e] && n[e]
            ? this[`fire${e}`]
            : ((t = this.childOriginEvents[e] || n[e] || t), t)
        },
        isClickToShow() {
          const { action: e, showAction: t } = this.$props
          return e.indexOf('click') !== -1 || t.indexOf('click') !== -1
        },
        isContextMenuOnly() {
          const { action: e } = this.$props
          return e === 'contextmenu' || (e.length === 1 && e[0] === 'contextmenu')
        },
        isContextmenuToShow() {
          const { action: e, showAction: t } = this.$props
          return e.indexOf('contextmenu') !== -1 || t.indexOf('contextmenu') !== -1
        },
        isClickToHide() {
          const { action: e, hideAction: t } = this.$props
          return e.indexOf('click') !== -1 || t.indexOf('click') !== -1
        },
        isMouseEnterToShow() {
          const { action: e, showAction: t } = this.$props
          return e.indexOf('hover') !== -1 || t.indexOf('mouseenter') !== -1
        },
        isMouseLeaveToHide() {
          const { action: e, hideAction: t } = this.$props
          return e.indexOf('hover') !== -1 || t.indexOf('mouseleave') !== -1
        },
        isFocusToShow() {
          const { action: e, showAction: t } = this.$props
          return e.indexOf('focus') !== -1 || t.indexOf('focus') !== -1
        },
        isBlurToHide() {
          const { action: e, hideAction: t } = this.$props
          return e.indexOf('focus') !== -1 || t.indexOf('blur') !== -1
        },
        forcePopupAlign() {
          var e
          this.$data.sPopupVisible &&
            ((e = this.popupRef) === null || e === void 0 || e.forceAlign())
        },
        fireEvents(e, t) {
          this.childOriginEvents[e] && this.childOriginEvents[e](t)
          const n = this.$props[e] || this.$attrs[e]
          n && n(t)
        },
        close() {
          this.setPopupVisible(!1)
        },
      },
      render() {
        const { $attrs: e } = this,
          t = Fr(ZS(this)),
          { alignPoint: n, getPopupContainer: r } = this.$props,
          o = t[0]
        this.childOriginEvents = hh(o)
        const i = { key: 'trigger' }
        ;(this.isContextmenuToShow()
          ? (i.onContextmenu = this.onContextmenu)
          : (i.onContextmenu = this.createTwoChains('onContextmenu')),
          this.isClickToHide() || this.isClickToShow()
            ? ((i.onClick = this.onClick),
              (i.onMousedown = this.onMousedown),
              (i[fn ? 'onTouchstartPassive' : 'onTouchstart'] = this.onTouchstart))
            : ((i.onClick = this.createTwoChains('onClick')),
              (i.onMousedown = this.createTwoChains('onMousedown')),
              (i[fn ? 'onTouchstartPassive' : 'onTouchstart'] =
                this.createTwoChains('onTouchstart'))),
          this.isMouseEnterToShow()
            ? ((i.onMouseenter = this.onMouseenter), n && (i.onMousemove = this.onMouseMove))
            : (i.onMouseenter = this.createTwoChains('onMouseenter')),
          this.isMouseLeaveToHide()
            ? (i.onMouseleave = this.onMouseleave)
            : (i.onMouseleave = this.createTwoChains('onMouseleave')),
          this.isFocusToShow() || this.isBlurToHide()
            ? ((i.onFocus = this.onFocus), (i.onBlur = this.onBlur))
            : ((i.onFocus = this.createTwoChains('onFocus')),
              (i.onBlur = (u) => {
                u &&
                  (!u.relatedTarget || !un(u.target, u.relatedTarget)) &&
                  this.createTwoChains('onBlur')(u)
              })))
        const a = xe(o && o.props && o.props.class, e.class)
        a && (i.class = a)
        const s = Ke(o, D(D({}, i), { ref: 'triggerRef' }), !0, !0),
          l = F(
            Z_,
            {
              key: 'portal',
              getContainer: r && (() => r(this.getRootDomNode())),
              didUpdate: this.handlePortalUpdate,
              visible: this.$data.sPopupVisible,
            },
            { default: this.getComponent }
          )
        return F(Re, null, [s, l])
      },
    }),
    ip = { TAB: 9, ESC: 27 }
  var kT = function (e, t) {
    var n = {}
    for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
    if (e != null && typeof Object.getOwnPropertySymbols == 'function')
      for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
        t.indexOf(r[o]) < 0 &&
          Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
          (n[r[o]] = e[r[o]])
    return n
  }
  const HT = te({
    compatConfig: { MODE: 3 },
    props: {
      disabled: Q.looseBool,
      type: Q.string,
      value: Q.any,
      tag: { type: String, default: 'input' },
      size: Q.string,
      onChange: Function,
      onInput: Function,
      onBlur: Function,
      onFocus: Function,
      onKeydown: Function,
      onCompositionstart: Function,
      onCompositionend: Function,
      onKeyup: Function,
      onPaste: Function,
      onMousedown: Function,
    },
    emits: [
      'change',
      'input',
      'blur',
      'keydown',
      'focus',
      'compositionstart',
      'compositionend',
      'keyup',
      'paste',
      'mousedown',
    ],
    setup(e, t) {
      let { expose: n } = t
      const r = ce(null)
      return (
        n({
          focus: () => {
            r.value && r.value.focus()
          },
          blur: () => {
            r.value && r.value.blur()
          },
          input: r,
          setSelectionRange: (l, u, c) => {
            var d
            ;(d = r.value) === null || d === void 0 || d.setSelectionRange(l, u, c)
          },
          select: () => {
            var l
            ;(l = r.value) === null || l === void 0 || l.select()
          },
          getSelectionStart: () => {
            var l
            return (l = r.value) === null || l === void 0 ? void 0 : l.selectionStart
          },
          getSelectionEnd: () => {
            var l
            return (l = r.value) === null || l === void 0 ? void 0 : l.selectionEnd
          },
          getScrollTop: () => {
            var l
            return (l = r.value) === null || l === void 0 ? void 0 : l.scrollTop
          },
        }),
        () => {
          const { tag: l, value: u } = e,
            c = kT(e, ['tag', 'value'])
          return F(l, oe(oe({}, c), {}, { ref: r, value: u }), null)
        }
      )
    },
  })
  function jT(e) {
    return Object.keys(e).reduce((t, n) => {
      const r = e[n]
      return (typeof r > 'u' || r === null || (t += `${n}: ${e[n]};`), t)
    }, '')
  }
  var VT = function (e, t) {
    var n = {}
    for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
    if (e != null && typeof Object.getOwnPropertySymbols == 'function')
      for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
        t.indexOf(r[o]) < 0 &&
          Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
          (n[r[o]] = e[r[o]])
    return n
  }
  const J_ = te({
      compatConfig: { MODE: 3 },
      inheritAttrs: !1,
      props: {
        disabled: Q.looseBool,
        type: Q.string,
        value: Q.any,
        lazy: Q.bool.def(!0),
        tag: { type: String, default: 'input' },
        size: Q.string,
        style: Q.oneOfType([String, Object]),
        class: Q.string,
      },
      emits: [
        'change',
        'input',
        'blur',
        'keydown',
        'focus',
        'compositionstart',
        'compositionend',
        'keyup',
        'paste',
        'mousedown',
      ],
      setup(e, t) {
        let { emit: n, attrs: r, expose: o } = t
        const i = ce(null),
          a = de(),
          s = de(!1)
        me(
          [() => e.value, s],
          () => {
            s.value || (a.value = e.value)
          },
          { immediate: !0 }
        )
        const l = (w) => {
            n('change', w)
          },
          u = (w) => {
            ;((s.value = !0), (w.target.composing = !0), n('compositionstart', w))
          },
          c = (w) => {
            ;((s.value = !1), (w.target.composing = !1), n('compositionend', w))
            const T = document.createEvent('HTMLEvents')
            ;(T.initEvent('input', !0, !0), w.target.dispatchEvent(T), l(w))
          },
          d = (w) => {
            if (s.value && e.lazy) {
              a.value = w.target.value
              return
            }
            n('input', w)
          },
          f = (w) => {
            n('blur', w)
          },
          h = (w) => {
            n('focus', w)
          },
          g = () => {
            i.value && i.value.focus()
          },
          m = () => {
            i.value && i.value.blur()
          },
          v = (w) => {
            n('keydown', w)
          },
          b = (w) => {
            n('keyup', w)
          },
          y = (w, T, A) => {
            var $
            ;($ = i.value) === null || $ === void 0 || $.setSelectionRange(w, T, A)
          },
          p = () => {
            var w
            ;(w = i.value) === null || w === void 0 || w.select()
          }
        o({
          focus: g,
          blur: m,
          input: X(() => {
            var w
            return (w = i.value) === null || w === void 0 ? void 0 : w.input
          }),
          setSelectionRange: y,
          select: p,
          getSelectionStart: () => {
            var w
            return (w = i.value) === null || w === void 0 ? void 0 : w.getSelectionStart()
          },
          getSelectionEnd: () => {
            var w
            return (w = i.value) === null || w === void 0 ? void 0 : w.getSelectionEnd()
          },
          getScrollTop: () => {
            var w
            return (w = i.value) === null || w === void 0 ? void 0 : w.getScrollTop()
          },
        })
        const _ = (w) => {
            n('mousedown', w)
          },
          x = (w) => {
            n('paste', w)
          },
          S = X(() => (e.style && typeof e.style != 'string' ? jT(e.style) : e.style))
        return () => {
          const { style: w, lazy: T } = e,
            A = VT(e, ['style', 'lazy'])
          return F(
            HT,
            oe(
              oe(oe({}, A), r),
              {},
              {
                style: S.value,
                onInput: d,
                onChange: l,
                onBlur: f,
                onFocus: h,
                ref: i,
                value: a.value,
                onCompositionstart: u,
                onCompositionend: c,
                onKeyup: b,
                onKeydown: v,
                onPaste: x,
                onMousedown: _,
              }
            ),
            null
          )
        }
      },
    }),
    GT = `accept acceptcharset accesskey action allowfullscreen allowtransparency
alt async autocomplete autofocus autoplay capture cellpadding cellspacing challenge
charset checked classid classname colspan cols content contenteditable contextmenu
controls coords crossorigin data datetime default defer dir disabled download draggable
enctype form formaction formenctype formmethod formnovalidate formtarget frameborder
headers height hidden high href hreflang htmlfor for httpequiv icon id inputmode integrity
is keyparams keytype kind label lang list loop low manifest marginheight marginwidth max maxlength media
mediagroup method min minlength multiple muted name novalidate nonce open
optimum pattern placeholder poster preload radiogroup readonly rel required
reversed role rowspan rows sandbox scope scoped scrolling seamless selected
shape size sizes span spellcheck src srcdoc srclang srcset start step style
summary tabindex target title type usemap value width wmode wrap`,
    WT = `onCopy onCut onPaste onCompositionend onCompositionstart onCompositionupdate onKeydown
    onKeypress onKeyup onFocus onBlur onChange onInput onSubmit onClick onContextmenu onDoubleclick onDblclick
    onDrag onDragend onDragenter onDragexit onDragleave onDragover onDragstart onDrop onMousedown
    onMouseenter onMouseleave onMousemove onMouseout onMouseover onMouseup onSelect onTouchcancel
    onTouchend onTouchmove onTouchstart onTouchstartPassive onTouchmovePassive onScroll onWheel onAbort onCanplay onCanplaythrough
    onDurationchange onEmptied onEncrypted onEnded onError onLoadeddata onLoadedmetadata
    onLoadstart onPause onPlay onPlaying onProgress onRatechange onSeeked onSeeking onStalled onSuspend onTimeupdate onVolumechange onWaiting onLoad onError`,
    ap = `${GT} ${WT}`.split(/[\s\n]+/),
    UT = 'aria-',
    YT = 'data-'
  function sp(e, t) {
    return e.indexOf(t) === 0
  }
  function XT(e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1,
      n
    t === !1
      ? (n = { aria: !0, data: !0, attr: !0 })
      : t === !0
        ? (n = { aria: !0 })
        : (n = D({}, t))
    const r = {}
    return (
      Object.keys(e).forEach((o) => {
        ;((n.aria && (o === 'role' || sp(o, UT))) ||
          (n.data && sp(o, YT)) ||
          (n.attr && (ap.includes(o) || ap.includes(o.toLowerCase())))) &&
          (r[o] = e[o])
      }),
      r
    )
  }
  function ln(e) {
    const t = typeof e == 'function' ? e() : e,
      n = de(t)
    function r(o) {
      n.value = o
    }
    return [n, r]
  }
  var KT = {
    icon: {
      tag: 'svg',
      attrs: { viewBox: '64 64 896 896', focusable: 'false' },
      children: [
        {
          tag: 'path',
          attrs: {
            d: 'M909.6 854.5L649.9 594.8C690.2 542.7 712 479 712 412c0-80.2-31.3-155.4-87.9-212.1-56.6-56.7-132-87.9-212.1-87.9s-155.5 31.3-212.1 87.9C143.2 256.5 112 331.8 112 412c0 80.1 31.3 155.5 87.9 212.1C256.5 680.8 331.8 712 412 712c67 0 130.6-21.8 182.7-62l259.7 259.6a8.2 8.2 0 0011.6 0l43.6-43.5a8.2 8.2 0 000-11.6zM570.4 570.4C528 612.7 471.8 636 412 636s-116-23.3-158.4-65.6C211.3 528 188 471.8 188 412s23.3-116.1 65.6-158.4C296 211.3 352.2 188 412 188s116.1 23.2 158.4 65.6S636 352.2 636 412s-23.3 116.1-65.6 158.4z',
          },
        },
      ],
    },
    name: 'search',
    theme: 'outlined',
  }
  function lp(e) {
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
          ZT(e, o, n[o])
        }))
    }
    return e
  }
  function ZT(e, t, n) {
    return (
      t in e
        ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
        : (e[t] = n),
      e
    )
  }
  var bf = function (t, n) {
    var r = lp({}, t, n.attrs)
    return F(kr, lp({}, r, { icon: KT }), null)
  }
  bf.displayName = 'SearchOutlined'
  bf.inheritAttrs = !1
  function _f(e) {
    const t = Symbol('contextKey')
    return {
      useProvide: (o, i) => {
        const a = Ko({})
        return (
          St(t, a),
          Et(() => {
            D(a, o, i || {})
          }),
          a
        )
      },
      useInject: () => xt(t, e) || {},
    }
  }
  const up = Symbol('ContextProps'),
    cp = Symbol('InternalContextProps'),
    dp = {
      id: X(() => {}),
      onFieldBlur: () => {},
      onFieldChange: () => {},
      clearValidate: () => {},
    },
    fp = { addFormItemField: () => {}, removeFormItemField: () => {} },
    Q_ = () => {
      const e = xt(cp, fp),
        t = Symbol('FormItemFieldKey'),
        n = Qe()
      return (
        e.addFormItemField(t, n.type),
        je(() => {
          e.removeFormItemField(t)
        }),
        St(cp, fp),
        St(up, dp),
        xt(up, dp)
      )
    },
    jn = _f({}),
    hp = te({
      name: 'NoFormStatus',
      setup(e, t) {
        let { slots: n } = t
        return (
          jn.useProvide({}),
          () => {
            var r
            return (r = n.default) === null || r === void 0 ? void 0 : r.call(n)
          }
        )
      },
    })
  function yr(e, t, n) {
    return xe({
      [`${e}-status-success`]: t === 'success',
      [`${e}-status-warning`]: t === 'warning',
      [`${e}-status-error`]: t === 'error',
      [`${e}-status-validating`]: t === 'validating',
      [`${e}-has-feedback`]: n,
    })
  }
  const wf = (e, t) => t || e,
    JT = (e) => {
      const { componentCls: t } = e
      return {
        [t]: {
          display: 'inline-flex',
          '&-block': { display: 'flex', width: '100%' },
          '&-vertical': { flexDirection: 'column' },
        },
      }
    },
    QT = (e) => {
      const { componentCls: t } = e
      return {
        [t]: {
          display: 'inline-flex',
          '&-rtl': { direction: 'rtl' },
          '&-vertical': { flexDirection: 'column' },
          '&-align': {
            flexDirection: 'column',
            '&-center': { alignItems: 'center' },
            '&-start': { alignItems: 'flex-start' },
            '&-end': { alignItems: 'flex-end' },
            '&-baseline': { alignItems: 'baseline' },
          },
          [`${t}-item`]: { '&:empty': { display: 'none' } },
        },
      }
    },
    eO = en('Space', (e) => [QT(e), JT(e)])
  var tO = U_(Object.getPrototypeOf, Object),
    nO = '[object Object]',
    rO = Function.prototype,
    oO = Object.prototype,
    ew = rO.toString,
    iO = oO.hasOwnProperty,
    aO = ew.call(Object)
  function sO(e) {
    if (!Hn(e) || Zn(e) != nO) return !1
    var t = tO(e)
    if (t === null) return !0
    var n = iO.call(t, 'constructor') && t.constructor
    return typeof n == 'function' && n instanceof n && ew.call(n) == aO
  }
  var lO = '[object Map]',
    uO = '[object Set]',
    cO = Object.prototype,
    dO = cO.hasOwnProperty
  function tw(e) {
    if (e == null) return !0
    if (
      X_(e) &&
      (Ir(e) || typeof e == 'string' || typeof e.splice == 'function' || Do(e) || yf(e) || H_(e))
    )
      return !e.length
    var t = Pt(e)
    if (t == lO || t == uO) return !e.size
    if (W_(e)) return !Y_(e).length
    for (var n in e) if (dO.call(e, n)) return !1
    return !0
  }
  const fO = () => ({
      compactSize: String,
      compactDirection: Q.oneOf(To('horizontal', 'vertical')).def('horizontal'),
      isFirstItem: Xe(),
      isLastItem: Xe(),
    }),
    ii = _f(null),
    nw = (e, t) => {
      const n = ii.useInject(),
        r = X(() => {
          if (!n || tw(n)) return ''
          const { compactDirection: o, isFirstItem: i, isLastItem: a } = n,
            s = o === 'vertical' ? '-vertical-' : '-'
          return xe({
            [`${e.value}-compact${s}item`]: !0,
            [`${e.value}-compact${s}first-item`]: i,
            [`${e.value}-compact${s}last-item`]: a,
            [`${e.value}-compact${s}item-rtl`]: t.value === 'rtl',
          })
        })
      return {
        compactSize: X(() => n?.compactSize),
        compactDirection: X(() => n?.compactDirection),
        compactItemClassnames: r,
      }
    },
    pp = te({
      name: 'NoCompactStyle',
      setup(e, t) {
        let { slots: n } = t
        return (
          ii.useProvide(null),
          () => {
            var r
            return (r = n.default) === null || r === void 0 ? void 0 : r.call(n)
          }
        )
      },
    }),
    hO = () => ({
      prefixCls: String,
      size: { type: String },
      direction: Q.oneOf(To('horizontal', 'vertical')).def('horizontal'),
      align: Q.oneOf(To('start', 'end', 'center', 'baseline')),
      block: { type: Boolean, default: void 0 },
    }),
    pO = te({
      name: 'CompactItem',
      props: fO(),
      setup(e, t) {
        let { slots: n } = t
        return (
          ii.useProvide(e),
          () => {
            var r
            return (r = n.default) === null || r === void 0 ? void 0 : r.call(n)
          }
        )
      },
    })
  te({
    name: 'ASpaceCompact',
    inheritAttrs: !1,
    props: hO(),
    setup(e, t) {
      let { attrs: n, slots: r } = t
      const { prefixCls: o, direction: i } = Ge('space-compact', e),
        a = ii.useInject(),
        [s, l] = eO(o),
        u = X(() =>
          xe(o.value, l.value, {
            [`${o.value}-rtl`]: i.value === 'rtl',
            [`${o.value}-block`]: e.block,
            [`${o.value}-vertical`]: e.direction === 'vertical',
          })
        )
      return () => {
        var c
        const d = Xn(((c = r.default) === null || c === void 0 ? void 0 : c.call(r)) || [])
        return d.length === 0
          ? null
          : s(
              F('div', oe(oe({}, n), {}, { class: [u.value, n.class] }), [
                d.map((f, h) => {
                  var g
                  const m = (f && f.key) || `${o.value}-item-${h}`,
                    v = !a || tw(a)
                  return F(
                    pO,
                    {
                      key: m,
                      compactSize: (g = e.size) !== null && g !== void 0 ? g : 'middle',
                      compactDirection: e.direction,
                      isFirstItem: h === 0 && (v || a?.isFirstItem),
                      isLastItem: h === d.length - 1 && (v || a?.isLastItem),
                    },
                    { default: () => [f] }
                  )
                }),
              ])
            )
      }
    },
  })
  const vO = (e) => ({ animationDuration: e, animationFillMode: 'both' }),
    gO = (e) => ({ animationDuration: e, animationFillMode: 'both' }),
    rw = function (e, t, n, r) {
      const i = (arguments.length > 4 && arguments[4] !== void 0 ? arguments[4] : !1) ? '&' : ''
      return {
        [`
      ${i}${e}-enter,
      ${i}${e}-appear
    `]: D(D({}, vO(r)), { animationPlayState: 'paused' }),
        [`${i}${e}-leave`]: D(D({}, gO(r)), { animationPlayState: 'paused' }),
        [`
      ${i}${e}-enter${e}-enter-active,
      ${i}${e}-appear${e}-appear-active
    `]: { animationName: t, animationPlayState: 'running' },
        [`${i}${e}-leave${e}-leave-active`]: {
          animationName: n,
          animationPlayState: 'running',
          pointerEvents: 'none',
        },
      }
    },
    mO = new Ye('antFadeIn', { '0%': { opacity: 0 }, '100%': { opacity: 1 } }),
    yO = new Ye('antFadeOut', { '0%': { opacity: 1 }, '100%': { opacity: 0 } }),
    bO = function (e) {
      let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1
      const { antCls: n } = e,
        r = `${n}-fade`,
        o = t ? '&' : ''
      return [
        rw(r, mO, yO, e.motionDurationMid, t),
        {
          [`
        ${o}${r}-enter,
        ${o}${r}-appear
      `]: { opacity: 0, animationTimingFunction: 'linear' },
          [`${o}${r}-leave`]: { animationTimingFunction: 'linear' },
        },
      ]
    },
    _O = new Ye('antZoomIn', {
      '0%': { transform: 'scale(0.2)', opacity: 0 },
      '100%': { transform: 'scale(1)', opacity: 1 },
    }),
    wO = new Ye('antZoomOut', {
      '0%': { transform: 'scale(1)' },
      '100%': { transform: 'scale(0.2)', opacity: 0 },
    }),
    vp = new Ye('antZoomBigIn', {
      '0%': { transform: 'scale(0.8)', opacity: 0 },
      '100%': { transform: 'scale(1)', opacity: 1 },
    }),
    gp = new Ye('antZoomBigOut', {
      '0%': { transform: 'scale(1)' },
      '100%': { transform: 'scale(0.8)', opacity: 0 },
    }),
    SO = new Ye('antZoomUpIn', {
      '0%': { transform: 'scale(0.8)', transformOrigin: '50% 0%', opacity: 0 },
      '100%': { transform: 'scale(1)', transformOrigin: '50% 0%' },
    }),
    xO = new Ye('antZoomUpOut', {
      '0%': { transform: 'scale(1)', transformOrigin: '50% 0%' },
      '100%': { transform: 'scale(0.8)', transformOrigin: '50% 0%', opacity: 0 },
    }),
    CO = new Ye('antZoomLeftIn', {
      '0%': { transform: 'scale(0.8)', transformOrigin: '0% 50%', opacity: 0 },
      '100%': { transform: 'scale(1)', transformOrigin: '0% 50%' },
    }),
    EO = new Ye('antZoomLeftOut', {
      '0%': { transform: 'scale(1)', transformOrigin: '0% 50%' },
      '100%': { transform: 'scale(0.8)', transformOrigin: '0% 50%', opacity: 0 },
    }),
    $O = new Ye('antZoomRightIn', {
      '0%': { transform: 'scale(0.8)', transformOrigin: '100% 50%', opacity: 0 },
      '100%': { transform: 'scale(1)', transformOrigin: '100% 50%' },
    }),
    TO = new Ye('antZoomRightOut', {
      '0%': { transform: 'scale(1)', transformOrigin: '100% 50%' },
      '100%': { transform: 'scale(0.8)', transformOrigin: '100% 50%', opacity: 0 },
    }),
    OO = new Ye('antZoomDownIn', {
      '0%': { transform: 'scale(0.8)', transformOrigin: '50% 100%', opacity: 0 },
      '100%': { transform: 'scale(1)', transformOrigin: '50% 100%' },
    }),
    PO = new Ye('antZoomDownOut', {
      '0%': { transform: 'scale(1)', transformOrigin: '50% 100%' },
      '100%': { transform: 'scale(0.8)', transformOrigin: '50% 100%', opacity: 0 },
    }),
    IO = {
      zoom: { inKeyframes: _O, outKeyframes: wO },
      'zoom-big': { inKeyframes: vp, outKeyframes: gp },
      'zoom-big-fast': { inKeyframes: vp, outKeyframes: gp },
      'zoom-left': { inKeyframes: CO, outKeyframes: EO },
      'zoom-right': { inKeyframes: $O, outKeyframes: TO },
      'zoom-up': { inKeyframes: SO, outKeyframes: xO },
      'zoom-down': { inKeyframes: OO, outKeyframes: PO },
    },
    ow = (e, t) => {
      const { antCls: n } = e,
        r = `${n}-${t}`,
        { inKeyframes: o, outKeyframes: i } = IO[t]
      return [
        rw(r, o, i, t === 'zoom-big-fast' ? e.motionDurationFast : e.motionDurationMid),
        {
          [`
        ${r}-enter,
        ${r}-appear
      `]: {
            transform: 'scale(0)',
            opacity: 0,
            animationTimingFunction: e.motionEaseOutCirc,
            '&-prepare': { transform: 'none' },
          },
          [`${r}-leave`]: { animationTimingFunction: e.motionEaseInOutCirc },
        },
      ]
    },
    AO = (e) => ({
      [e.componentCls]: {
        [`${e.antCls}-motion-collapse-legacy`]: {
          overflow: 'hidden',
          '&-active': {
            transition: `height ${e.motionDurationMid} ${e.motionEaseInOut},
        opacity ${e.motionDurationMid} ${e.motionEaseInOut} !important`,
          },
        },
        [`${e.antCls}-motion-collapse`]: {
          overflow: 'hidden',
          transition: `height ${e.motionDurationMid} ${e.motionEaseInOut},
        opacity ${e.motionDurationMid} ${e.motionEaseInOut} !important`,
        },
      },
    })
  function NO(e, t, n) {
    const { focusElCls: r, focus: o, borderElCls: i } = n,
      a = i ? '> *' : '',
      s = ['hover', o ? 'focus' : null, 'active']
        .filter(Boolean)
        .map((l) => `&:${l} ${a}`)
        .join(',')
    return {
      [`&-item:not(${t}-last-item)`]: { marginInlineEnd: -e.lineWidth },
      '&-item': D(D({ [s]: { zIndex: 2 } }, r ? { [`&${r}`]: { zIndex: 2 } } : {}), {
        [`&[disabled] ${a}`]: { zIndex: 0 },
      }),
    }
  }
  function RO(e, t, n) {
    const { borderElCls: r } = n,
      o = r ? `> ${r}` : ''
    return {
      [`&-item:not(${t}-first-item):not(${t}-last-item) ${o}`]: { borderRadius: 0 },
      [`&-item:not(${t}-last-item)${t}-first-item`]: {
        [`& ${o}, &${e}-sm ${o}, &${e}-lg ${o}`]: {
          borderStartEndRadius: 0,
          borderEndEndRadius: 0,
        },
      },
      [`&-item:not(${t}-first-item)${t}-last-item`]: {
        [`& ${o}, &${e}-sm ${o}, &${e}-lg ${o}`]: {
          borderStartStartRadius: 0,
          borderEndStartRadius: 0,
        },
      },
    }
  }
  function iw(e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : { focus: !0 }
    const { componentCls: n } = e,
      r = `${n}-compact`
    return { [r]: D(D({}, NO(e, r, t)), RO(n, r, t)) }
  }
  const tt = { adjustX: 1, adjustY: 1 },
    nt = [0, 0],
    aw = {
      left: { points: ['cr', 'cl'], overflow: tt, offset: [-4, 0], targetOffset: nt },
      right: { points: ['cl', 'cr'], overflow: tt, offset: [4, 0], targetOffset: nt },
      top: { points: ['bc', 'tc'], overflow: tt, offset: [0, -4], targetOffset: nt },
      bottom: { points: ['tc', 'bc'], overflow: tt, offset: [0, 4], targetOffset: nt },
      topLeft: { points: ['bl', 'tl'], overflow: tt, offset: [0, -4], targetOffset: nt },
      leftTop: { points: ['tr', 'tl'], overflow: tt, offset: [-4, 0], targetOffset: nt },
      topRight: { points: ['br', 'tr'], overflow: tt, offset: [0, -4], targetOffset: nt },
      rightTop: { points: ['tl', 'tr'], overflow: tt, offset: [4, 0], targetOffset: nt },
      bottomRight: { points: ['tr', 'br'], overflow: tt, offset: [0, 4], targetOffset: nt },
      rightBottom: { points: ['bl', 'br'], overflow: tt, offset: [4, 0], targetOffset: nt },
      bottomLeft: { points: ['tl', 'bl'], overflow: tt, offset: [0, 4], targetOffset: nt },
      leftBottom: { points: ['br', 'bl'], overflow: tt, offset: [-4, 0], targetOffset: nt },
    },
    MO = { prefixCls: String, id: String, overlayInnerStyle: Q.any },
    DO = te({
      compatConfig: { MODE: 3 },
      name: 'TooltipContent',
      props: MO,
      setup(e, t) {
        let { slots: n } = t
        return () => {
          var r
          return F(
            'div',
            {
              class: `${e.prefixCls}-inner`,
              id: e.id,
              role: 'tooltip',
              style: e.overlayInnerStyle,
            },
            [(r = n.overlay) === null || r === void 0 ? void 0 : r.call(n)]
          )
        }
      },
    })
  var BO = function (e, t) {
    var n = {}
    for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
    if (e != null && typeof Object.getOwnPropertySymbols == 'function')
      for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
        t.indexOf(r[o]) < 0 &&
          Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
          (n[r[o]] = e[r[o]])
    return n
  }
  function mp() {}
  const qO = te({
      compatConfig: { MODE: 3 },
      name: 'Tooltip',
      inheritAttrs: !1,
      props: {
        trigger: Q.any.def(['hover']),
        defaultVisible: { type: Boolean, default: void 0 },
        visible: { type: Boolean, default: void 0 },
        placement: Q.string.def('right'),
        transitionName: String,
        animation: Q.any,
        afterVisibleChange: Q.func.def(() => {}),
        overlayStyle: { type: Object, default: void 0 },
        overlayClassName: String,
        prefixCls: Q.string.def('rc-tooltip'),
        mouseEnterDelay: Q.number.def(0.1),
        mouseLeaveDelay: Q.number.def(0.1),
        getPopupContainer: Function,
        destroyTooltipOnHide: { type: Boolean, default: !1 },
        align: Q.object.def(() => ({})),
        arrowContent: Q.any.def(null),
        tipId: String,
        builtinPlacements: Q.object,
        overlayInnerStyle: { type: Object, default: void 0 },
        popupVisible: { type: Boolean, default: void 0 },
        onVisibleChange: Function,
        onPopupAlign: Function,
        arrow: { type: Boolean, default: !0 },
      },
      setup(e, t) {
        let { slots: n, attrs: r, expose: o } = t
        const i = ce(),
          a = () => {
            const { prefixCls: c, tipId: d, overlayInnerStyle: f } = e
            return [
              e.arrow
                ? F('div', { class: `${c}-arrow`, key: 'arrow' }, [ex(n, e, 'arrowContent')])
                : null,
              F(
                DO,
                { key: 'content', prefixCls: c, id: d, overlayInnerStyle: f },
                { overlay: n.overlay }
              ),
            ]
          }
        o({
          getPopupDomNode: () => i.value.getPopupDomNode(),
          triggerDOM: i,
          forcePopupAlign: () => {
            var c
            return (c = i.value) === null || c === void 0 ? void 0 : c.forcePopupAlign()
          },
        })
        const l = ce(!1),
          u = ce(!1)
        return (
          Et(() => {
            const { destroyTooltipOnHide: c } = e
            if (typeof c == 'boolean') l.value = c
            else if (c && typeof c == 'object') {
              const { keepParent: d } = c
              ;((l.value = d === !0), (u.value = d === !1))
            }
          }),
          () => {
            const {
                overlayClassName: c,
                trigger: d,
                mouseEnterDelay: f,
                mouseLeaveDelay: h,
                overlayStyle: g,
                prefixCls: m,
                afterVisibleChange: v,
                transitionName: b,
                animation: y,
                placement: p,
                align: _,
                destroyTooltipOnHide: x,
                defaultVisible: S,
              } = e,
              w = BO(e, [
                'overlayClassName',
                'trigger',
                'mouseEnterDelay',
                'mouseLeaveDelay',
                'overlayStyle',
                'prefixCls',
                'afterVisibleChange',
                'transitionName',
                'animation',
                'placement',
                'align',
                'destroyTooltipOnHide',
                'defaultVisible',
              ]),
              T = D({}, w)
            e.visible !== void 0 && (T.popupVisible = e.visible)
            const A = D(
              D(
                D(
                  {
                    popupClassName: c,
                    prefixCls: m,
                    action: d,
                    builtinPlacements: aw,
                    popupPlacement: p,
                    popupAlign: _,
                    afterPopupVisibleChange: v,
                    popupTransitionName: b,
                    popupAnimation: y,
                    defaultPopupVisible: S,
                    destroyPopupOnHide: l.value,
                    autoDestroy: u.value,
                    mouseLeaveDelay: h,
                    popupStyle: g,
                    mouseEnterDelay: f,
                  },
                  T
                ),
                r
              ),
              {
                onPopupVisibleChange: e.onVisibleChange || mp,
                onPopupAlign: e.onPopupAlign || mp,
                ref: i,
                arrow: !!e.arrow,
                popup: a(),
              }
            )
            return F(FT, A, { default: n.default })
          }
        )
      },
    }),
    zO = () => ({
      trigger: [String, Array],
      open: { type: Boolean, default: void 0 },
      visible: { type: Boolean, default: void 0 },
      placement: String,
      color: String,
      transitionName: String,
      overlayStyle: st(),
      overlayInnerStyle: st(),
      overlayClassName: String,
      openClassName: String,
      prefixCls: String,
      mouseEnterDelay: Number,
      mouseLeaveDelay: Number,
      getPopupContainer: Function,
      arrowPointAtCenter: { type: Boolean, default: void 0 },
      arrow: { type: [Boolean, Object], default: !0 },
      autoAdjustOverflow: { type: [Boolean, Object], default: void 0 },
      destroyTooltipOnHide: { type: Boolean, default: void 0 },
      align: st(),
      builtinPlacements: st(),
      children: Array,
      onVisibleChange: Function,
      'onUpdate:visible': Function,
      onOpenChange: Function,
      'onUpdate:open': Function,
    }),
    LO = { adjustX: 1, adjustY: 1 },
    yp = { adjustX: 0, adjustY: 0 },
    FO = [0, 0]
  function bp(e) {
    return typeof e == 'boolean' ? (e ? LO : yp) : D(D({}, yp), e)
  }
  function kO(e) {
    const {
        arrowWidth: t = 4,
        horizontalArrowShift: n = 16,
        verticalArrowShift: r = 8,
        autoAdjustOverflow: o,
        arrowPointAtCenter: i,
      } = e,
      a = {
        left: { points: ['cr', 'cl'], offset: [-4, 0] },
        right: { points: ['cl', 'cr'], offset: [4, 0] },
        top: { points: ['bc', 'tc'], offset: [0, -4] },
        bottom: { points: ['tc', 'bc'], offset: [0, 4] },
        topLeft: { points: ['bl', 'tc'], offset: [-(n + t), -4] },
        leftTop: { points: ['tr', 'cl'], offset: [-4, -(r + t)] },
        topRight: { points: ['br', 'tc'], offset: [n + t, -4] },
        rightTop: { points: ['tl', 'cr'], offset: [4, -(r + t)] },
        bottomRight: { points: ['tr', 'bc'], offset: [n + t, 4] },
        rightBottom: { points: ['bl', 'cr'], offset: [4, r + t] },
        bottomLeft: { points: ['tl', 'bc'], offset: [-(n + t), 4] },
        leftBottom: { points: ['br', 'cl'], offset: [-4, r + t] },
      }
    return (
      Object.keys(a).forEach((s) => {
        ;((a[s] = i
          ? D(D({}, a[s]), { overflow: bp(o), targetOffset: FO })
          : D(D({}, aw[s]), { overflow: bp(o) })),
          (a[s].ignoreShake = !0))
      }),
      a
    )
  }
  function sw() {
    let e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : []
    for (let t = 0, n = e.length; t < n; t++) if (e[t] !== void 0) return e[t]
  }
  const HO = No.map((e) => `${e}-inverse`),
    jO = ['success', 'processing', 'error', 'default', 'warning']
  function lw(e) {
    return (arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0)
      ? [...HO, ...No].includes(e)
      : No.includes(e)
  }
  function VO(e) {
    return jO.includes(e)
  }
  function GO(e, t) {
    const n = lw(t),
      r = xe({ [`${e}-${t}`]: t && n }),
      o = {},
      i = {}
    return (
      t && !n && ((o.background = t), (i['--antd-arrow-background-color'] = t)),
      { className: r, overlayStyle: o, arrowStyle: i }
    )
  }
  function ao(e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : ''
    return e.map((n) => `${t}${n}`).join(',')
  }
  const uw = 8
  function WO(e) {
    const t = uw,
      { sizePopupArrow: n, contentRadius: r, borderRadiusOuter: o } = e,
      i = n / 2 - Math.ceil(o * (Math.sqrt(2) - 1)),
      a = (r > 12 ? r + 2 : 12) - i,
      s = t - i
    return { dropdownArrowOffset: a, dropdownArrowOffsetVertical: s }
  }
  function UO(e, t) {
    const {
        componentCls: n,
        sizePopupArrow: r,
        marginXXS: o,
        borderRadiusXS: i,
        borderRadiusOuter: a,
        boxShadowPopoverArrow: s,
      } = e,
      { colorBg: l, showArrowCls: u, contentRadius: c = e.borderRadiusLG } = t,
      { dropdownArrowOffsetVertical: d, dropdownArrowOffset: f } = WO({
        sizePopupArrow: r,
        contentRadius: c,
        borderRadiusOuter: a,
      }),
      h = r / 2 + o
    return {
      [n]: {
        [`${n}-arrow`]: [
          D(D({ position: 'absolute', zIndex: 1, display: 'block' }, oC(r, i, a, l, s)), {
            '&:before': { background: l },
          }),
        ],
        [[
          `&-placement-top ${n}-arrow`,
          `&-placement-topLeft ${n}-arrow`,
          `&-placement-topRight ${n}-arrow`,
        ].join(',')]: { bottom: 0, transform: 'translateY(100%) rotate(180deg)' },
        [`&-placement-top ${n}-arrow`]: {
          left: { _skip_check_: !0, value: '50%' },
          transform: 'translateX(-50%) translateY(100%) rotate(180deg)',
        },
        [`&-placement-topLeft ${n}-arrow`]: { left: { _skip_check_: !0, value: f } },
        [`&-placement-topRight ${n}-arrow`]: { right: { _skip_check_: !0, value: f } },
        [[
          `&-placement-bottom ${n}-arrow`,
          `&-placement-bottomLeft ${n}-arrow`,
          `&-placement-bottomRight ${n}-arrow`,
        ].join(',')]: { top: 0, transform: 'translateY(-100%)' },
        [`&-placement-bottom ${n}-arrow`]: {
          left: { _skip_check_: !0, value: '50%' },
          transform: 'translateX(-50%) translateY(-100%)',
        },
        [`&-placement-bottomLeft ${n}-arrow`]: { left: { _skip_check_: !0, value: f } },
        [`&-placement-bottomRight ${n}-arrow`]: { right: { _skip_check_: !0, value: f } },
        [[
          `&-placement-left ${n}-arrow`,
          `&-placement-leftTop ${n}-arrow`,
          `&-placement-leftBottom ${n}-arrow`,
        ].join(',')]: {
          right: { _skip_check_: !0, value: 0 },
          transform: 'translateX(100%) rotate(90deg)',
        },
        [`&-placement-left ${n}-arrow`]: {
          top: { _skip_check_: !0, value: '50%' },
          transform: 'translateY(-50%) translateX(100%) rotate(90deg)',
        },
        [`&-placement-leftTop ${n}-arrow`]: { top: d },
        [`&-placement-leftBottom ${n}-arrow`]: { bottom: d },
        [[
          `&-placement-right ${n}-arrow`,
          `&-placement-rightTop ${n}-arrow`,
          `&-placement-rightBottom ${n}-arrow`,
        ].join(',')]: {
          left: { _skip_check_: !0, value: 0 },
          transform: 'translateX(-100%) rotate(-90deg)',
        },
        [`&-placement-right ${n}-arrow`]: {
          top: { _skip_check_: !0, value: '50%' },
          transform: 'translateY(-50%) translateX(-100%) rotate(-90deg)',
        },
        [`&-placement-rightTop ${n}-arrow`]: { top: d },
        [`&-placement-rightBottom ${n}-arrow`]: { bottom: d },
        [ao(
          ['&-placement-topLeft', '&-placement-top', '&-placement-topRight'].map(
            (g) => (g += ':not(&-arrow-hidden)')
          ),
          u
        )]: { paddingBottom: h },
        [ao(
          ['&-placement-bottomLeft', '&-placement-bottom', '&-placement-bottomRight'].map(
            (g) => (g += ':not(&-arrow-hidden)')
          ),
          u
        )]: { paddingTop: h },
        [ao(
          ['&-placement-leftTop', '&-placement-left', '&-placement-leftBottom'].map(
            (g) => (g += ':not(&-arrow-hidden)')
          ),
          u
        )]: { paddingRight: { _skip_check_: !0, value: h } },
        [ao(
          ['&-placement-rightTop', '&-placement-right', '&-placement-rightBottom'].map(
            (g) => (g += ':not(&-arrow-hidden)')
          ),
          u
        )]: { paddingLeft: { _skip_check_: !0, value: h } },
      },
    }
  }
  const YO = (e) => {
      const {
        componentCls: t,
        tooltipMaxWidth: n,
        tooltipColor: r,
        tooltipBg: o,
        tooltipBorderRadius: i,
        zIndexPopup: a,
        controlHeight: s,
        boxShadowSecondary: l,
        paddingSM: u,
        paddingXS: c,
        tooltipRadiusOuter: d,
      } = e
      return [
        {
          [t]: D(
            D(
              D(D({}, Kn(e)), {
                position: 'absolute',
                zIndex: a,
                display: 'block',
                '&': [{ width: 'max-content' }, { width: 'intrinsic' }],
                maxWidth: n,
                visibility: 'visible',
                '&-hidden': { display: 'none' },
                '--antd-arrow-background-color': o,
                [`${t}-inner`]: {
                  minWidth: s,
                  minHeight: s,
                  padding: `${u / 2}px ${c}px`,
                  color: r,
                  textAlign: 'start',
                  textDecoration: 'none',
                  wordWrap: 'break-word',
                  backgroundColor: o,
                  borderRadius: i,
                  boxShadow: l,
                },
                [[
                  '&-placement-left',
                  '&-placement-leftTop',
                  '&-placement-leftBottom',
                  '&-placement-right',
                  '&-placement-rightTop',
                  '&-placement-rightBottom',
                ].join(',')]: { [`${t}-inner`]: { borderRadius: Math.min(i, uw) } },
                [`${t}-content`]: { position: 'relative' },
              }),
              x_(e, (f, h) => {
                let { darkColor: g } = h
                return {
                  [`&${t}-${f}`]: {
                    [`${t}-inner`]: { backgroundColor: g },
                    [`${t}-arrow`]: { '--antd-arrow-background-color': g },
                  },
                }
              })
            ),
            { '&-rtl': { direction: 'rtl' } }
          ),
        },
        UO(ot(e, { borderRadiusOuter: d }), {
          colorBg: 'var(--antd-arrow-background-color)',
          showArrowCls: '',
          contentRadius: i,
        }),
        { [`${t}-pure`]: { position: 'relative', maxWidth: 'none' } },
      ]
    },
    XO = (e, t) =>
      en(
        'Tooltip',
        (r) => {
          if (t?.value === !1) return []
          const {
              borderRadius: o,
              colorTextLightSolid: i,
              colorBgDefault: a,
              borderRadiusOuter: s,
            } = r,
            l = ot(r, {
              tooltipMaxWidth: 250,
              tooltipColor: i,
              tooltipBorderRadius: o,
              tooltipBg: a,
              tooltipRadiusOuter: s > 4 ? 4 : s,
            })
          return [YO(l), ow(r, 'zoom-big-fast')]
        },
        (r) => {
          let { zIndexPopupBase: o, colorBgSpotlight: i } = r
          return { zIndexPopup: o + 70, colorBgDefault: i }
        }
      )(e),
    KO = (e, t) => {
      const n = {},
        r = D({}, e)
      return (
        t.forEach((o) => {
          e && o in e && ((n[o] = e[o]), delete r[o])
        }),
        { picked: n, omitted: r }
      )
    },
    ZO = () => D(D({}, zO()), { title: Q.any }),
    JO = te({
      compatConfig: { MODE: 3 },
      name: 'ATooltip',
      inheritAttrs: !1,
      props: tn(ZO(), {
        trigger: 'hover',
        align: {},
        placement: 'top',
        mouseEnterDelay: 0.1,
        mouseLeaveDelay: 0.1,
        arrowPointAtCenter: !1,
        autoAdjustOverflow: !0,
      }),
      slots: Object,
      setup(e, t) {
        let { slots: n, emit: r, attrs: o, expose: i } = t
        const {
            prefixCls: a,
            getPopupContainer: s,
            direction: l,
            rootPrefixCls: u,
          } = Ge('tooltip', e),
          c = X(() => {
            var $
            return ($ = e.open) !== null && $ !== void 0 ? $ : e.visible
          }),
          d = de(sw([e.open, e.visible])),
          f = de()
        let h
        me(c, ($) => {
          ;(He.cancel(h),
            (h = He(() => {
              d.value = !!$
            })))
        })
        const g = () => {
            var $
            const P = ($ = e.title) !== null && $ !== void 0 ? $ : n.title
            return !P && P !== 0
          },
          m = ($) => {
            const P = g()
            ;(c.value === void 0 && (d.value = P ? !1 : $),
              P ||
                (r('update:visible', $),
                r('visibleChange', $),
                r('update:open', $),
                r('openChange', $)))
          }
        i({
          getPopupDomNode: () => f.value.getPopupDomNode(),
          open: d,
          forcePopupAlign: () => {
            var $
            return ($ = f.value) === null || $ === void 0 ? void 0 : $.forcePopupAlign()
          },
        })
        const b = X(() => {
            var $
            const {
              builtinPlacements: P,
              autoAdjustOverflow: E,
              arrow: z,
              arrowPointAtCenter: C,
            } = e
            let R = C
            return (
              typeof z == 'object' && (R = ($ = z.pointAtCenter) !== null && $ !== void 0 ? $ : C),
              P || kO({ arrowPointAtCenter: R, autoAdjustOverflow: E })
            )
          }),
          y = ($) => $ || $ === '',
          p = ($) => {
            const P = $.type
            if (
              typeof P == 'object' &&
              $.props &&
              (((P.__ANT_BUTTON === !0 || P === 'button') && y($.props.disabled)) ||
                (P.__ANT_SWITCH === !0 && (y($.props.disabled) || y($.props.loading))) ||
                (P.__ANT_RADIO === !0 && y($.props.disabled)))
            ) {
              const { picked: E, omitted: z } = KO(nx($), [
                  'position',
                  'left',
                  'right',
                  'top',
                  'bottom',
                  'float',
                  'display',
                  'zIndex',
                ]),
                C = D(D({ display: 'inline-block' }, E), {
                  cursor: 'not-allowed',
                  lineHeight: 1,
                  width: $.props && $.props.block ? '100%' : void 0,
                }),
                R = D(D({}, z), { pointerEvents: 'none' }),
                N = Ke($, { style: R }, !0)
              return F('span', { style: C, class: `${a.value}-disabled-compatible-wrapper` }, [N])
            }
            return $
          },
          _ = () => {
            var $, P
            return ($ = e.title) !== null && $ !== void 0
              ? $
              : (P = n.title) === null || P === void 0
                ? void 0
                : P.call(n)
          },
          x = ($, P) => {
            const E = b.value,
              z = Object.keys(E).find((C) => {
                var R, N
                return (
                  E[C].points[0] === ((R = P.points) === null || R === void 0 ? void 0 : R[0]) &&
                  E[C].points[1] === ((N = P.points) === null || N === void 0 ? void 0 : N[1])
                )
              })
            if (z) {
              const C = $.getBoundingClientRect(),
                R = { top: '50%', left: '50%' }
              ;(z.indexOf('top') >= 0 || z.indexOf('Bottom') >= 0
                ? (R.top = `${C.height - P.offset[1]}px`)
                : (z.indexOf('Top') >= 0 || z.indexOf('bottom') >= 0) &&
                  (R.top = `${-P.offset[1]}px`),
                z.indexOf('left') >= 0 || z.indexOf('Right') >= 0
                  ? (R.left = `${C.width - P.offset[0]}px`)
                  : (z.indexOf('right') >= 0 || z.indexOf('Left') >= 0) &&
                    (R.left = `${-P.offset[0]}px`),
                ($.style.transformOrigin = `${R.left} ${R.top}`))
            }
          },
          S = X(() => GO(a.value, e.color)),
          w = X(() => o['data-popover-inject']),
          [T, A] = XO(
            a,
            X(() => !w.value)
          )
        return () => {
          var $, P
          const { openClassName: E, overlayClassName: z, overlayStyle: C, overlayInnerStyle: R } = e
          let N =
            (P = Fr(($ = n.default) === null || $ === void 0 ? void 0 : $.call(n))) !== null &&
            P !== void 0
              ? P
              : null
          N = N.length === 1 ? N[0] : N
          let j = d.value
          if ((c.value === void 0 && g() && (j = !1), !N)) return null
          const V = p(rf(N) && !tx(N) ? N : F('span', null, [N])),
            H = xe({
              [E || `${a.value}-open`]: !0,
              [V.props && V.props.class]: V.props && V.props.class,
            }),
            G = xe(z, { [`${a.value}-rtl`]: l.value === 'rtl' }, S.value.className, A.value),
            Y = D(D({}, S.value.overlayStyle), R),
            Z = S.value.arrowStyle,
            ne = D(D(D({}, o), e), {
              prefixCls: a.value,
              arrow: !!e.arrow,
              getPopupContainer: s?.value,
              builtinPlacements: b.value,
              visible: j,
              ref: f,
              overlayClassName: G,
              overlayStyle: D(D({}, Z), C),
              overlayInnerStyle: Y,
              onVisibleChange: m,
              onPopupAlign: x,
              transitionName: Er(u.value, 'zoom-big-fast', e.transitionName),
            })
          return T(
            F(qO, ne, {
              default: () => [d.value ? Ke(V, { class: H }) : V],
              arrowContent: () => F('span', { class: `${a.value}-arrow-content` }, null),
              overlay: _,
            })
          )
        }
      },
    }),
    QO = rx(JO),
    eP = (e) => {
      const { componentCls: t, colorPrimary: n } = e
      return {
        [t]: {
          position: 'absolute',
          background: 'transparent',
          pointerEvents: 'none',
          boxSizing: 'border-box',
          color: `var(--wave-color, ${n})`,
          boxShadow: '0 0 0 0 currentcolor',
          opacity: 0.2,
          '&.wave-motion-appear': {
            transition: [
              `box-shadow 0.4s ${e.motionEaseOutCirc}`,
              `opacity 2s ${e.motionEaseOutCirc}`,
            ].join(','),
            '&-active': { boxShadow: '0 0 0 6px currentcolor', opacity: 0 },
          },
        },
      }
    },
    tP = en('Wave', (e) => [eP(e)])
  function nP(e) {
    const t = (e || '').match(/rgba?\((\d*), (\d*), (\d*)(, [\d.]*)?\)/)
    return t && t[1] && t[2] && t[3] ? !(t[1] === t[2] && t[2] === t[3]) : !0
  }
  function Vi(e) {
    return (
      e &&
      e !== '#fff' &&
      e !== '#ffffff' &&
      e !== 'rgb(255, 255, 255)' &&
      e !== 'rgba(255, 255, 255, 1)' &&
      nP(e) &&
      !/rgba\((?:\d*, ){3}0\)/.test(e) &&
      e !== 'transparent'
    )
  }
  function rP(e) {
    const { borderTopColor: t, borderColor: n, backgroundColor: r } = getComputedStyle(e)
    return Vi(t) ? t : Vi(n) ? n : Vi(r) ? r : null
  }
  function Gi(e) {
    return Number.isNaN(e) ? 0 : e
  }
  const oP = te({
    props: { target: st(), className: String },
    setup(e) {
      const t = ce(null),
        [n, r] = ln(null),
        [o, i] = ln([]),
        [a, s] = ln(0),
        [l, u] = ln(0),
        [c, d] = ln(0),
        [f, h] = ln(0),
        [g, m] = ln(!1)
      function v() {
        const { target: w } = e,
          T = getComputedStyle(w)
        r(rP(w))
        const A = T.position === 'static',
          { borderLeftWidth: $, borderTopWidth: P } = T
        ;(s(A ? w.offsetLeft : Gi(-parseFloat($))),
          u(A ? w.offsetTop : Gi(-parseFloat(P))),
          d(w.offsetWidth),
          h(w.offsetHeight))
        const {
          borderTopLeftRadius: E,
          borderTopRightRadius: z,
          borderBottomLeftRadius: C,
          borderBottomRightRadius: R,
        } = T
        i([E, z, R, C].map((N) => Gi(parseFloat(N))))
      }
      let b, y, p
      const _ = () => {
          ;(clearTimeout(p), He.cancel(y), b?.disconnect())
        },
        x = () => {
          var w
          const T = (w = t.value) === null || w === void 0 ? void 0 : w.parentElement
          T && (Ln(null, T), T.parentElement && T.parentElement.removeChild(T))
        }
      ;(Me(() => {
        ;(_(),
          (p = setTimeout(() => {
            x()
          }, 5e3)))
        const { target: w } = e
        w &&
          ((y = He(() => {
            ;(v(), m(!0))
          })),
          typeof ResizeObserver < 'u' && ((b = new ResizeObserver(v)), b.observe(w)))
      }),
        je(() => {
          _()
        }))
      const S = (w) => {
        w.propertyName === 'opacity' && x()
      }
      return () => {
        if (!g.value) return null
        const w = {
          left: `${a.value}px`,
          top: `${l.value}px`,
          width: `${c.value}px`,
          height: `${f.value}px`,
          borderRadius: o.value.map((T) => `${T}px`).join(' '),
        }
        return (
          n && (w['--wave-color'] = n.value),
          F(
            Qt,
            {
              appear: !0,
              name: 'wave-motion',
              appearFromClass: 'wave-motion-appear',
              appearActiveClass: 'wave-motion-appear',
              appearToClass: 'wave-motion-appear wave-motion-appear-active',
            },
            {
              default: () => [
                F('div', { ref: t, class: e.className, style: w, onTransitionend: S }, null),
              ],
            }
          )
        )
      }
    },
  })
  function iP(e, t) {
    const n = document.createElement('div')
    return (
      (n.style.position = 'absolute'),
      (n.style.left = '0px'),
      (n.style.top = '0px'),
      e?.insertBefore(n, e?.firstChild),
      Ln(F(oP, { target: e, className: t }, null), n),
      () => {
        ;(Ln(null, n), n.parentElement && n.parentElement.removeChild(n))
      }
    )
  }
  function aP(e, t) {
    const n = Qe()
    let r
    function o() {
      var i
      const a = At(n)
      ;(r?.(),
        !((!((i = t?.value) === null || i === void 0) && i.disabled) || !a) && (r = iP(a, e.value)))
    }
    return (
      je(() => {
        r?.()
      }),
      o
    )
  }
  const cw = te({
    compatConfig: { MODE: 3 },
    name: 'Wave',
    props: { disabled: Boolean },
    setup(e, t) {
      let { slots: n } = t
      const r = Qe(),
        { prefixCls: o, wave: i } = Ge('wave', e),
        [, a] = tP(o),
        s = aP(
          X(() => xe(o.value, a.value)),
          i
        )
      let l
      const u = () => {
        At(r).removeEventListener('click', l, !0)
      }
      return (
        Me(() => {
          me(
            () => e.disabled,
            () => {
              ;(u(),
                Ne(() => {
                  const c = At(r)
                  ;(c?.removeEventListener('click', l, !0),
                    !(!c || c.nodeType !== 1 || e.disabled) &&
                      ((l = (d) => {
                        d.target.tagName === 'INPUT' ||
                          !M_(d.target) ||
                          !c.getAttribute ||
                          c.getAttribute('disabled') ||
                          c.disabled ||
                          c.className.includes('disabled') ||
                          c.className.includes('-leave') ||
                          s()
                      }),
                      c.addEventListener('click', l, !0)))
                }))
            },
            { immediate: !0, flush: 'post' }
          )
        }),
        je(() => {
          u()
        }),
        () => {
          var c
          return (c = n.default) === null || c === void 0 ? void 0 : c.call(n)[0]
        }
      )
    },
  })
  function dw(e) {
    return e === 'danger' ? { danger: !0 } : { type: e }
  }
  const sP = () => ({
      prefixCls: String,
      type: String,
      htmlType: { type: String, default: 'button' },
      shape: { type: String },
      size: { type: String },
      loading: { type: [Boolean, Object], default: () => !1 },
      disabled: { type: Boolean, default: void 0 },
      ghost: { type: Boolean, default: void 0 },
      block: { type: Boolean, default: void 0 },
      danger: { type: Boolean, default: void 0 },
      icon: Q.any,
      href: String,
      target: String,
      title: String,
      onClick: $r(),
      onMousedown: $r(),
    }),
    _p = (e) => {
      e && ((e.style.width = '0px'), (e.style.opacity = '0'), (e.style.transform = 'scale(0)'))
    },
    wp = (e) => {
      Ne(() => {
        e &&
          ((e.style.width = `${e.scrollWidth}px`),
          (e.style.opacity = '1'),
          (e.style.transform = 'scale(1)'))
      })
    },
    Sp = (e) => {
      e && e.style && ((e.style.width = null), (e.style.opacity = null), (e.style.transform = null))
    },
    lP = te({
      compatConfig: { MODE: 3 },
      name: 'LoadingIcon',
      props: { prefixCls: String, loading: [Boolean, Object], existIcon: Boolean },
      setup(e) {
        return () => {
          const { existIcon: t, prefixCls: n, loading: r } = e
          if (t) return F('span', { class: `${n}-loading-icon` }, [F(ph, null, null)])
          const o = !!r
          return F(
            Qt,
            {
              name: `${n}-loading-icon-motion`,
              onBeforeEnter: _p,
              onEnter: wp,
              onAfterEnter: Sp,
              onBeforeLeave: wp,
              onLeave: (i) => {
                setTimeout(() => {
                  _p(i)
                })
              },
              onAfterLeave: Sp,
            },
            {
              default: () => [
                o ? F('span', { class: `${n}-loading-icon` }, [F(ph, null, null)]) : null,
              ],
            }
          )
        }
      },
    }),
    xp = (e, t) => ({
      [`> span, > ${e}`]: {
        '&:not(:last-child)': {
          [`&, & > ${e}`]: { '&:not(:disabled)': { borderInlineEndColor: t } },
        },
        '&:not(:first-child)': {
          [`&, & > ${e}`]: { '&:not(:disabled)': { borderInlineStartColor: t } },
        },
      },
    }),
    uP = (e) => {
      const {
        componentCls: t,
        fontSize: n,
        lineWidth: r,
        colorPrimaryHover: o,
        colorErrorHover: i,
      } = e
      return {
        [`${t}-group`]: [
          {
            position: 'relative',
            display: 'inline-flex',
            [`> span, > ${t}`]: {
              '&:not(:last-child)': {
                [`&, & > ${t}`]: { borderStartEndRadius: 0, borderEndEndRadius: 0 },
              },
              '&:not(:first-child)': {
                marginInlineStart: -r,
                [`&, & > ${t}`]: { borderStartStartRadius: 0, borderEndStartRadius: 0 },
              },
            },
            [t]: {
              position: 'relative',
              zIndex: 1,
              '&:hover,\n          &:focus,\n          &:active': { zIndex: 2 },
              '&[disabled]': { zIndex: 0 },
            },
            [`${t}-icon-only`]: { fontSize: n },
          },
          xp(`${t}-primary`, o),
          xp(`${t}-danger`, i),
        ],
      }
    }
  function cP(e, t) {
    return {
      [`&-item:not(${t}-last-item)`]: { marginBottom: -e.lineWidth },
      '&-item': { '&:hover,&:focus,&:active': { zIndex: 2 }, '&[disabled]': { zIndex: 0 } },
    }
  }
  function dP(e, t) {
    return {
      [`&-item:not(${t}-first-item):not(${t}-last-item)`]: { borderRadius: 0 },
      [`&-item${t}-first-item:not(${t}-last-item)`]: {
        [`&, &${e}-sm, &${e}-lg`]: { borderEndEndRadius: 0, borderEndStartRadius: 0 },
      },
      [`&-item${t}-last-item:not(${t}-first-item)`]: {
        [`&, &${e}-sm, &${e}-lg`]: { borderStartStartRadius: 0, borderStartEndRadius: 0 },
      },
    }
  }
  function fP(e) {
    const t = `${e.componentCls}-compact-vertical`
    return { [t]: D(D({}, cP(e, t)), dP(e.componentCls, t)) }
  }
  const hP = (e) => {
      const { componentCls: t, iconCls: n } = e
      return {
        [t]: {
          outline: 'none',
          position: 'relative',
          display: 'inline-block',
          fontWeight: 400,
          whiteSpace: 'nowrap',
          textAlign: 'center',
          backgroundImage: 'none',
          backgroundColor: 'transparent',
          border: `${e.lineWidth}px ${e.lineType} transparent`,
          cursor: 'pointer',
          transition: `all ${e.motionDurationMid} ${e.motionEaseInOut}`,
          userSelect: 'none',
          touchAction: 'manipulation',
          lineHeight: e.lineHeight,
          color: e.colorText,
          '> span': { display: 'inline-block' },
          [`> ${n} + span, > span + ${n}`]: { marginInlineStart: e.marginXS },
          '> a': { color: 'currentColor' },
          '&:not(:disabled)': D({}, s_(e)),
          [`&-icon-only${t}-compact-item`]: { flex: 'none' },
          [`&-compact-item${t}-primary`]: {
            [`&:not([disabled]) + ${t}-compact-item${t}-primary:not([disabled])`]: {
              position: 'relative',
              '&:before': {
                position: 'absolute',
                top: -e.lineWidth,
                insetInlineStart: -e.lineWidth,
                display: 'inline-block',
                width: e.lineWidth,
                height: `calc(100% + ${e.lineWidth * 2}px)`,
                backgroundColor: e.colorPrimaryHover,
                content: '""',
              },
            },
          },
          '&-compact-vertical-item': {
            [`&${t}-primary`]: {
              [`&:not([disabled]) + ${t}-compact-vertical-item${t}-primary:not([disabled])`]: {
                position: 'relative',
                '&:before': {
                  position: 'absolute',
                  top: -e.lineWidth,
                  insetInlineStart: -e.lineWidth,
                  display: 'inline-block',
                  width: `calc(100% + ${e.lineWidth * 2}px)`,
                  height: e.lineWidth,
                  backgroundColor: e.colorPrimaryHover,
                  content: '""',
                },
              },
            },
          },
        },
      }
    },
    Bt = (e, t) => ({ '&:not(:disabled)': { '&:hover': e, '&:active': t } }),
    pP = (e) => ({
      minWidth: e.controlHeight,
      paddingInlineStart: 0,
      paddingInlineEnd: 0,
      borderRadius: '50%',
    }),
    vP = (e) => ({
      borderRadius: e.controlHeight,
      paddingInlineStart: e.controlHeight / 2,
      paddingInlineEnd: e.controlHeight / 2,
    }),
    Md = (e) => ({
      cursor: 'not-allowed',
      borderColor: e.colorBorder,
      color: e.colorTextDisabled,
      backgroundColor: e.colorBgContainerDisabled,
      boxShadow: 'none',
    }),
    Bo = (e, t, n, r, o, i, a) => ({
      [`&${e}-background-ghost`]: D(
        D(
          {
            color: t || void 0,
            backgroundColor: 'transparent',
            borderColor: n || void 0,
            boxShadow: 'none',
          },
          Bt(D({ backgroundColor: 'transparent' }, i), D({ backgroundColor: 'transparent' }, a))
        ),
        { '&:disabled': { cursor: 'not-allowed', color: r || void 0, borderColor: o || void 0 } }
      ),
    }),
    Sf = (e) => ({ '&:disabled': D({}, Md(e)) }),
    fw = (e) => D({}, Sf(e)),
    qo = (e) => ({ '&:disabled': { cursor: 'not-allowed', color: e.colorTextDisabled } }),
    hw = (e) =>
      D(
        D(
          D(
            D(D({}, fw(e)), {
              backgroundColor: e.colorBgContainer,
              borderColor: e.colorBorder,
              boxShadow: `0 ${e.controlOutlineWidth}px 0 ${e.controlTmpOutline}`,
            }),
            Bt(
              { color: e.colorPrimaryHover, borderColor: e.colorPrimaryHover },
              { color: e.colorPrimaryActive, borderColor: e.colorPrimaryActive }
            )
          ),
          Bo(
            e.componentCls,
            e.colorBgContainer,
            e.colorBgContainer,
            e.colorTextDisabled,
            e.colorBorder
          )
        ),
        {
          [`&${e.componentCls}-dangerous`]: D(
            D(
              D(
                { color: e.colorError, borderColor: e.colorError },
                Bt(
                  { color: e.colorErrorHover, borderColor: e.colorErrorBorderHover },
                  { color: e.colorErrorActive, borderColor: e.colorErrorActive }
                )
              ),
              Bo(e.componentCls, e.colorError, e.colorError, e.colorTextDisabled, e.colorBorder)
            ),
            Sf(e)
          ),
        }
      ),
    gP = (e) =>
      D(
        D(
          D(
            D(D({}, fw(e)), {
              color: e.colorTextLightSolid,
              backgroundColor: e.colorPrimary,
              boxShadow: `0 ${e.controlOutlineWidth}px 0 ${e.controlOutline}`,
            }),
            Bt(
              { color: e.colorTextLightSolid, backgroundColor: e.colorPrimaryHover },
              { color: e.colorTextLightSolid, backgroundColor: e.colorPrimaryActive }
            )
          ),
          Bo(
            e.componentCls,
            e.colorPrimary,
            e.colorPrimary,
            e.colorTextDisabled,
            e.colorBorder,
            { color: e.colorPrimaryHover, borderColor: e.colorPrimaryHover },
            { color: e.colorPrimaryActive, borderColor: e.colorPrimaryActive }
          )
        ),
        {
          [`&${e.componentCls}-dangerous`]: D(
            D(
              D(
                {
                  backgroundColor: e.colorError,
                  boxShadow: `0 ${e.controlOutlineWidth}px 0 ${e.colorErrorOutline}`,
                },
                Bt({ backgroundColor: e.colorErrorHover }, { backgroundColor: e.colorErrorActive })
              ),
              Bo(
                e.componentCls,
                e.colorError,
                e.colorError,
                e.colorTextDisabled,
                e.colorBorder,
                { color: e.colorErrorHover, borderColor: e.colorErrorHover },
                { color: e.colorErrorActive, borderColor: e.colorErrorActive }
              )
            ),
            Sf(e)
          ),
        }
      ),
    mP = (e) => D(D({}, hw(e)), { borderStyle: 'dashed' }),
    yP = (e) =>
      D(
        D(
          D({ color: e.colorLink }, Bt({ color: e.colorLinkHover }, { color: e.colorLinkActive })),
          qo(e)
        ),
        {
          [`&${e.componentCls}-dangerous`]: D(
            D(
              { color: e.colorError },
              Bt({ color: e.colorErrorHover }, { color: e.colorErrorActive })
            ),
            qo(e)
          ),
        }
      ),
    bP = (e) =>
      D(
        D(
          D(
            {},
            Bt(
              { color: e.colorText, backgroundColor: e.colorBgTextHover },
              { color: e.colorText, backgroundColor: e.colorBgTextActive }
            )
          ),
          qo(e)
        ),
        {
          [`&${e.componentCls}-dangerous`]: D(
            D({ color: e.colorError }, qo(e)),
            Bt(
              { color: e.colorErrorHover, backgroundColor: e.colorErrorBg },
              { color: e.colorErrorHover, backgroundColor: e.colorErrorBg }
            )
          ),
        }
      ),
    _P = (e) => D(D({}, Md(e)), { [`&${e.componentCls}:hover`]: D({}, Md(e)) }),
    wP = (e) => {
      const { componentCls: t } = e
      return {
        [`${t}-default`]: hw(e),
        [`${t}-primary`]: gP(e),
        [`${t}-dashed`]: mP(e),
        [`${t}-link`]: yP(e),
        [`${t}-text`]: bP(e),
        [`${t}-disabled`]: _P(e),
      }
    },
    xf = function (e) {
      let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : ''
      const {
          componentCls: n,
          iconCls: r,
          controlHeight: o,
          fontSize: i,
          lineHeight: a,
          lineWidth: s,
          borderRadius: l,
          buttonPaddingHorizontal: u,
        } = e,
        c = Math.max(0, (o - i * a) / 2 - s),
        d = u - s,
        f = `${n}-icon-only`
      return [
        {
          [`${n}${t}`]: {
            fontSize: i,
            height: o,
            padding: `${c}px ${d}px`,
            borderRadius: l,
            [`&${f}`]: {
              width: o,
              paddingInlineStart: 0,
              paddingInlineEnd: 0,
              [`&${n}-round`]: { width: 'auto' },
              '> span': { transform: 'scale(1.143)' },
            },
            [`&${n}-loading`]: { opacity: e.opacityLoading, cursor: 'default' },
            [`${n}-loading-icon`]: {
              transition: `width ${e.motionDurationSlow} ${e.motionEaseInOut}, opacity ${e.motionDurationSlow} ${e.motionEaseInOut}`,
            },
            [`&:not(${f}) ${n}-loading-icon > ${r}`]: { marginInlineEnd: e.marginXS },
          },
        },
        { [`${n}${n}-circle${t}`]: pP(e) },
        { [`${n}${n}-round${t}`]: vP(e) },
      ]
    },
    SP = (e) => xf(e),
    xP = (e) => {
      const t = ot(e, {
        controlHeight: e.controlHeightSM,
        padding: e.paddingXS,
        buttonPaddingHorizontal: 8,
        borderRadius: e.borderRadiusSM,
      })
      return xf(t, `${e.componentCls}-sm`)
    },
    CP = (e) => {
      const t = ot(e, {
        controlHeight: e.controlHeightLG,
        fontSize: e.fontSizeLG,
        borderRadius: e.borderRadiusLG,
      })
      return xf(t, `${e.componentCls}-lg`)
    },
    EP = (e) => {
      const { componentCls: t } = e
      return { [t]: { [`&${t}-block`]: { width: '100%' } } }
    },
    $P = en('Button', (e) => {
      const { controlTmpOutline: t, paddingContentHorizontal: n } = e,
        r = ot(e, { colorOutlineDefault: t, buttonPaddingHorizontal: n })
      return [hP(r), xP(r), SP(r), CP(r), EP(r), wP(r), uP(r), iw(e, { focus: !1 }), fP(e)]
    }),
    TP = () => ({ prefixCls: String, size: { type: String } }),
    pw = _f(),
    Dd = te({
      compatConfig: { MODE: 3 },
      name: 'AButtonGroup',
      props: TP(),
      setup(e, t) {
        let { slots: n } = t
        const { prefixCls: r, direction: o } = Ge('btn-group', e),
          [, , i] = ox()
        pw.useProvide(Ko({ size: X(() => e.size) }))
        const a = X(() => {
          const { size: s } = e
          let l = ''
          switch (s) {
            case 'large':
              l = 'lg'
              break
            case 'small':
              l = 'sm'
              break
            case 'middle':
            case void 0:
              break
            default:
              df(!s, 'Button.Group', 'Invalid prop `size`.')
          }
          return {
            [`${r.value}`]: !0,
            [`${r.value}-${l}`]: l,
            [`${r.value}-rtl`]: o.value === 'rtl',
            [i.value]: !0,
          }
        })
        return () => {
          var s
          return F('div', { class: a.value }, [
            Xn((s = n.default) === null || s === void 0 ? void 0 : s.call(n)),
          ])
        }
      },
    }),
    Cp = /^[\u4e00-\u9fa5]{2}$/,
    Ep = Cp.test.bind(Cp)
  function so(e) {
    return e === 'text' || e === 'link'
  }
  const _t = te({
    compatConfig: { MODE: 3 },
    name: 'AButton',
    inheritAttrs: !1,
    __ANT_BUTTON: !0,
    props: tn(sP(), { type: 'default' }),
    slots: Object,
    setup(e, t) {
      let { slots: n, attrs: r, emit: o, expose: i } = t
      const { prefixCls: a, autoInsertSpaceInButton: s, direction: l, size: u } = Ge('btn', e),
        [c, d] = $P(a),
        f = pw.useInject(),
        h = of(),
        g = X(() => {
          var R
          return (R = e.disabled) !== null && R !== void 0 ? R : h.value
        }),
        m = ce(null),
        v = ce(void 0)
      let b = !1
      const y = ce(!1),
        p = ce(!1),
        _ = X(() => s.value !== !1),
        { compactSize: x, compactItemClassnames: S } = nw(a, l),
        w = X(() =>
          typeof e.loading == 'object' && e.loading.delay ? e.loading.delay || !0 : !!e.loading
        )
      me(
        w,
        (R) => {
          ;(clearTimeout(v.value),
            typeof w.value == 'number'
              ? (v.value = setTimeout(() => {
                  y.value = R
                }, w.value))
              : (y.value = R))
        },
        { immediate: !0 }
      )
      const T = X(() => {
          const { type: R, shape: N = 'default', ghost: j, block: V, danger: H } = e,
            G = a.value,
            Y = { large: 'lg', small: 'sm', middle: void 0 },
            Z = x.value || f?.size || u.value,
            ne = (Z && Y[Z]) || ''
          return [
            S.value,
            {
              [d.value]: !0,
              [`${G}`]: !0,
              [`${G}-${N}`]: N !== 'default' && N,
              [`${G}-${R}`]: R,
              [`${G}-${ne}`]: ne,
              [`${G}-loading`]: y.value,
              [`${G}-background-ghost`]: j && !so(R),
              [`${G}-two-chinese-chars`]: p.value && _.value,
              [`${G}-block`]: V,
              [`${G}-dangerous`]: !!H,
              [`${G}-rtl`]: l.value === 'rtl',
            },
          ]
        }),
        A = () => {
          const R = m.value
          if (!R || s.value === !1) return
          const N = R.textContent
          b && Ep(N) ? p.value || (p.value = !0) : p.value && (p.value = !1)
        },
        $ = (R) => {
          if (y.value || g.value) {
            R.preventDefault()
            return
          }
          o('click', R)
        },
        P = (R) => {
          o('mousedown', R)
        },
        E = (R, N) => {
          const j = N ? ' ' : ''
          if (R.type === ix) {
            let V = R.children.trim()
            return (Ep(V) && (V = V.split('').join(j)), F('span', null, [V]))
          }
          return R
        }
      return (
        Et(() => {
          df(
            !(e.ghost && so(e.type)),
            'Button',
            "`link` or `text` button can't be a `ghost` button."
          )
        }),
        Me(A),
        Zo(A),
        je(() => {
          v.value && clearTimeout(v.value)
        }),
        i({
          focus: () => {
            var R
            ;(R = m.value) === null || R === void 0 || R.focus()
          },
          blur: () => {
            var R
            ;(R = m.value) === null || R === void 0 || R.blur()
          },
        }),
        () => {
          var R, N
          const { icon: j = (R = n.icon) === null || R === void 0 ? void 0 : R.call(n) } = e,
            V = Xn((N = n.default) === null || N === void 0 ? void 0 : N.call(n))
          b = V.length === 1 && !j && !so(e.type)
          const { type: H, htmlType: G, href: Y, title: Z, target: ne } = e,
            B = y.value ? 'loading' : j,
            L = D(D({}, r), {
              title: Z,
              disabled: g.value,
              class: [T.value, r.class, { [`${a.value}-icon-only`]: V.length === 0 && !!B }],
              onClick: $,
              onMousedown: P,
            })
          g.value || delete L.disabled
          const k =
              j && !y.value
                ? j
                : F(lP, { existIcon: !!j, prefixCls: a.value, loading: !!y.value }, null),
            U = V.map((re) => E(re, b && _.value))
          if (Y !== void 0)
            return c(F('a', oe(oe({}, L), {}, { href: Y, target: ne, ref: m }), [k, U]))
          let J = F('button', oe(oe({}, L), {}, { ref: m, type: G }), [k, U])
          if (!so(H)) {
            const re = (function () {
              return J
            })()
            J = F(cw, { ref: 'wave', disabled: !!y.value }, { default: () => [re] })
          }
          return c(J)
        }
      )
    },
  })
  _t.Group = Dd
  _t.install = function (e) {
    return (e.component(_t.name, _t), e.component(Dd.name, Dd), e)
  }
  var OP = {
    icon: {
      tag: 'svg',
      attrs: { viewBox: '64 64 896 896', focusable: 'false' },
      children: [
        {
          tag: 'path',
          attrs: {
            d: 'M765.7 486.8L314.9 134.7A7.97 7.97 0 00302 141v77.3c0 4.9 2.3 9.6 6.1 12.6l360 281.1-360 281.1c-3.9 3-6.1 7.7-6.1 12.6V883c0 6.7 7.7 10.4 12.9 6.3l450.8-352.1a31.96 31.96 0 000-50.4z',
          },
        },
      ],
    },
    name: 'right',
    theme: 'outlined',
  }
  function $p(e) {
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
          PP(e, o, n[o])
        }))
    }
    return e
  }
  function PP(e, t, n) {
    return (
      t in e
        ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
        : (e[t] = n),
      e
    )
  }
  var Cf = function (t, n) {
    var r = $p({}, t, n.attrs)
    return F(kr, $p({}, r, { icon: OP }), null)
  }
  Cf.displayName = 'RightOutlined'
  Cf.inheritAttrs = !1
  function vw(e, t) {
    return e.classList ? e.classList.contains(t) : ` ${e.className} `.indexOf(` ${t} `) > -1
  }
  function Tp(e, t) {
    e.classList ? e.classList.add(t) : vw(e, t) || (e.className = `${e.className} ${t}`)
  }
  function Op(e, t) {
    if (e.classList) e.classList.remove(t)
    else if (vw(e, t)) {
      const n = e.className
      e.className = ` ${n} `.replace(` ${t} `, ' ')
    }
  }
  const IP = function () {
      let e =
          arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : 'ant-motion-collapse',
        t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0
      return {
        name: e,
        appear: t,
        css: !0,
        onBeforeEnter: (n) => {
          ;((n.style.height = '0px'), (n.style.opacity = '0'), Tp(n, e))
        },
        onEnter: (n) => {
          Ne(() => {
            ;((n.style.height = `${n.scrollHeight}px`), (n.style.opacity = '1'))
          })
        },
        onAfterEnter: (n) => {
          n && (Op(n, e), (n.style.height = null), (n.style.opacity = null))
        },
        onBeforeLeave: (n) => {
          ;(Tp(n, e), (n.style.height = `${n.offsetHeight}px`), (n.style.opacity = null))
        },
        onLeave: (n) => {
          setTimeout(() => {
            ;((n.style.height = '0px'), (n.style.opacity = '0'))
          })
        },
        onAfterLeave: (n) => {
          n && (Op(n, e), n.style && ((n.style.height = null), (n.style.opacity = null)))
        },
      }
    },
    AP = (e) => ({
      '&::-moz-placeholder': { opacity: 1 },
      '&::placeholder': { color: e, userSelect: 'none' },
      '&:placeholder-shown': { textOverflow: 'ellipsis' },
    }),
    Ef = (e) => ({ borderColor: e.inputBorderHoverColor, borderInlineEndWidth: e.lineWidth }),
    Bd = (e) => ({
      borderColor: e.inputBorderHoverColor,
      boxShadow: `0 0 0 ${e.controlOutlineWidth}px ${e.controlOutline}`,
      borderInlineEndWidth: e.lineWidth,
      outline: 0,
    }),
    NP = (e) => ({
      color: e.colorTextDisabled,
      backgroundColor: e.colorBgContainerDisabled,
      borderColor: e.colorBorder,
      boxShadow: 'none',
      cursor: 'not-allowed',
      opacity: 1,
      '&:hover': D({}, Ef(ot(e, { inputBorderHoverColor: e.colorBorder }))),
    }),
    gw = (e) => {
      const {
        inputPaddingVerticalLG: t,
        fontSizeLG: n,
        lineHeightLG: r,
        borderRadiusLG: o,
        inputPaddingHorizontalLG: i,
      } = e
      return { padding: `${t}px ${i}px`, fontSize: n, lineHeight: r, borderRadius: o }
    },
    mw = (e) => ({
      padding: `${e.inputPaddingVerticalSM}px ${e.controlPaddingHorizontalSM - 1}px`,
      borderRadius: e.borderRadiusSM,
    }),
    yw = (e, t) => {
      const {
        componentCls: n,
        colorError: r,
        colorWarning: o,
        colorErrorOutline: i,
        colorWarningOutline: a,
        colorErrorBorderHover: s,
        colorWarningBorderHover: l,
      } = e
      return {
        [`&-status-error:not(${t}-disabled):not(${t}-borderless)${t}`]: {
          borderColor: r,
          '&:hover': { borderColor: s },
          '&:focus, &-focused': D(
            {},
            Bd(ot(e, { inputBorderActiveColor: r, inputBorderHoverColor: r, controlOutline: i }))
          ),
          [`${n}-prefix`]: { color: r },
        },
        [`&-status-warning:not(${t}-disabled):not(${t}-borderless)${t}`]: {
          borderColor: o,
          '&:hover': { borderColor: l },
          '&:focus, &-focused': D(
            {},
            Bd(ot(e, { inputBorderActiveColor: o, inputBorderHoverColor: o, controlOutline: a }))
          ),
          [`${n}-prefix`]: { color: o },
        },
      }
    },
    bw = (e) =>
      D(
        D(
          {
            position: 'relative',
            display: 'inline-block',
            width: '100%',
            minWidth: 0,
            padding: `${e.inputPaddingVertical}px ${e.inputPaddingHorizontal}px`,
            color: e.colorText,
            fontSize: e.fontSize,
            lineHeight: e.lineHeight,
            backgroundColor: e.colorBgContainer,
            backgroundImage: 'none',
            borderWidth: e.lineWidth,
            borderStyle: e.lineType,
            borderColor: e.colorBorder,
            borderRadius: e.borderRadius,
            transition: `all ${e.motionDurationMid}`,
          },
          AP(e.colorTextPlaceholder)
        ),
        {
          '&:hover': D({}, Ef(e)),
          '&:focus, &-focused': D({}, Bd(e)),
          '&-disabled, &[disabled]': D({}, NP(e)),
          '&-borderless': {
            '&, &:hover, &:focus, &-focused, &-disabled, &[disabled]': {
              backgroundColor: 'transparent',
              border: 'none',
              boxShadow: 'none',
            },
          },
          'textarea&': {
            maxWidth: '100%',
            height: 'auto',
            minHeight: e.controlHeight,
            lineHeight: e.lineHeight,
            verticalAlign: 'bottom',
            transition: `all ${e.motionDurationSlow}, height 0s`,
            resize: 'vertical',
          },
          '&-lg': D({}, gw(e)),
          '&-sm': D({}, mw(e)),
          '&-rtl': { direction: 'rtl' },
          '&-textarea-rtl': { direction: 'rtl' },
        }
      ),
    RP = (e) => {
      const { componentCls: t, antCls: n } = e
      return {
        position: 'relative',
        display: 'table',
        width: '100%',
        borderCollapse: 'separate',
        borderSpacing: 0,
        "&[class*='col-']": {
          paddingInlineEnd: e.paddingXS,
          '&:last-child': { paddingInlineEnd: 0 },
        },
        [`&-lg ${t}, &-lg > ${t}-group-addon`]: D({}, gw(e)),
        [`&-sm ${t}, &-sm > ${t}-group-addon`]: D({}, mw(e)),
        [`> ${t}`]: {
          display: 'table-cell',
          '&:not(:first-child):not(:last-child)': { borderRadius: 0 },
        },
        [`${t}-group`]: {
          '&-addon, &-wrap': {
            display: 'table-cell',
            width: 1,
            whiteSpace: 'nowrap',
            verticalAlign: 'middle',
            '&:not(:first-child):not(:last-child)': { borderRadius: 0 },
          },
          '&-wrap > *': { display: 'block !important' },
          '&-addon': {
            position: 'relative',
            padding: `0 ${e.inputPaddingHorizontal}px`,
            color: e.colorText,
            fontWeight: 'normal',
            fontSize: e.fontSize,
            textAlign: 'center',
            backgroundColor: e.colorFillAlter,
            border: `${e.lineWidth}px ${e.lineType} ${e.colorBorder}`,
            borderRadius: e.borderRadius,
            transition: `all ${e.motionDurationSlow}`,
            lineHeight: 1,
            [`${n}-select`]: {
              margin: `-${e.inputPaddingVertical + 1}px -${e.inputPaddingHorizontal}px`,
              [`&${n}-select-single:not(${n}-select-customize-input)`]: {
                [`${n}-select-selector`]: {
                  backgroundColor: 'inherit',
                  border: `${e.lineWidth}px ${e.lineType} transparent`,
                  boxShadow: 'none',
                },
              },
              '&-open, &-focused': { [`${n}-select-selector`]: { color: e.colorPrimary } },
            },
            [`${n}-cascader-picker`]: {
              margin: `-9px -${e.inputPaddingHorizontal}px`,
              backgroundColor: 'transparent',
              [`${n}-cascader-input`]: { textAlign: 'start', border: 0, boxShadow: 'none' },
            },
          },
          '&-addon:first-child': { borderInlineEnd: 0 },
          '&-addon:last-child': { borderInlineStart: 0 },
        },
        [`${t}`]: {
          float: 'inline-start',
          width: '100%',
          marginBottom: 0,
          textAlign: 'inherit',
          '&:focus': { zIndex: 1, borderInlineEndWidth: 1 },
          '&:hover': {
            zIndex: 1,
            borderInlineEndWidth: 1,
            [`${t}-search-with-button &`]: { zIndex: 0 },
          },
        },
        [`> ${t}:first-child, ${t}-group-addon:first-child`]: {
          borderStartEndRadius: 0,
          borderEndEndRadius: 0,
          [`${n}-select ${n}-select-selector`]: { borderStartEndRadius: 0, borderEndEndRadius: 0 },
        },
        [`> ${t}-affix-wrapper`]: {
          [`&:not(:first-child) ${t}`]: { borderStartStartRadius: 0, borderEndStartRadius: 0 },
          [`&:not(:last-child) ${t}`]: { borderStartEndRadius: 0, borderEndEndRadius: 0 },
        },
        [`> ${t}:last-child, ${t}-group-addon:last-child`]: {
          borderStartStartRadius: 0,
          borderEndStartRadius: 0,
          [`${n}-select ${n}-select-selector`]: {
            borderStartStartRadius: 0,
            borderEndStartRadius: 0,
          },
        },
        [`${t}-affix-wrapper`]: {
          '&:not(:last-child)': {
            borderStartEndRadius: 0,
            borderEndEndRadius: 0,
            [`${t}-search &`]: {
              borderStartStartRadius: e.borderRadius,
              borderEndStartRadius: e.borderRadius,
            },
          },
          [`&:not(:first-child), ${t}-search &:not(:first-child)`]: {
            borderStartStartRadius: 0,
            borderEndStartRadius: 0,
          },
        },
        [`&${t}-group-compact`]: D(D({ display: 'block' }, l_()), {
          [`${t}-group-addon, ${t}-group-wrap, > ${t}`]: {
            '&:not(:first-child):not(:last-child)': {
              borderInlineEndWidth: e.lineWidth,
              '&:hover': { zIndex: 1 },
              '&:focus': { zIndex: 1 },
            },
          },
          '& > *': {
            display: 'inline-block',
            float: 'none',
            verticalAlign: 'top',
            borderRadius: 0,
          },
          [`& > ${t}-affix-wrapper`]: { display: 'inline-flex' },
          [`& > ${n}-picker-range`]: { display: 'inline-flex' },
          '& > *:not(:last-child)': {
            marginInlineEnd: -e.lineWidth,
            borderInlineEndWidth: e.lineWidth,
          },
          [`${t}`]: { float: 'none' },
          [`& > ${n}-select > ${n}-select-selector,
      & > ${n}-select-auto-complete ${t},
      & > ${n}-cascader-picker ${t},
      & > ${t}-group-wrapper ${t}`]: {
            borderInlineEndWidth: e.lineWidth,
            borderRadius: 0,
            '&:hover': { zIndex: 1 },
            '&:focus': { zIndex: 1 },
          },
          [`& > ${n}-select-focused`]: { zIndex: 1 },
          [`& > ${n}-select > ${n}-select-arrow`]: { zIndex: 1 },
          [`& > *:first-child,
      & > ${n}-select:first-child > ${n}-select-selector,
      & > ${n}-select-auto-complete:first-child ${t},
      & > ${n}-cascader-picker:first-child ${t}`]: {
            borderStartStartRadius: e.borderRadius,
            borderEndStartRadius: e.borderRadius,
          },
          [`& > *:last-child,
      & > ${n}-select:last-child > ${n}-select-selector,
      & > ${n}-cascader-picker:last-child ${t},
      & > ${n}-cascader-picker-focused:last-child ${t}`]: {
            borderInlineEndWidth: e.lineWidth,
            borderStartEndRadius: e.borderRadius,
            borderEndEndRadius: e.borderRadius,
          },
          [`& > ${n}-select-auto-complete ${t}`]: { verticalAlign: 'top' },
          [`${t}-group-wrapper + ${t}-group-wrapper`]: {
            marginInlineStart: -e.lineWidth,
            [`${t}-affix-wrapper`]: { borderRadius: 0 },
          },
          [`${t}-group-wrapper:not(:last-child)`]: {
            [`&${t}-search > ${t}-group`]: {
              [`& > ${t}-group-addon > ${t}-search-button`]: { borderRadius: 0 },
              [`& > ${t}`]: {
                borderStartStartRadius: e.borderRadius,
                borderStartEndRadius: 0,
                borderEndEndRadius: 0,
                borderEndStartRadius: e.borderRadius,
              },
            },
          },
        }),
        [`&&-sm ${n}-btn`]: {
          fontSize: e.fontSizeSM,
          height: e.controlHeightSM,
          lineHeight: 'normal',
        },
        [`&&-lg ${n}-btn`]: {
          fontSize: e.fontSizeLG,
          height: e.controlHeightLG,
          lineHeight: 'normal',
        },
        [`&&-lg ${n}-select-single ${n}-select-selector`]: {
          height: `${e.controlHeightLG}px`,
          [`${n}-select-selection-item, ${n}-select-selection-placeholder`]: {
            lineHeight: `${e.controlHeightLG - 2}px`,
          },
          [`${n}-select-selection-search-input`]: { height: `${e.controlHeightLG}px` },
        },
        [`&&-sm ${n}-select-single ${n}-select-selector`]: {
          height: `${e.controlHeightSM}px`,
          [`${n}-select-selection-item, ${n}-select-selection-placeholder`]: {
            lineHeight: `${e.controlHeightSM - 2}px`,
          },
          [`${n}-select-selection-search-input`]: { height: `${e.controlHeightSM}px` },
        },
      }
    },
    MP = (e) => {
      const { componentCls: t, controlHeightSM: n, lineWidth: r } = e,
        i = (n - r * 2 - 16) / 2
      return {
        [t]: D(D(D(D({}, Kn(e)), bw(e)), yw(e, t)), {
          '&[type="color"]': {
            height: e.controlHeight,
            [`&${t}-lg`]: { height: e.controlHeightLG },
            [`&${t}-sm`]: { height: n, paddingTop: i, paddingBottom: i },
          },
        }),
      }
    },
    DP = (e) => {
      const { componentCls: t } = e
      return {
        [`${t}-clear-icon`]: {
          margin: 0,
          color: e.colorTextQuaternary,
          fontSize: e.fontSizeIcon,
          verticalAlign: -1,
          cursor: 'pointer',
          transition: `color ${e.motionDurationSlow}`,
          '&:hover': { color: e.colorTextTertiary },
          '&:active': { color: e.colorText },
          '&-hidden': { visibility: 'hidden' },
          '&-has-suffix': { margin: `0 ${e.inputAffixPadding}px` },
        },
        '&-textarea-with-clear-btn': {
          padding: '0 !important',
          border: '0 !important',
          [`${t}-clear-icon`]: {
            position: 'absolute',
            insetBlockStart: e.paddingXS,
            insetInlineEnd: e.paddingXS,
            zIndex: 1,
          },
        },
      }
    },
    BP = (e) => {
      const {
        componentCls: t,
        inputAffixPadding: n,
        colorTextDescription: r,
        motionDurationSlow: o,
        colorIcon: i,
        colorIconHover: a,
        iconCls: s,
      } = e
      return {
        [`${t}-affix-wrapper`]: D(
          D(
            D(
              D(D({}, bw(e)), {
                display: 'inline-flex',
                [`&:not(${t}-affix-wrapper-disabled):hover`]: D(D({}, Ef(e)), {
                  zIndex: 1,
                  [`${t}-search-with-button &`]: { zIndex: 0 },
                }),
                '&-focused, &:focus': { zIndex: 1 },
                '&-disabled': { [`${t}[disabled]`]: { background: 'transparent' } },
                [`> input${t}`]: {
                  padding: 0,
                  fontSize: 'inherit',
                  border: 'none',
                  borderRadius: 0,
                  outline: 'none',
                  '&:focus': { boxShadow: 'none !important' },
                },
                '&::before': { width: 0, visibility: 'hidden', content: '"\\a0"' },
                [`${t}`]: {
                  '&-prefix, &-suffix': {
                    display: 'flex',
                    flex: 'none',
                    alignItems: 'center',
                    '> *:not(:last-child)': { marginInlineEnd: e.paddingXS },
                  },
                  '&-show-count-suffix': { color: r },
                  '&-show-count-has-suffix': { marginInlineEnd: e.paddingXXS },
                  '&-prefix': { marginInlineEnd: n },
                  '&-suffix': { marginInlineStart: n },
                },
              }),
              DP(e)
            ),
            {
              [`${s}${t}-password-icon`]: {
                color: i,
                cursor: 'pointer',
                transition: `all ${o}`,
                '&:hover': { color: a },
              },
            }
          ),
          yw(e, `${t}-affix-wrapper`)
        ),
      }
    },
    qP = (e) => {
      const {
        componentCls: t,
        colorError: n,
        colorSuccess: r,
        borderRadiusLG: o,
        borderRadiusSM: i,
      } = e
      return {
        [`${t}-group`]: D(D(D({}, Kn(e)), RP(e)), {
          '&-rtl': { direction: 'rtl' },
          '&-wrapper': {
            display: 'inline-block',
            width: '100%',
            textAlign: 'start',
            verticalAlign: 'top',
            '&-rtl': { direction: 'rtl' },
            '&-lg': { [`${t}-group-addon`]: { borderRadius: o } },
            '&-sm': { [`${t}-group-addon`]: { borderRadius: i } },
            '&-status-error': { [`${t}-group-addon`]: { color: n, borderColor: n } },
            '&-status-warning': { [`${t}-group-addon:last-child`]: { color: r, borderColor: r } },
          },
        }),
      }
    },
    zP = (e) => {
      const { componentCls: t, antCls: n } = e,
        r = `${t}-search`
      return {
        [r]: {
          [`${t}`]: {
            '&:hover, &:focus': {
              borderColor: e.colorPrimaryHover,
              [`+ ${t}-group-addon ${r}-button:not(${n}-btn-primary)`]: {
                borderInlineStartColor: e.colorPrimaryHover,
              },
            },
          },
          [`${t}-affix-wrapper`]: { borderRadius: 0 },
          [`${t}-lg`]: { lineHeight: e.lineHeightLG - 2e-4 },
          [`> ${t}-group`]: {
            [`> ${t}-group-addon:last-child`]: {
              insetInlineStart: -1,
              padding: 0,
              border: 0,
              [`${r}-button`]: {
                paddingTop: 0,
                paddingBottom: 0,
                borderStartStartRadius: 0,
                borderStartEndRadius: e.borderRadius,
                borderEndEndRadius: e.borderRadius,
                borderEndStartRadius: 0,
              },
              [`${r}-button:not(${n}-btn-primary)`]: {
                color: e.colorTextDescription,
                '&:hover': { color: e.colorPrimaryHover },
                '&:active': { color: e.colorPrimaryActive },
                [`&${n}-btn-loading::before`]: {
                  insetInlineStart: 0,
                  insetInlineEnd: 0,
                  insetBlockStart: 0,
                  insetBlockEnd: 0,
                },
              },
            },
          },
          [`${r}-button`]: { height: e.controlHeight, '&:hover, &:focus': { zIndex: 1 } },
          [`&-large ${r}-button`]: { height: e.controlHeightLG },
          [`&-small ${r}-button`]: { height: e.controlHeightSM },
          '&-rtl': { direction: 'rtl' },
          [`&${t}-compact-item`]: {
            [`&:not(${t}-compact-last-item)`]: {
              [`${t}-group-addon`]: {
                [`${t}-search-button`]: { marginInlineEnd: -e.lineWidth, borderRadius: 0 },
              },
            },
            [`&:not(${t}-compact-first-item)`]: {
              [`${t},${t}-affix-wrapper`]: { borderRadius: 0 },
            },
            [`> ${t}-group-addon ${t}-search-button,
        > ${t},
        ${t}-affix-wrapper`]: { '&:hover,&:focus,&:active': { zIndex: 2 } },
            [`> ${t}-affix-wrapper-focused`]: { zIndex: 2 },
          },
        },
      }
    }
  function LP(e) {
    return ot(e, {
      inputAffixPadding: e.paddingXXS,
      inputPaddingVertical: Math.max(
        Math.round(((e.controlHeight - e.fontSize * e.lineHeight) / 2) * 10) / 10 - e.lineWidth,
        3
      ),
      inputPaddingVerticalLG:
        Math.ceil(((e.controlHeightLG - e.fontSizeLG * e.lineHeightLG) / 2) * 10) / 10 -
        e.lineWidth,
      inputPaddingVerticalSM: Math.max(
        Math.round(((e.controlHeightSM - e.fontSize * e.lineHeight) / 2) * 10) / 10 - e.lineWidth,
        0
      ),
      inputPaddingHorizontal: e.paddingSM - e.lineWidth,
      inputPaddingHorizontalSM: e.paddingXS - e.lineWidth,
      inputPaddingHorizontalLG: e.controlPaddingHorizontal - e.lineWidth,
      inputBorderHoverColor: e.colorPrimaryHover,
      inputBorderActiveColor: e.colorPrimaryHover,
    })
  }
  const FP = (e) => {
      const { componentCls: t, inputPaddingHorizontal: n, paddingLG: r } = e,
        o = `${t}-textarea`
      return {
        [o]: {
          position: 'relative',
          [`${o}-suffix`]: {
            position: 'absolute',
            top: 0,
            insetInlineEnd: n,
            bottom: 0,
            zIndex: 1,
            display: 'inline-flex',
            alignItems: 'center',
            margin: 'auto',
          },
          '&-status-error,\n        &-status-warning,\n        &-status-success,\n        &-status-validating':
            { [`&${o}-has-feedback`]: { [`${t}`]: { paddingInlineEnd: r } } },
          '&-show-count': {
            [`> ${t}`]: { height: '100%' },
            '&::after': {
              color: e.colorTextDescription,
              whiteSpace: 'nowrap',
              content: 'attr(data-count)',
              pointerEvents: 'none',
              float: 'right',
            },
          },
          '&-rtl': { '&::after': { float: 'left' } },
        },
      }
    },
    $f = en('Input', (e) => {
      const t = LP(e)
      return [MP(t), FP(t), BP(t), qP(t), zP(t), iw(t)]
    }),
    kP = () => ({
      prefixCls: String,
      activeKey: Cd([Array, Number, String]),
      defaultActiveKey: Cd([Array, Number, String]),
      accordion: Xe(),
      destroyInactivePanel: Xe(),
      bordered: Xe(),
      expandIcon: vr(),
      openAnimation: Q.object,
      expandIconPosition: Oo(),
      collapsible: Oo(),
      ghost: Xe(),
      onChange: vr(),
      'onUpdate:activeKey': vr(),
    }),
    _w = () => ({
      openAnimation: Q.object,
      prefixCls: String,
      header: Q.any,
      headerClass: String,
      showArrow: Xe(),
      isActive: Xe(),
      destroyInactivePanel: Xe(),
      disabled: Xe(),
      accordion: Xe(),
      forceRender: Xe(),
      expandIcon: vr(),
      extra: Q.any,
      panelKey: Cd(),
      collapsible: Oo(),
      role: String,
      onItemClick: vr(),
    }),
    HP = (e) => {
      const {
          componentCls: t,
          collapseContentBg: n,
          padding: r,
          collapseContentPaddingHorizontal: o,
          collapseHeaderBg: i,
          collapseHeaderPadding: a,
          collapsePanelBorderRadius: s,
          lineWidth: l,
          lineType: u,
          colorBorder: c,
          colorText: d,
          colorTextHeading: f,
          colorTextDisabled: h,
          fontSize: g,
          lineHeight: m,
          marginSM: v,
          paddingSM: b,
          motionDurationSlow: y,
          fontSizeIcon: p,
        } = e,
        _ = `${l}px ${u} ${c}`
      return {
        [t]: D(D({}, Kn(e)), {
          backgroundColor: i,
          border: _,
          borderBottom: 0,
          borderRadius: `${s}px`,
          '&-rtl': { direction: 'rtl' },
          [`& > ${t}-item`]: {
            borderBottom: _,
            '&:last-child': {
              [`
            &,
            & > ${t}-header`]: { borderRadius: `0 0 ${s}px ${s}px` },
            },
            [`> ${t}-header`]: {
              position: 'relative',
              display: 'flex',
              flexWrap: 'nowrap',
              alignItems: 'flex-start',
              padding: a,
              color: f,
              lineHeight: m,
              cursor: 'pointer',
              transition: `all ${y}, visibility 0s`,
              [`> ${t}-header-text`]: { flex: 'auto' },
              '&:focus': { outline: 'none' },
              [`${t}-expand-icon`]: {
                height: g * m,
                display: 'flex',
                alignItems: 'center',
                paddingInlineEnd: v,
              },
              [`${t}-arrow`]: D(D({}, ax()), {
                fontSize: p,
                svg: { transition: `transform ${y}` },
              }),
              [`${t}-header-text`]: { marginInlineEnd: 'auto' },
            },
            [`${t}-header-collapsible-only`]: {
              cursor: 'default',
              [`${t}-header-text`]: { flex: 'none', cursor: 'pointer' },
              [`${t}-expand-icon`]: { cursor: 'pointer' },
            },
            [`${t}-icon-collapsible-only`]: {
              cursor: 'default',
              [`${t}-expand-icon`]: { cursor: 'pointer' },
            },
            [`&${t}-no-arrow`]: { [`> ${t}-header`]: { paddingInlineStart: b } },
          },
          [`${t}-content`]: {
            color: d,
            backgroundColor: n,
            borderTop: _,
            [`& > ${t}-content-box`]: { padding: `${r}px ${o}px` },
            '&-hidden': { display: 'none' },
          },
          [`${t}-item:last-child`]: { [`> ${t}-content`]: { borderRadius: `0 0 ${s}px ${s}px` } },
          [`& ${t}-item-disabled > ${t}-header`]: {
            '\n          &,\n          & > .arrow\n        ': { color: h, cursor: 'not-allowed' },
          },
          [`&${t}-icon-position-end`]: {
            [`& > ${t}-item`]: {
              [`> ${t}-header`]: {
                [`${t}-expand-icon`]: { order: 1, paddingInlineEnd: 0, paddingInlineStart: v },
              },
            },
          },
        }),
      }
    },
    jP = (e) => {
      const { componentCls: t } = e,
        n = `> ${t}-item > ${t}-header ${t}-arrow svg`
      return { [`${t}-rtl`]: { [n]: { transform: 'rotate(180deg)' } } }
    },
    VP = (e) => {
      const { componentCls: t, collapseHeaderBg: n, paddingXXS: r, colorBorder: o } = e
      return {
        [`${t}-borderless`]: {
          backgroundColor: n,
          border: 0,
          [`> ${t}-item`]: { borderBottom: `1px solid ${o}` },
          [`
        > ${t}-item:last-child,
        > ${t}-item:last-child ${t}-header
      `]: { borderRadius: 0 },
          [`> ${t}-item:last-child`]: { borderBottom: 0 },
          [`> ${t}-item > ${t}-content`]: { backgroundColor: 'transparent', borderTop: 0 },
          [`> ${t}-item > ${t}-content > ${t}-content-box`]: { paddingTop: r },
        },
      }
    },
    GP = (e) => {
      const { componentCls: t, paddingSM: n } = e
      return {
        [`${t}-ghost`]: {
          backgroundColor: 'transparent',
          border: 0,
          [`> ${t}-item`]: {
            borderBottom: 0,
            [`> ${t}-content`]: {
              backgroundColor: 'transparent',
              border: 0,
              [`> ${t}-content-box`]: { paddingBlock: n },
            },
          },
        },
      }
    },
    WP = en('Collapse', (e) => {
      const t = ot(e, {
        collapseContentBg: e.colorBgContainer,
        collapseHeaderBg: e.colorFillAlter,
        collapseHeaderPadding: `${e.paddingSM}px ${e.padding}px`,
        collapsePanelBorderRadius: e.borderRadiusLG,
        collapseContentPaddingHorizontal: 16,
      })
      return [HP(t), VP(t), GP(t), jP(t), AO(t)]
    })
  function Pp(e) {
    let t = e
    if (!Array.isArray(t)) {
      const n = typeof t
      t = n === 'number' || n === 'string' ? [t] : []
    }
    return t.map((n) => String(n))
  }
  const Dn = te({
      compatConfig: { MODE: 3 },
      name: 'ACollapse',
      inheritAttrs: !1,
      props: tn(kP(), {
        accordion: !1,
        destroyInactivePanel: !1,
        bordered: !0,
        expandIconPosition: 'start',
      }),
      slots: Object,
      setup(e, t) {
        let { attrs: n, slots: r, emit: o } = t
        const i = de(Pp(sw([e.activeKey, e.defaultActiveKey])))
        me(
          () => e.activeKey,
          () => {
            i.value = Pp(e.activeKey)
          },
          { deep: !0 }
        )
        const { prefixCls: a, direction: s, rootPrefixCls: l } = Ge('collapse', e),
          [u, c] = WP(a),
          d = X(() => {
            const { expandIconPosition: b } = e
            return b !== void 0 ? b : s.value === 'rtl' ? 'end' : 'start'
          }),
          f = (b) => {
            const { expandIcon: y = r.expandIcon } = e,
              p = y ? y(b) : F(Cf, { rotate: b.isActive ? 90 : void 0 }, null)
            return F(
              'div',
              {
                class: [`${a.value}-expand-icon`, c.value],
                onClick: () => ['header', 'icon'].includes(e.collapsible) && g(b.panelKey),
              },
              [rf(Array.isArray(y) ? p[0] : p) ? Ke(p, { class: `${a.value}-arrow` }, !1) : p]
            )
          },
          h = (b) => {
            e.activeKey === void 0 && (i.value = b)
            const y = e.accordion ? b[0] : b
            ;(o('update:activeKey', y), o('change', y))
          },
          g = (b) => {
            let y = i.value
            if (e.accordion) y = y[0] === b ? [] : [b]
            else {
              y = [...y]
              const p = y.indexOf(b)
              p > -1 ? y.splice(p, 1) : y.push(b)
            }
            h(y)
          },
          m = (b, y) => {
            var p, _, x
            if (lx(b)) return
            const S = i.value,
              { accordion: w, destroyInactivePanel: T, collapsible: A, openAnimation: $ } = e,
              P = $ || IP(`${l.value}-motion-collapse`),
              E = String((p = b.key) !== null && p !== void 0 ? p : y),
              {
                header: z = (x = (_ = b.children) === null || _ === void 0 ? void 0 : _.header) ===
                  null || x === void 0
                  ? void 0
                  : x.call(_),
                headerClass: C,
                collapsible: R,
                disabled: N,
              } = b.props || {}
            let j = !1
            w ? (j = S[0] === E) : (j = S.indexOf(E) > -1)
            let V = R ?? A
            ;(N || N === '') && (V = 'disabled')
            const H = {
              key: E,
              panelKey: E,
              header: z,
              headerClass: C,
              isActive: j,
              prefixCls: a.value,
              destroyInactivePanel: T,
              openAnimation: P,
              accordion: w,
              onItemClick: V === 'disabled' ? null : g,
              expandIcon: f,
              collapsible: V,
            }
            return Ke(b, H)
          },
          v = () => {
            var b
            return Xn((b = r.default) === null || b === void 0 ? void 0 : b.call(r)).map(m)
          }
        return () => {
          const { accordion: b, bordered: y, ghost: p } = e,
            _ = xe(
              a.value,
              {
                [`${a.value}-borderless`]: !y,
                [`${a.value}-icon-position-${d.value}`]: !0,
                [`${a.value}-rtl`]: s.value === 'rtl',
                [`${a.value}-ghost`]: !!p,
                [n.class]: !!n.class,
              },
              c.value
            )
          return u(
            F(
              'div',
              oe(oe({ class: _ }, sx(n)), {}, { style: n.style, role: b ? 'tablist' : null }),
              [v()]
            )
          )
        }
      },
    }),
    UP = te({
      compatConfig: { MODE: 3 },
      name: 'PanelContent',
      props: _w(),
      setup(e, t) {
        let { slots: n } = t
        const r = ce(!1)
        return (
          Et(() => {
            ;(e.isActive || e.forceRender) && (r.value = !0)
          }),
          () => {
            var o
            if (!r.value) return null
            const { prefixCls: i, isActive: a, role: s } = e
            return F(
              'div',
              {
                class: xe(`${i}-content`, {
                  [`${i}-content-active`]: a,
                  [`${i}-content-inactive`]: !a,
                }),
                role: s,
              },
              [
                F('div', { class: `${i}-content-box` }, [
                  (o = n.default) === null || o === void 0 ? void 0 : o.call(n),
                ]),
              ]
            )
          }
        )
      },
    }),
    qd = te({
      compatConfig: { MODE: 3 },
      name: 'ACollapsePanel',
      inheritAttrs: !1,
      props: tn(_w(), {
        showArrow: !0,
        isActive: !1,
        onItemClick() {},
        headerClass: '',
        forceRender: !1,
      }),
      slots: Object,
      setup(e, t) {
        let { slots: n, emit: r, attrs: o } = t
        df(
          e.disabled === void 0,
          'Collapse.Panel',
          '`disabled` is deprecated. Please use `collapsible="disabled"` instead.'
        )
        const { prefixCls: i } = Ge('collapse', e),
          a = () => {
            r('itemClick', e.panelKey)
          },
          s = (l) => {
            ;(l.key === 'Enter' || l.keyCode === 13 || l.which === 13) && a()
          }
        return () => {
          var l, u
          const {
              header: c = (l = n.header) === null || l === void 0 ? void 0 : l.call(n),
              headerClass: d,
              isActive: f,
              showArrow: h,
              destroyInactivePanel: g,
              accordion: m,
              forceRender: v,
              openAnimation: b,
              expandIcon: y = n.expandIcon,
              extra: p = (u = n.extra) === null || u === void 0 ? void 0 : u.call(n),
              collapsible: _,
            } = e,
            x = _ === 'disabled',
            S = i.value,
            w = xe(`${S}-header`, {
              [d]: d,
              [`${S}-header-collapsible-only`]: _ === 'header',
              [`${S}-icon-collapsible-only`]: _ === 'icon',
            }),
            T = xe({
              [`${S}-item`]: !0,
              [`${S}-item-active`]: f,
              [`${S}-item-disabled`]: x,
              [`${S}-no-arrow`]: !h,
              [`${o.class}`]: !!o.class,
            })
          let A = F('i', { class: 'arrow' }, null)
          h && typeof y == 'function' && (A = y(e))
          const $ = Lr(
              F(
                UP,
                { prefixCls: S, isActive: f, forceRender: v, role: m ? 'tabpanel' : null },
                { default: n.default }
              ),
              [[Qo, f]]
            ),
            P = D({ appear: !1, css: !1 }, b)
          return F('div', oe(oe({}, o), {}, { class: T }), [
            F(
              'div',
              {
                class: w,
                onClick: () => !['header', 'icon'].includes(_) && a(),
                role: m ? 'tab' : 'button',
                tabindex: x ? -1 : 0,
                'aria-expanded': f,
                onKeypress: s,
              },
              [
                h && A,
                F('span', { onClick: () => _ === 'header' && a(), class: `${S}-header-text` }, [c]),
                p && F('div', { class: `${S}-extra` }, [p]),
              ]
            ),
            F(Qt, P, { default: () => [!g || f ? $ : null] }),
          ])
        }
      },
    })
  Dn.Panel = qd
  Dn.install = function (e) {
    return (e.component(Dn.name, Dn), e.component(qd.name, qd), e)
  }
  const YP = () => Cr() && window.document.documentElement,
    lo = (e, t, n) => {
      const r = ux(n)
      return {
        [`${e.componentCls}-${t}`]: {
          color: e[`color${n}`],
          background: e[`color${r}Bg`],
          borderColor: e[`color${r}Border`],
          [`&${e.componentCls}-borderless`]: { borderColor: 'transparent' },
        },
      }
    },
    XP = (e) =>
      x_(e, (t, n) => {
        let { textColor: r, lightBorderColor: o, lightColor: i, darkColor: a } = n
        return {
          [`${e.componentCls}-${t}`]: {
            color: r,
            background: i,
            borderColor: o,
            '&-inverse': { color: e.colorTextLightSolid, background: a, borderColor: a },
            [`&${e.componentCls}-borderless`]: { borderColor: 'transparent' },
          },
        }
      }),
    KP = (e) => {
      const { paddingXXS: t, lineWidth: n, tagPaddingHorizontal: r, componentCls: o } = e,
        i = r - n,
        a = t - n
      return {
        [o]: D(D({}, Kn(e)), {
          display: 'inline-block',
          height: 'auto',
          marginInlineEnd: e.marginXS,
          paddingInline: i,
          fontSize: e.tagFontSize,
          lineHeight: `${e.tagLineHeight}px`,
          whiteSpace: 'nowrap',
          background: e.tagDefaultBg,
          border: `${e.lineWidth}px ${e.lineType} ${e.colorBorder}`,
          borderRadius: e.borderRadiusSM,
          opacity: 1,
          transition: `all ${e.motionDurationMid}`,
          textAlign: 'start',
          [`&${o}-rtl`]: { direction: 'rtl' },
          '&, a, a:hover': { color: e.tagDefaultColor },
          [`${o}-close-icon`]: {
            marginInlineStart: a,
            color: e.colorTextDescription,
            fontSize: e.tagIconSize,
            cursor: 'pointer',
            transition: `all ${e.motionDurationMid}`,
            '&:hover': { color: e.colorTextHeading },
          },
          [`&${o}-has-color`]: {
            borderColor: 'transparent',
            [`&, a, a:hover, ${e.iconCls}-close, ${e.iconCls}-close:hover`]: {
              color: e.colorTextLightSolid,
            },
          },
          '&-checkable': {
            backgroundColor: 'transparent',
            borderColor: 'transparent',
            cursor: 'pointer',
            [`&:not(${o}-checkable-checked):hover`]: {
              color: e.colorPrimary,
              backgroundColor: e.colorFillSecondary,
            },
            '&:active, &-checked': { color: e.colorTextLightSolid },
            '&-checked': {
              backgroundColor: e.colorPrimary,
              '&:hover': { backgroundColor: e.colorPrimaryHover },
            },
            '&:active': { backgroundColor: e.colorPrimaryActive },
          },
          '&-hidden': { display: 'none' },
          [`> ${e.iconCls} + span, > span + ${e.iconCls}`]: { marginInlineStart: i },
        }),
        [`${o}-borderless`]: { borderColor: 'transparent', background: e.tagBorderlessBg },
      }
    },
    ww = en('Tag', (e) => {
      const { fontSize: t, lineHeight: n, lineWidth: r, fontSizeIcon: o } = e,
        i = Math.round(t * n),
        a = e.fontSizeSM,
        s = i - r * 2,
        l = e.colorFillAlter,
        u = e.colorText,
        c = ot(e, {
          tagFontSize: a,
          tagLineHeight: s,
          tagDefaultBg: l,
          tagDefaultColor: u,
          tagIconSize: o - 2 * r,
          tagPaddingHorizontal: 8,
          tagBorderlessBg: e.colorFillTertiary,
        })
      return [
        KP(c),
        XP(c),
        lo(c, 'success', 'Success'),
        lo(c, 'processing', 'Info'),
        lo(c, 'error', 'Error'),
        lo(c, 'warning', 'Warning'),
      ]
    }),
    ZP = () => ({
      prefixCls: String,
      checked: { type: Boolean, default: void 0 },
      onChange: { type: Function },
      onClick: { type: Function },
      'onUpdate:checked': Function,
    }),
    zd = te({
      compatConfig: { MODE: 3 },
      name: 'ACheckableTag',
      inheritAttrs: !1,
      props: ZP(),
      setup(e, t) {
        let { slots: n, emit: r, attrs: o } = t
        const { prefixCls: i } = Ge('tag', e),
          [a, s] = ww(i),
          l = (c) => {
            const { checked: d } = e
            ;(r('update:checked', !d), r('change', !d), r('click', c))
          },
          u = X(() =>
            xe(i.value, s.value, {
              [`${i.value}-checkable`]: !0,
              [`${i.value}-checkable-checked`]: e.checked,
            })
          )
        return () => {
          var c
          return a(
            F('span', oe(oe({}, o), {}, { class: [u.value, o.class], onClick: l }), [
              (c = n.default) === null || c === void 0 ? void 0 : c.call(n),
            ])
          )
        }
      },
    }),
    JP = () => ({
      prefixCls: String,
      color: { type: String },
      closable: { type: Boolean, default: !1 },
      closeIcon: Q.any,
      visible: { type: Boolean, default: void 0 },
      onClose: { type: Function },
      onClick: $r(),
      'onUpdate:visible': Function,
      icon: Q.any,
      bordered: { type: Boolean, default: !0 },
    }),
    vn = te({
      compatConfig: { MODE: 3 },
      name: 'ATag',
      inheritAttrs: !1,
      props: JP(),
      slots: Object,
      setup(e, t) {
        let { slots: n, emit: r, attrs: o } = t
        const { prefixCls: i, direction: a } = Ge('tag', e),
          [s, l] = ww(i),
          u = ce(!0)
        Et(() => {
          e.visible !== void 0 && (u.value = e.visible)
        })
        const c = (g) => {
            ;(g.stopPropagation(),
              r('update:visible', !1),
              r('close', g),
              !g.defaultPrevented && e.visible === void 0 && (u.value = !1))
          },
          d = X(() => lw(e.color) || VO(e.color)),
          f = X(() =>
            xe(i.value, l.value, {
              [`${i.value}-${e.color}`]: d.value,
              [`${i.value}-has-color`]: e.color && !d.value,
              [`${i.value}-hidden`]: !u.value,
              [`${i.value}-rtl`]: a.value === 'rtl',
              [`${i.value}-borderless`]: !e.bordered,
            })
          ),
          h = (g) => {
            r('click', g)
          }
        return () => {
          var g, m, v
          const {
              icon: b = (g = n.icon) === null || g === void 0 ? void 0 : g.call(n),
              color: y,
              closeIcon: p = (m = n.closeIcon) === null || m === void 0 ? void 0 : m.call(n),
              closable: _ = !1,
            } = e,
            x = () =>
              _
                ? p
                  ? F('span', { class: `${i.value}-close-icon`, onClick: c }, [p])
                  : F(u_, { class: `${i.value}-close-icon`, onClick: c }, null)
                : null,
            S = { backgroundColor: y && !d.value ? y : void 0 },
            w = b || null,
            T = (v = n.default) === null || v === void 0 ? void 0 : v.call(n),
            A = w ? F(Re, null, [w, F('span', null, [T])]) : T,
            $ = e.onClick !== void 0,
            P = F(
              'span',
              oe(oe({}, o), {}, { onClick: h, class: [f.value, o.class], style: [S, o.style] }),
              [A, x()]
            )
          return s($ ? F(cw, null, { default: () => [P] }) : P)
        }
      },
    })
  vn.CheckableTag = zd
  vn.install = function (e) {
    return (e.component(vn.name, vn), e.component(zd.name, zd), e)
  }
  const br = (e) => e != null && (Array.isArray(e) ? Fr(e).length : !0)
  function Tf(e) {
    return br(e.prefix) || br(e.suffix) || br(e.allowClear)
  }
  function wo(e) {
    return br(e.addonBefore) || br(e.addonAfter)
  }
  function Ld(e) {
    return typeof e > 'u' || e === null ? '' : String(e)
  }
  function _r(e, t, n, r) {
    if (!n) return
    const o = t
    if (t.type === 'click') {
      ;(Object.defineProperty(o, 'target', { writable: !0 }),
        Object.defineProperty(o, 'currentTarget', { writable: !0 }))
      const i = e.cloneNode(!0)
      ;((o.target = i), (o.currentTarget = i), (i.value = ''), n(o))
      return
    }
    if (r !== void 0) {
      ;(Object.defineProperty(o, 'target', { writable: !0 }),
        Object.defineProperty(o, 'currentTarget', { writable: !0 }),
        (o.target = e),
        (o.currentTarget = e),
        (e.value = r),
        n(o))
      return
    }
    n(o)
  }
  function Sw(e, t) {
    if (!e) return
    e.focus(t)
    const { cursor: n } = t || {}
    if (n) {
      const r = e.value.length
      switch (n) {
        case 'start':
          e.setSelectionRange(0, 0)
          break
        case 'end':
          e.setSelectionRange(r, r)
          break
        default:
          e.setSelectionRange(0, r)
      }
    }
  }
  const QP = () => ({
      addonBefore: Q.any,
      addonAfter: Q.any,
      prefix: Q.any,
      suffix: Q.any,
      clearIcon: Q.any,
      affixWrapperClassName: String,
      groupClassName: String,
      wrapperClassName: String,
      inputClassName: String,
      allowClear: { type: Boolean, default: void 0 },
    }),
    xw = () =>
      D(D({}, QP()), {
        value: { type: [String, Number, Symbol], default: void 0 },
        defaultValue: { type: [String, Number, Symbol], default: void 0 },
        inputElement: Q.any,
        prefixCls: String,
        disabled: { type: Boolean, default: void 0 },
        focused: { type: Boolean, default: void 0 },
        triggerFocus: Function,
        readonly: { type: Boolean, default: void 0 },
        handleReset: Function,
        hidden: { type: Boolean, default: void 0 },
      }),
    Cw = () =>
      D(D({}, xw()), {
        id: String,
        placeholder: { type: [String, Number] },
        autocomplete: String,
        type: Oo('text'),
        name: String,
        size: { type: String },
        autofocus: { type: Boolean, default: void 0 },
        lazy: { type: Boolean, default: !0 },
        maxlength: Number,
        loading: { type: Boolean, default: void 0 },
        bordered: { type: Boolean, default: void 0 },
        showCount: { type: [Boolean, Object] },
        htmlSize: Number,
        onPressEnter: Function,
        onKeydown: Function,
        onKeyup: Function,
        onFocus: Function,
        onBlur: Function,
        onChange: Function,
        onInput: Function,
        'onUpdate:value': Function,
        onCompositionstart: Function,
        onCompositionend: Function,
        valueModifiers: Object,
        hidden: { type: Boolean, default: void 0 },
        status: String,
      }),
    eI = te({
      name: 'BaseInput',
      inheritAttrs: !1,
      props: xw(),
      setup(e, t) {
        let { slots: n, attrs: r } = t
        const o = de(),
          i = (s) => {
            var l
            if (!((l = o.value) === null || l === void 0) && l.contains(s.target)) {
              const { triggerFocus: u } = e
              u?.()
            }
          },
          a = () => {
            var s
            const {
              allowClear: l,
              value: u,
              disabled: c,
              readonly: d,
              handleReset: f,
              suffix: h = n.suffix,
              prefixCls: g,
            } = e
            if (!l) return null
            const m = !c && !d && u,
              v = `${g}-clear-icon`,
              b = ((s = n.clearIcon) === null || s === void 0 ? void 0 : s.call(n)) || '*'
            return F(
              'span',
              {
                onClick: f,
                onMousedown: (y) => y.preventDefault(),
                class: xe({ [`${v}-hidden`]: !m, [`${v}-has-suffix`]: !!h }, v),
                role: 'button',
                tabindex: -1,
              },
              [b]
            )
          }
        return () => {
          var s, l
          const {
            focused: u,
            value: c,
            disabled: d,
            allowClear: f,
            readonly: h,
            hidden: g,
            prefixCls: m,
            prefix: v = (s = n.prefix) === null || s === void 0 ? void 0 : s.call(n),
            suffix: b = (l = n.suffix) === null || l === void 0 ? void 0 : l.call(n),
            addonAfter: y = n.addonAfter,
            addonBefore: p = n.addonBefore,
            inputElement: _,
            affixWrapperClassName: x,
            wrapperClassName: S,
            groupClassName: w,
          } = e
          let T = Ke(_, { value: c, hidden: g })
          if (Tf({ prefix: v, suffix: b, allowClear: f })) {
            const A = `${m}-affix-wrapper`,
              $ = xe(
                A,
                {
                  [`${A}-disabled`]: d,
                  [`${A}-focused`]: u,
                  [`${A}-readonly`]: h,
                  [`${A}-input-with-clear-btn`]: b && f && c,
                },
                !wo({ addonAfter: y, addonBefore: p }) && r.class,
                x
              ),
              P = (b || f) && F('span', { class: `${m}-suffix` }, [a(), b])
            T = F(
              'span',
              {
                class: $,
                style: r.style,
                hidden: !wo({ addonAfter: y, addonBefore: p }) && g,
                onMousedown: i,
                ref: o,
              },
              [
                v && F('span', { class: `${m}-prefix` }, [v]),
                Ke(_, { style: null, value: c, hidden: null }),
                P,
              ]
            )
          }
          if (wo({ addonAfter: y, addonBefore: p })) {
            const A = `${m}-group`,
              $ = `${A}-addon`,
              P = xe(`${m}-wrapper`, A, S),
              E = xe(`${m}-group-wrapper`, r.class, w)
            return F('span', { class: E, style: r.style, hidden: g }, [
              F('span', { class: P }, [
                p && F('span', { class: $ }, [p]),
                Ke(T, { style: null, hidden: null }),
                y && F('span', { class: $ }, [y]),
              ]),
            ])
          }
          return T
        }
      },
    })
  var tI = function (e, t) {
    var n = {}
    for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
    if (e != null && typeof Object.getOwnPropertySymbols == 'function')
      for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
        t.indexOf(r[o]) < 0 &&
          Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
          (n[r[o]] = e[r[o]])
    return n
  }
  const nI = te({
      name: 'VCInput',
      inheritAttrs: !1,
      props: Cw(),
      setup(e, t) {
        let { slots: n, attrs: r, expose: o, emit: i } = t
        const a = ce(e.value === void 0 ? e.defaultValue : e.value),
          s = ce(!1),
          l = ce(),
          u = ce()
        ;(me(
          () => e.value,
          () => {
            a.value = e.value
          }
        ),
          me(
            () => e.disabled,
            () => {
              e.disabled && (s.value = !1)
            }
          ))
        const c = (w) => {
            l.value && Sw(l.value.input, w)
          },
          d = () => {
            var w
            ;(w = l.value.input) === null || w === void 0 || w.blur()
          },
          f = (w, T, A) => {
            var $
            ;($ = l.value.input) === null || $ === void 0 || $.setSelectionRange(w, T, A)
          },
          h = () => {
            var w
            ;(w = l.value.input) === null || w === void 0 || w.select()
          }
        o({
          focus: c,
          blur: d,
          input: X(() => {
            var w
            return (w = l.value.input) === null || w === void 0 ? void 0 : w.input
          }),
          stateValue: a,
          setSelectionRange: f,
          select: h,
        })
        const g = (w) => {
            i('change', w)
          },
          m = (w, T) => {
            a.value !== w &&
              (e.value === void 0
                ? (a.value = w)
                : Ne(() => {
                    var A
                    l.value.input.value !== a.value &&
                      ((A = u.value) === null || A === void 0 || A.$forceUpdate())
                  }),
              Ne(() => {
                T && T()
              }))
          },
          v = (w) => {
            const { value: T } = w.target
            if (a.value === T) return
            const A = w.target.value
            ;(_r(l.value.input, w, g), m(A))
          },
          b = (w) => {
            ;(w.keyCode === 13 && i('pressEnter', w), i('keydown', w))
          },
          y = (w) => {
            ;((s.value = !0), i('focus', w))
          },
          p = (w) => {
            ;((s.value = !1), i('blur', w))
          },
          _ = (w) => {
            ;(_r(l.value.input, w, g),
              m('', () => {
                c()
              }))
          },
          x = () => {
            var w, T
            const {
                addonBefore: A = n.addonBefore,
                addonAfter: $ = n.addonAfter,
                disabled: P,
                valueModifiers: E = {},
                htmlSize: z,
                autocomplete: C,
                prefixCls: R,
                inputClassName: N,
                prefix: j = (w = n.prefix) === null || w === void 0 ? void 0 : w.call(n),
                suffix: V = (T = n.suffix) === null || T === void 0 ? void 0 : T.call(n),
                allowClear: H,
                type: G = 'text',
              } = e,
              Y = dt(e, [
                'prefixCls',
                'onPressEnter',
                'addonBefore',
                'addonAfter',
                'prefix',
                'suffix',
                'allowClear',
                'defaultValue',
                'size',
                'bordered',
                'htmlSize',
                'lazy',
                'showCount',
                'valueModifiers',
                'showCount',
                'affixWrapperClassName',
                'groupClassName',
                'inputClassName',
                'wrapperClassName',
              ]),
              Z = D(D(D({}, Y), r), {
                autocomplete: C,
                onChange: v,
                onInput: v,
                onFocus: y,
                onBlur: p,
                onKeydown: b,
                class: xe(
                  R,
                  { [`${R}-disabled`]: P },
                  N,
                  !wo({ addonAfter: $, addonBefore: A }) &&
                    !Tf({ prefix: j, suffix: V, allowClear: H }) &&
                    r.class
                ),
                ref: l,
                key: 'ant-input',
                size: z,
                type: G,
                lazy: e.lazy,
              })
            return (
              E.lazy && delete Z.onInput,
              Z.autofocus || delete Z.autofocus,
              F(J_, dt(Z, ['size']), null)
            )
          },
          S = () => {
            var w
            const {
                maxlength: T,
                suffix: A = (w = n.suffix) === null || w === void 0 ? void 0 : w.call(n),
                showCount: $,
                prefixCls: P,
              } = e,
              E = Number(T) > 0
            if (A || $) {
              const z = [...Ld(a.value)].length,
                C =
                  typeof $ == 'object'
                    ? $.formatter({ count: z, maxlength: T })
                    : `${z}${E ? ` / ${T}` : ''}`
              return F(Re, null, [
                !!$ &&
                  F(
                    'span',
                    {
                      class: xe(`${P}-show-count-suffix`, { [`${P}-show-count-has-suffix`]: !!A }),
                    },
                    [C]
                  ),
                A,
              ])
            }
            return null
          }
        return (
          Me(() => {}),
          () => {
            const { prefixCls: w, disabled: T } = e,
              A = tI(e, ['prefixCls', 'disabled'])
            return F(
              eI,
              oe(
                oe(oe({}, A), r),
                {},
                {
                  ref: u,
                  prefixCls: w,
                  inputElement: x(),
                  handleReset: _,
                  value: Ld(a.value),
                  focused: s.value,
                  triggerFocus: c,
                  suffix: S(),
                  disabled: T,
                }
              ),
              n
            )
          }
        )
      },
    }),
    ai = () =>
      dt(Cw(), ['wrapperClassName', 'groupClassName', 'inputClassName', 'affixWrapperClassName']),
    Ew = () =>
      D(D({}, dt(ai(), ['prefix', 'addonBefore', 'addonAfter', 'suffix'])), {
        rows: Number,
        autosize: { type: [Boolean, Object], default: void 0 },
        autoSize: { type: [Boolean, Object], default: void 0 },
        onResize: { type: Function },
        onCompositionstart: $r(),
        onCompositionend: $r(),
        valueModifiers: Object,
      })
  var rI = function (e, t) {
    var n = {}
    for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
    if (e != null && typeof Object.getOwnPropertySymbols == 'function')
      for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
        t.indexOf(r[o]) < 0 &&
          Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
          (n[r[o]] = e[r[o]])
    return n
  }
  const Fe = te({
      compatConfig: { MODE: 3 },
      name: 'AInput',
      inheritAttrs: !1,
      props: ai(),
      setup(e, t) {
        let { slots: n, attrs: r, expose: o, emit: i } = t
        const a = de(),
          s = Q_(),
          l = jn.useInject(),
          u = X(() => wf(l.status, e.status)),
          { direction: c, prefixCls: d, size: f, autocomplete: h } = Ge('input', e),
          { compactSize: g, compactItemClassnames: m } = nw(d, c),
          v = X(() => g.value || f.value),
          [b, y] = $f(d),
          p = of()
        o({
          focus: (z) => {
            var C
            ;(C = a.value) === null || C === void 0 || C.focus(z)
          },
          blur: () => {
            var z
            ;(z = a.value) === null || z === void 0 || z.blur()
          },
          input: a,
          setSelectionRange: (z, C, R) => {
            var N
            ;(N = a.value) === null || N === void 0 || N.setSelectionRange(z, C, R)
          },
          select: () => {
            var z
            ;(z = a.value) === null || z === void 0 || z.select()
          },
        })
        const T = de([]),
          A = () => {
            T.value.push(
              setTimeout(() => {
                var z, C, R, N
                !((z = a.value) === null || z === void 0) &&
                  z.input &&
                  ((C = a.value) === null || C === void 0
                    ? void 0
                    : C.input.getAttribute('type')) === 'password' &&
                  !((R = a.value) === null || R === void 0) &&
                  R.input.hasAttribute('value') &&
                  ((N = a.value) === null || N === void 0 || N.input.removeAttribute('value'))
              })
            )
          }
        ;(Me(() => {
          A()
        }),
          cx(() => {
            T.value.forEach((z) => clearTimeout(z))
          }),
          je(() => {
            T.value.forEach((z) => clearTimeout(z))
          }))
        const $ = (z) => {
            ;(A(), i('blur', z), s.onFieldBlur())
          },
          P = (z) => {
            ;(A(), i('focus', z))
          },
          E = (z) => {
            ;(i('update:value', z.target.value), i('change', z), i('input', z), s.onFieldChange())
          }
        return () => {
          var z, C, R, N, j, V
          const { hasFeedback: H, feedbackIcon: G } = l,
            {
              allowClear: Y,
              bordered: Z = !0,
              prefix: ne = (z = n.prefix) === null || z === void 0 ? void 0 : z.call(n),
              suffix: B = (C = n.suffix) === null || C === void 0 ? void 0 : C.call(n),
              addonAfter: L = (R = n.addonAfter) === null || R === void 0 ? void 0 : R.call(n),
              addonBefore: k = (N = n.addonBefore) === null || N === void 0 ? void 0 : N.call(n),
              id: U = (j = s.id) === null || j === void 0 ? void 0 : j.value,
            } = e,
            J = rI(e, [
              'allowClear',
              'bordered',
              'prefix',
              'suffix',
              'addonAfter',
              'addonBefore',
              'id',
            ]),
            re = (H || B) && F(Re, null, [B, H && G]),
            ie = d.value,
            _e = Tf({ prefix: ne, suffix: B }) || !!H,
            ye = n.clearIcon || (() => F(af, null, null))
          return b(
            F(
              nI,
              oe(
                oe(oe({}, r), dt(J, ['onUpdate:value', 'onChange', 'onInput'])),
                {},
                {
                  onChange: E,
                  id: U,
                  disabled: (V = e.disabled) !== null && V !== void 0 ? V : p.value,
                  ref: a,
                  prefixCls: ie,
                  autocomplete: h.value,
                  onBlur: $,
                  onFocus: P,
                  prefix: ne,
                  suffix: re,
                  allowClear: Y,
                  addonAfter:
                    L && F(pp, null, { default: () => [F(hp, null, { default: () => [L] })] }),
                  addonBefore:
                    k && F(pp, null, { default: () => [F(hp, null, { default: () => [k] })] }),
                  class: [r.class, m.value],
                  inputClassName: xe(
                    {
                      [`${ie}-sm`]: v.value === 'small',
                      [`${ie}-lg`]: v.value === 'large',
                      [`${ie}-rtl`]: c.value === 'rtl',
                      [`${ie}-borderless`]: !Z,
                    },
                    !_e && yr(ie, u.value),
                    y.value
                  ),
                  affixWrapperClassName: xe(
                    {
                      [`${ie}-affix-wrapper-sm`]: v.value === 'small',
                      [`${ie}-affix-wrapper-lg`]: v.value === 'large',
                      [`${ie}-affix-wrapper-rtl`]: c.value === 'rtl',
                      [`${ie}-affix-wrapper-borderless`]: !Z,
                    },
                    yr(`${ie}-affix-wrapper`, u.value, H),
                    y.value
                  ),
                  wrapperClassName: xe({ [`${ie}-group-rtl`]: c.value === 'rtl' }, y.value),
                  groupClassName: xe(
                    {
                      [`${ie}-group-wrapper-sm`]: v.value === 'small',
                      [`${ie}-group-wrapper-lg`]: v.value === 'large',
                      [`${ie}-group-wrapper-rtl`]: c.value === 'rtl',
                    },
                    yr(`${ie}-group-wrapper`, u.value, H),
                    y.value
                  ),
                }
              ),
              D(D({}, n), { clearIcon: ye })
            )
          )
        }
      },
    }),
    oI = te({
      compatConfig: { MODE: 3 },
      name: 'AInputGroup',
      inheritAttrs: !1,
      props: {
        prefixCls: String,
        size: { type: String },
        compact: { type: Boolean, default: void 0 },
      },
      setup(e, t) {
        let { slots: n, attrs: r } = t
        const { prefixCls: o, direction: i, getPrefixCls: a } = Ge('input-group', e),
          s = jn.useInject()
        jn.useProvide(s, { isFormItemInput: !1 })
        const l = X(() => a('input')),
          [u, c] = $f(l),
          d = X(() => {
            const f = o.value
            return {
              [`${f}`]: !0,
              [c.value]: !0,
              [`${f}-lg`]: e.size === 'large',
              [`${f}-sm`]: e.size === 'small',
              [`${f}-compact`]: e.compact,
              [`${f}-rtl`]: i.value === 'rtl',
            }
          })
        return () => {
          var f
          return u(
            F('span', oe(oe({}, r), {}, { class: xe(d.value, r.class) }), [
              (f = n.default) === null || f === void 0 ? void 0 : f.call(n),
            ])
          )
        }
      },
    })
  var iI = function (e, t) {
    var n = {}
    for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
    if (e != null && typeof Object.getOwnPropertySymbols == 'function')
      for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
        t.indexOf(r[o]) < 0 &&
          Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
          (n[r[o]] = e[r[o]])
    return n
  }
  const aI = te({
      compatConfig: { MODE: 3 },
      name: 'AInputSearch',
      inheritAttrs: !1,
      props: D(D({}, ai()), {
        inputPrefixCls: String,
        enterButton: Q.any,
        onSearch: { type: Function },
      }),
      setup(e, t) {
        let { slots: n, attrs: r, expose: o, emit: i } = t
        const a = ce(),
          s = ce(!1)
        o({
          focus: () => {
            var x
            ;(x = a.value) === null || x === void 0 || x.focus()
          },
          blur: () => {
            var x
            ;(x = a.value) === null || x === void 0 || x.blur()
          },
        })
        const c = (x) => {
            ;(i('update:value', x.target.value),
              x && x.target && x.type === 'click' && i('search', x.target.value, x),
              i('change', x))
          },
          d = (x) => {
            var S
            document.activeElement ===
              ((S = a.value) === null || S === void 0 ? void 0 : S.input) && x.preventDefault()
          },
          f = (x) => {
            var S, w
            i(
              'search',
              (w = (S = a.value) === null || S === void 0 ? void 0 : S.input) === null ||
                w === void 0
                ? void 0
                : w.stateValue,
              x
            )
          },
          h = (x) => {
            s.value || e.loading || f(x)
          },
          g = (x) => {
            ;((s.value = !0), i('compositionstart', x))
          },
          m = (x) => {
            ;((s.value = !1), i('compositionend', x))
          },
          { prefixCls: v, getPrefixCls: b, direction: y, size: p } = Ge('input-search', e),
          _ = X(() => b('input', e.inputPrefixCls))
        return () => {
          var x, S, w, T
          const {
              disabled: A,
              loading: $,
              addonAfter: P = (x = n.addonAfter) === null || x === void 0 ? void 0 : x.call(n),
              suffix: E = (S = n.suffix) === null || S === void 0 ? void 0 : S.call(n),
            } = e,
            z = iI(e, ['disabled', 'loading', 'addonAfter', 'suffix'])
          let {
            enterButton: C = (T =
              (w = n.enterButton) === null || w === void 0 ? void 0 : w.call(n)) !== null &&
            T !== void 0
              ? T
              : !1,
          } = e
          C = C || C === ''
          const R = typeof C == 'boolean' ? F(bf, null, null) : null,
            N = `${v.value}-button`,
            j = Array.isArray(C) ? C[0] : C
          let V
          const H = j.type && sO(j.type) && j.type.__ANT_BUTTON
          if (H || j.tagName === 'button')
            V = Ke(
              j,
              D(
                { onMousedown: d, onClick: f, key: 'enterButton' },
                H ? { class: N, size: p.value } : {}
              ),
              !1
            )
          else {
            const Y = R && !C
            V = F(
              _t,
              {
                class: N,
                type: C ? 'primary' : void 0,
                size: p.value,
                disabled: A,
                key: 'enterButton',
                onMousedown: d,
                onClick: f,
                loading: $,
                icon: Y ? R : null,
              },
              { default: () => [Y ? null : R || C] }
            )
          }
          P && (V = [V, P])
          const G = xe(
            v.value,
            {
              [`${v.value}-rtl`]: y.value === 'rtl',
              [`${v.value}-${p.value}`]: !!p.value,
              [`${v.value}-with-button`]: !!C,
            },
            r.class
          )
          return F(
            Fe,
            oe(
              oe(oe({ ref: a }, dt(z, ['onUpdate:value', 'onSearch', 'enterButton'])), r),
              {},
              {
                onPressEnter: h,
                onCompositionstart: g,
                onCompositionend: m,
                size: p.value,
                prefixCls: _.value,
                addonAfter: V,
                suffix: E,
                onChange: c,
                class: G,
                disabled: A,
              }
            ),
            n
          )
        }
      },
    }),
    Ip = (e) => e != null && (Array.isArray(e) ? Fr(e).length : !0)
  function sI(e) {
    return Ip(e.addonBefore) || Ip(e.addonAfter)
  }
  const lI = ['text', 'input'],
    uI = te({
      compatConfig: { MODE: 3 },
      name: 'ClearableLabeledInput',
      inheritAttrs: !1,
      props: {
        prefixCls: String,
        inputType: Q.oneOf(To('text', 'input')),
        value: on(),
        defaultValue: on(),
        allowClear: { type: Boolean, default: void 0 },
        element: on(),
        handleReset: Function,
        disabled: { type: Boolean, default: void 0 },
        direction: { type: String },
        size: { type: String },
        suffix: on(),
        prefix: on(),
        addonBefore: on(),
        addonAfter: on(),
        readonly: { type: Boolean, default: void 0 },
        focused: { type: Boolean, default: void 0 },
        bordered: { type: Boolean, default: !0 },
        triggerFocus: { type: Function },
        hidden: Boolean,
        status: String,
        hashId: String,
      },
      setup(e, t) {
        let { slots: n, attrs: r } = t
        const o = jn.useInject(),
          i = (s) => {
            const { value: l, disabled: u, readonly: c, handleReset: d, suffix: f = n.suffix } = e,
              h = !u && !c && l,
              g = `${s}-clear-icon`
            return F(
              af,
              {
                onClick: d,
                onMousedown: (m) => m.preventDefault(),
                class: xe({ [`${g}-hidden`]: !h, [`${g}-has-suffix`]: !!f }, g),
                role: 'button',
              },
              null
            )
          },
          a = (s, l) => {
            const {
                value: u,
                allowClear: c,
                direction: d,
                bordered: f,
                hidden: h,
                status: g,
                addonAfter: m = n.addonAfter,
                addonBefore: v = n.addonBefore,
                hashId: b,
              } = e,
              { status: y, hasFeedback: p } = o
            if (!c) return Ke(l, { value: u, disabled: e.disabled })
            const _ = xe(
              `${s}-affix-wrapper`,
              `${s}-affix-wrapper-textarea-with-clear-btn`,
              yr(`${s}-affix-wrapper`, wf(y, g), p),
              {
                [`${s}-affix-wrapper-rtl`]: d === 'rtl',
                [`${s}-affix-wrapper-borderless`]: !f,
                [`${r.class}`]: !sI({ addonAfter: m, addonBefore: v }) && r.class,
              },
              b
            )
            return F('span', { class: _, style: r.style, hidden: h }, [
              Ke(l, { style: null, value: u, disabled: e.disabled }),
              i(s),
            ])
          }
        return () => {
          var s
          const {
            prefixCls: l,
            inputType: u,
            element: c = (s = n.element) === null || s === void 0 ? void 0 : s.call(n),
          } = e
          return u === lI[0] ? a(l, c) : null
        }
      },
    }),
    cI = `
  min-height:0 !important;
  max-height:none !important;
  height:0 !important;
  visibility:hidden !important;
  overflow:hidden !important;
  position:absolute !important;
  z-index:-1000 !important;
  top:0 !important;
  right:0 !important;
  pointer-events: none !important;
`,
    dI = [
      'letter-spacing',
      'line-height',
      'padding-top',
      'padding-bottom',
      'font-family',
      'font-weight',
      'font-size',
      'font-variant',
      'text-rendering',
      'text-transform',
      'width',
      'text-indent',
      'padding-left',
      'padding-right',
      'border-width',
      'box-sizing',
      'word-break',
      'white-space',
    ],
    Wi = {}
  let rt
  function fI(e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1
    const n = e.getAttribute('id') || e.getAttribute('data-reactid') || e.getAttribute('name')
    if (t && Wi[n]) return Wi[n]
    const r = window.getComputedStyle(e),
      o =
        r.getPropertyValue('box-sizing') ||
        r.getPropertyValue('-moz-box-sizing') ||
        r.getPropertyValue('-webkit-box-sizing'),
      i =
        parseFloat(r.getPropertyValue('padding-bottom')) +
        parseFloat(r.getPropertyValue('padding-top')),
      a =
        parseFloat(r.getPropertyValue('border-bottom-width')) +
        parseFloat(r.getPropertyValue('border-top-width')),
      l = {
        sizingStyle: dI.map((u) => `${u}:${r.getPropertyValue(u)}`).join(';'),
        paddingSize: i,
        borderSize: a,
        boxSizing: o,
      }
    return (t && n && (Wi[n] = l), l)
  }
  function hI(e) {
    let t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1,
      n = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : null,
      r = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : null
    ;(rt ||
      ((rt = document.createElement('textarea')),
      rt.setAttribute('tab-index', '-1'),
      rt.setAttribute('aria-hidden', 'true'),
      document.body.appendChild(rt)),
      e.getAttribute('wrap')
        ? rt.setAttribute('wrap', e.getAttribute('wrap'))
        : rt.removeAttribute('wrap'))
    const { paddingSize: o, borderSize: i, boxSizing: a, sizingStyle: s } = fI(e, t)
    ;(rt.setAttribute('style', `${s};${cI}`), (rt.value = e.value || e.placeholder || ''))
    let l,
      u,
      c,
      d = rt.scrollHeight
    if (
      (a === 'border-box' ? (d += i) : a === 'content-box' && (d -= o), n !== null || r !== null)
    ) {
      rt.value = ' '
      const h = rt.scrollHeight - o
      ;(n !== null && ((l = h * n), a === 'border-box' && (l = l + o + i), (d = Math.max(l, d))),
        r !== null &&
          ((u = h * r),
          a === 'border-box' && (u = u + o + i),
          (c = d > u ? '' : 'hidden'),
          (d = Math.min(u, d))))
    }
    const f = { height: `${d}px`, overflowY: c, resize: 'none' }
    return (l && (f.minHeight = `${l}px`), u && (f.maxHeight = `${u}px`), f)
  }
  const Ui = 0,
    Yi = 1,
    Xi = 2,
    pI = te({
      compatConfig: { MODE: 3 },
      name: 'ResizableTextArea',
      inheritAttrs: !1,
      props: Ew(),
      setup(e, t) {
        let { attrs: n, emit: r, expose: o } = t,
          i,
          a
        const s = de(),
          l = de({}),
          u = de(Xi)
        je(() => {
          ;(He.cancel(i), He.cancel(a))
        })
        const c = () => {
            try {
              if (s.value && document.activeElement === s.value.input) {
                const S = s.value.getSelectionStart(),
                  w = s.value.getSelectionEnd(),
                  T = s.value.getScrollTop()
                ;(s.value.setSelectionRange(S, w), s.value.setScrollTop(T))
              }
            } catch {}
          },
          d = de(),
          f = de()
        Et(() => {
          const S = e.autoSize || e.autosize
          S
            ? ((d.value = S.minRows), (f.value = S.maxRows))
            : ((d.value = void 0), (f.value = void 0))
        })
        const h = X(() => !!(e.autoSize || e.autosize)),
          g = () => {
            u.value = Ui
          }
        me(
          [() => e.value, d, f, h],
          () => {
            h.value && g()
          },
          { immediate: !0 }
        )
        const m = de()
        me(
          [u, s],
          () => {
            if (s.value)
              if (u.value === Ui) u.value = Yi
              else if (u.value === Yi) {
                const S = hI(s.value.input, !1, d.value, f.value)
                ;((u.value = Xi), (m.value = S))
              } else c()
          },
          { immediate: !0, flush: 'post' }
        )
        const v = Qe(),
          b = de(),
          y = () => {
            He.cancel(b.value)
          },
          p = (S) => {
            u.value === Xi &&
              (r('resize', S),
              h.value &&
                (y(),
                (b.value = He(() => {
                  g()
                }))))
          }
        ;(je(() => {
          y()
        }),
          o({
            resizeTextarea: () => {
              g()
            },
            textArea: X(() => {
              var S
              return (S = s.value) === null || S === void 0 ? void 0 : S.input
            }),
            instance: v,
          }),
          tf(e.autosize === void 0))
        const x = () => {
          const { prefixCls: S, disabled: w } = e,
            T = dt(e, [
              'prefixCls',
              'onPressEnter',
              'autoSize',
              'autosize',
              'defaultValue',
              'allowClear',
              'type',
              'maxlength',
              'valueModifiers',
            ]),
            A = xe(S, n.class, { [`${S}-disabled`]: w }),
            $ = h.value ? m.value : null,
            P = [n.style, l.value, $],
            E = D(D(D({}, T), n), { style: P, class: A })
          return (
            (u.value === Ui || u.value === Yi) &&
              P.push({ overflowX: 'hidden', overflowY: 'hidden' }),
            E.autofocus || delete E.autofocus,
            E.rows === 0 && delete E.rows,
            F(
              eC,
              { onResize: p, disabled: !h.value },
              { default: () => [F(J_, oe(oe({}, E), {}, { ref: s, tag: 'textarea' }), null)] }
            )
          )
        }
        return () => x()
      },
    })
  function $w(e, t) {
    return [...(e || '')].slice(0, t).join('')
  }
  function Ap(e, t, n, r) {
    let o = n
    return (
      e ? (o = $w(n, r)) : [...(t || '')].length < n.length && [...(n || '')].length > r && (o = t),
      o
    )
  }
  const vI = te({
    compatConfig: { MODE: 3 },
    name: 'ATextarea',
    inheritAttrs: !1,
    props: Ew(),
    setup(e, t) {
      let { attrs: n, expose: r, emit: o } = t
      var i
      const a = Q_(),
        s = jn.useInject(),
        l = X(() => wf(s.status, e.status)),
        u = ce((i = e.value) !== null && i !== void 0 ? i : e.defaultValue),
        c = ce(),
        d = ce(''),
        { prefixCls: f, size: h, direction: g } = Ge('input', e),
        [m, v] = $f(f),
        b = of(),
        y = X(() => e.showCount === '' || e.showCount || !1),
        p = X(() => Number(e.maxlength) > 0),
        _ = ce(!1),
        x = ce(),
        S = ce(0),
        w = (H) => {
          ;((_.value = !0),
            (x.value = d.value),
            (S.value = H.currentTarget.selectionStart),
            o('compositionstart', H))
        },
        T = (H) => {
          var G
          _.value = !1
          let Y = H.currentTarget.value
          if (p.value) {
            const Z =
              S.value >= e.maxlength + 1 ||
              S.value === ((G = x.value) === null || G === void 0 ? void 0 : G.length)
            Y = Ap(Z, x.value, Y, e.maxlength)
          }
          ;(Y !== d.value && (E(Y), _r(H.currentTarget, H, R, Y)), o('compositionend', H))
        },
        A = Qe()
      me(
        () => e.value,
        () => {
          var H
          ;('value' in A.vnode.props, (u.value = (H = e.value) !== null && H !== void 0 ? H : ''))
        }
      )
      const $ = (H) => {
          var G
          Sw((G = c.value) === null || G === void 0 ? void 0 : G.textArea, H)
        },
        P = () => {
          var H, G
          ;(G = (H = c.value) === null || H === void 0 ? void 0 : H.textArea) === null ||
            G === void 0 ||
            G.blur()
        },
        E = (H, G) => {
          u.value !== H &&
            (e.value === void 0
              ? (u.value = H)
              : Ne(() => {
                  var Y, Z, ne
                  c.value.textArea.value !== d.value &&
                    ((ne =
                      (Y = c.value) === null || Y === void 0 ? void 0 : (Z = Y.instance).update) ===
                      null ||
                      ne === void 0 ||
                      ne.call(Z))
                }),
            Ne(() => {
              G && G()
            }))
        },
        z = (H) => {
          ;(H.keyCode === 13 && o('pressEnter', H), o('keydown', H))
        },
        C = (H) => {
          const { onBlur: G } = e
          ;(G?.(H), a.onFieldBlur())
        },
        R = (H) => {
          ;(o('update:value', H.target.value), o('change', H), o('input', H), a.onFieldChange())
        },
        N = (H) => {
          ;(_r(c.value.textArea, H, R),
            E('', () => {
              $()
            }))
        },
        j = (H) => {
          let G = H.target.value
          if (u.value !== G) {
            if (p.value) {
              const Y = H.target,
                Z =
                  Y.selectionStart >= e.maxlength + 1 ||
                  Y.selectionStart === G.length ||
                  !Y.selectionStart
              G = Ap(Z, d.value, G, e.maxlength)
            }
            ;(_r(H.currentTarget, H, R, G), E(G))
          }
        },
        V = () => {
          var H, G
          const { class: Y } = n,
            { bordered: Z = !0 } = e,
            ne = D(D(D({}, dt(e, ['allowClear'])), n), {
              class: [
                {
                  [`${f.value}-borderless`]: !Z,
                  [`${Y}`]: Y && !y.value,
                  [`${f.value}-sm`]: h.value === 'small',
                  [`${f.value}-lg`]: h.value === 'large',
                },
                yr(f.value, l.value),
                v.value,
              ],
              disabled: b.value,
              showCount: null,
              prefixCls: f.value,
              onInput: j,
              onChange: j,
              onBlur: C,
              onKeydown: z,
              onCompositionstart: w,
              onCompositionend: T,
            })
          return (
            !((H = e.valueModifiers) === null || H === void 0) && H.lazy && delete ne.onInput,
            F(
              pI,
              oe(
                oe({}, ne),
                {},
                {
                  id: (G = ne?.id) !== null && G !== void 0 ? G : a.id.value,
                  ref: c,
                  maxlength: e.maxlength,
                  lazy: e.lazy,
                }
              ),
              null
            )
          )
        }
      return (
        r({ focus: $, blur: P, resizableTextArea: c }),
        Et(() => {
          let H = Ld(u.value)
          ;(!_.value &&
            p.value &&
            (e.value === null || e.value === void 0) &&
            (H = $w(H, e.maxlength)),
            (d.value = H))
        }),
        () => {
          var H
          const { maxlength: G, bordered: Y = !0, hidden: Z } = e,
            { style: ne, class: B } = n,
            L = D(D(D({}, e), n), {
              prefixCls: f.value,
              inputType: 'text',
              handleReset: N,
              direction: g.value,
              bordered: Y,
              style: y.value ? void 0 : ne,
              hashId: v.value,
              disabled: (H = e.disabled) !== null && H !== void 0 ? H : b.value,
            })
          let k = F(uI, oe(oe({}, L), {}, { value: d.value, status: e.status }), { element: V })
          if (y.value || s.hasFeedback) {
            const U = [...d.value].length
            let J = ''
            ;(typeof y.value == 'object'
              ? (J = y.value.formatter({ value: d.value, count: U, maxlength: G }))
              : (J = `${U}${p.value ? ` / ${G}` : ''}`),
              (k = F(
                'div',
                {
                  hidden: Z,
                  class: xe(
                    `${f.value}-textarea`,
                    {
                      [`${f.value}-textarea-rtl`]: g.value === 'rtl',
                      [`${f.value}-textarea-show-count`]: y.value,
                      [`${f.value}-textarea-in-form-item`]: s.isFormItemInput,
                    },
                    `${f.value}-textarea-show-count`,
                    B,
                    v.value
                  ),
                  style: ne,
                  'data-count': typeof J != 'object' ? J : void 0,
                },
                [
                  k,
                  s.hasFeedback &&
                    F('span', { class: `${f.value}-textarea-suffix` }, [s.feedbackIcon]),
                ]
              )))
          }
          return m(k)
        }
      )
    },
  })
  var gI = {
    icon: {
      tag: 'svg',
      attrs: { viewBox: '64 64 896 896', focusable: 'false' },
      children: [
        {
          tag: 'path',
          attrs: {
            d: 'M942.2 486.2C847.4 286.5 704.1 186 512 186c-192.2 0-335.4 100.5-430.2 300.3a60.3 60.3 0 000 51.5C176.6 737.5 319.9 838 512 838c192.2 0 335.4-100.5 430.2-300.3 7.7-16.2 7.7-35 0-51.5zM512 766c-161.3 0-279.4-81.8-362.7-254C232.6 339.8 350.7 258 512 258c161.3 0 279.4 81.8 362.7 254C791.5 684.2 673.4 766 512 766zm-4-430c-97.2 0-176 78.8-176 176s78.8 176 176 176 176-78.8 176-176-78.8-176-176-176zm0 288c-61.9 0-112-50.1-112-112s50.1-112 112-112 112 50.1 112 112-50.1 112-112 112z',
          },
        },
      ],
    },
    name: 'eye',
    theme: 'outlined',
  }
  function Np(e) {
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
          mI(e, o, n[o])
        }))
    }
    return e
  }
  function mI(e, t, n) {
    return (
      t in e
        ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
        : (e[t] = n),
      e
    )
  }
  var Of = function (t, n) {
    var r = Np({}, t, n.attrs)
    return F(kr, Np({}, r, { icon: gI }), null)
  }
  Of.displayName = 'EyeOutlined'
  Of.inheritAttrs = !1
  var yI = {
    icon: {
      tag: 'svg',
      attrs: { viewBox: '64 64 896 896', focusable: 'false' },
      children: [
        {
          tag: 'path',
          attrs: {
            d: 'M942.2 486.2Q889.47 375.11 816.7 305l-50.88 50.88C807.31 395.53 843.45 447.4 874.7 512 791.5 684.2 673.4 766 512 766q-72.67 0-133.87-22.38L323 798.75Q408 838 512 838q288.3 0 430.2-300.3a60.29 60.29 0 000-51.5zm-63.57-320.64L836 122.88a8 8 0 00-11.32 0L715.31 232.2Q624.86 186 512 186q-288.3 0-430.2 300.3a60.3 60.3 0 000 51.5q56.69 119.4 136.5 191.41L112.48 835a8 8 0 000 11.31L155.17 889a8 8 0 0011.31 0l712.15-712.12a8 8 0 000-11.32zM149.3 512C232.6 339.8 350.7 258 512 258c54.54 0 104.13 9.36 149.12 28.39l-70.3 70.3a176 176 0 00-238.13 238.13l-83.42 83.42C223.1 637.49 183.3 582.28 149.3 512zm246.7 0a112.11 112.11 0 01146.2-106.69L401.31 546.2A112 112 0 01396 512z',
          },
        },
        {
          tag: 'path',
          attrs: {
            d: 'M508 624c-3.46 0-6.87-.16-10.25-.47l-52.82 52.82a176.09 176.09 0 00227.42-227.42l-52.82 52.82c.31 3.38.47 6.79.47 10.25a111.94 111.94 0 01-112 112z',
          },
        },
      ],
    },
    name: 'eye-invisible',
    theme: 'outlined',
  }
  function Rp(e) {
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
          bI(e, o, n[o])
        }))
    }
    return e
  }
  function bI(e, t, n) {
    return (
      t in e
        ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
        : (e[t] = n),
      e
    )
  }
  var Pf = function (t, n) {
    var r = Rp({}, t, n.attrs)
    return F(kr, Rp({}, r, { icon: yI }), null)
  }
  Pf.displayName = 'EyeInvisibleOutlined'
  Pf.inheritAttrs = !1
  var _I = function (e, t) {
    var n = {}
    for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
    if (e != null && typeof Object.getOwnPropertySymbols == 'function')
      for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
        t.indexOf(r[o]) < 0 &&
          Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
          (n[r[o]] = e[r[o]])
    return n
  }
  const wI = { click: 'onClick', hover: 'onMouseover' },
    SI = (e) => (e ? F(Of, null, null) : F(Pf, null, null)),
    xI = te({
      compatConfig: { MODE: 3 },
      name: 'AInputPassword',
      inheritAttrs: !1,
      props: D(D({}, ai()), {
        prefixCls: String,
        inputPrefixCls: String,
        action: { type: String, default: 'click' },
        visibilityToggle: { type: Boolean, default: !0 },
        visible: { type: Boolean, default: void 0 },
        'onUpdate:visible': Function,
        iconRender: Function,
      }),
      setup(e, t) {
        let { slots: n, attrs: r, expose: o, emit: i } = t
        const a = ce(!1),
          s = () => {
            const { disabled: v } = e
            v || ((a.value = !a.value), i('update:visible', a.value))
          }
        Et(() => {
          e.visible !== void 0 && (a.value = !!e.visible)
        })
        const l = ce()
        o({
          focus: () => {
            var v
            ;(v = l.value) === null || v === void 0 || v.focus()
          },
          blur: () => {
            var v
            ;(v = l.value) === null || v === void 0 || v.blur()
          },
        })
        const d = (v) => {
            const { action: b, iconRender: y = n.iconRender || SI } = e,
              p = wI[b] || '',
              _ = y(a.value),
              x = {
                [p]: s,
                class: `${v}-icon`,
                key: 'passwordIcon',
                onMousedown: (S) => {
                  S.preventDefault()
                },
                onMouseup: (S) => {
                  S.preventDefault()
                },
              }
            return Ke(rf(_) ? _ : F('span', null, [_]), x)
          },
          { prefixCls: f, getPrefixCls: h } = Ge('input-password', e),
          g = X(() => h('input', e.inputPrefixCls)),
          m = () => {
            const { size: v, visibilityToggle: b } = e,
              y = _I(e, ['size', 'visibilityToggle']),
              p = b && d(f.value),
              _ = xe(f.value, r.class, { [`${f.value}-${v}`]: !!v }),
              x = D(D(D({}, dt(y, ['suffix', 'iconRender', 'action'])), r), {
                type: a.value ? 'text' : 'password',
                class: _,
                prefixCls: g.value,
                suffix: p,
              })
            return (v && (x.size = v), F(Fe, oe({ ref: l }, x), n))
          }
        return () => m()
      },
    })
  Fe.Group = oI
  Fe.Search = aI
  Fe.TextArea = vI
  Fe.Password = xI
  Fe.install = function (e) {
    return (
      e.component(Fe.name, Fe),
      e.component(Fe.Group.name, Fe.Group),
      e.component(Fe.Search.name, Fe.Search),
      e.component(Fe.TextArea.name, Fe.TextArea),
      e.component(Fe.Password.name, Fe.Password),
      e
    )
  }
  function If() {
    return {
      keyboard: { type: Boolean, default: void 0 },
      mask: { type: Boolean, default: void 0 },
      afterClose: Function,
      closable: { type: Boolean, default: void 0 },
      maskClosable: { type: Boolean, default: void 0 },
      visible: { type: Boolean, default: void 0 },
      destroyOnClose: { type: Boolean, default: void 0 },
      mousePosition: Q.shape({ x: Number, y: Number }).loose,
      title: Q.any,
      footer: Q.any,
      transitionName: String,
      maskTransitionName: String,
      animation: Q.any,
      maskAnimation: Q.any,
      wrapStyle: { type: Object, default: void 0 },
      bodyStyle: { type: Object, default: void 0 },
      maskStyle: { type: Object, default: void 0 },
      prefixCls: String,
      wrapClassName: String,
      rootClassName: String,
      width: [String, Number],
      height: [String, Number],
      zIndex: Number,
      bodyProps: Q.any,
      maskProps: Q.any,
      wrapProps: Q.any,
      getContainer: Q.any,
      dialogStyle: { type: Object, default: void 0 },
      dialogClass: String,
      closeIcon: Q.any,
      forceRender: { type: Boolean, default: void 0 },
      getOpenCount: Function,
      focusTriggerAfterClose: { type: Boolean, default: void 0 },
      onClose: Function,
      modalRender: Function,
    }
  }
  function Mp(e, t, n) {
    let r = t
    return (!r && n && (r = `${e}-${n}`), r)
  }
  let Dp = -1
  function CI() {
    return ((Dp += 1), Dp)
  }
  function Bp(e, t) {
    let n = e[`page${t ? 'Y' : 'X'}Offset`]
    const r = `scroll${t ? 'Top' : 'Left'}`
    if (typeof n != 'number') {
      const o = e.document
      ;((n = o.documentElement[r]), typeof n != 'number' && (n = o.body[r]))
    }
    return n
  }
  function EI(e) {
    const t = e.getBoundingClientRect(),
      n = { left: t.left, top: t.top },
      r = e.ownerDocument,
      o = r.defaultView || r.parentWindow
    return ((n.left += Bp(o)), (n.top += Bp(o, !0)), n)
  }
  const $I = { width: 0, height: 0, overflow: 'hidden', outline: 'none' },
    TI = { outline: 'none' },
    OI = te({
      compatConfig: { MODE: 3 },
      name: 'DialogContent',
      inheritAttrs: !1,
      props: D(D({}, If()), {
        motionName: String,
        ariaId: String,
        onVisibleChanged: Function,
        onMousedown: Function,
        onMouseup: Function,
      }),
      setup(e, t) {
        let { expose: n, slots: r, attrs: o } = t
        const i = de(),
          a = de(),
          s = de()
        n({
          focus: () => {
            var f
            ;(f = i.value) === null || f === void 0 || f.focus({ preventScroll: !0 })
          },
          changeActive: (f) => {
            const { activeElement: h } = document
            f && h === a.value
              ? i.value.focus({ preventScroll: !0 })
              : !f && h === i.value && a.value.focus({ preventScroll: !0 })
          },
        })
        const l = de(),
          u = X(() => {
            const { width: f, height: h } = e,
              g = {}
            return (
              f !== void 0 && (g.width = typeof f == 'number' ? `${f}px` : f),
              h !== void 0 && (g.height = typeof h == 'number' ? `${h}px` : h),
              l.value && (g.transformOrigin = l.value),
              g
            )
          }),
          c = () => {
            Ne(() => {
              if (s.value) {
                const f = EI(s.value)
                l.value = e.mousePosition
                  ? `${e.mousePosition.x - f.left}px ${e.mousePosition.y - f.top}px`
                  : ''
              }
            })
          },
          d = (f) => {
            e.onVisibleChanged(f)
          }
        return () => {
          var f, h, g, m
          const {
            prefixCls: v,
            footer: b = (f = r.footer) === null || f === void 0 ? void 0 : f.call(r),
            title: y = (h = r.title) === null || h === void 0 ? void 0 : h.call(r),
            ariaId: p,
            closable: _,
            closeIcon: x = (g = r.closeIcon) === null || g === void 0 ? void 0 : g.call(r),
            onClose: S,
            bodyStyle: w,
            bodyProps: T,
            onMousedown: A,
            onMouseup: $,
            visible: P,
            modalRender: E = r.modalRender,
            destroyOnClose: z,
            motionName: C,
          } = e
          let R
          b && (R = F('div', { class: `${v}-footer` }, [b]))
          let N
          y &&
            (N = F('div', { class: `${v}-header` }, [
              F('div', { class: `${v}-title`, id: p }, [y]),
            ]))
          let j
          _ &&
            (j = F(
              'button',
              { type: 'button', onClick: S, 'aria-label': 'Close', class: `${v}-close` },
              [x || F('span', { class: `${v}-close-x` }, null)]
            ))
          const V = F('div', { class: `${v}-content` }, [
              j,
              N,
              F('div', oe({ class: `${v}-body`, style: w }, T), [
                (m = r.default) === null || m === void 0 ? void 0 : m.call(r),
              ]),
              R,
            ]),
            H = nf(C)
          return F(
            Qt,
            oe(
              oe({}, H),
              {},
              { onBeforeEnter: c, onAfterEnter: () => d(!0), onAfterLeave: () => d(!1) }
            ),
            {
              default: () => [
                P || !z
                  ? Lr(
                      F(
                        'div',
                        oe(
                          oe({}, o),
                          {},
                          {
                            ref: s,
                            key: 'dialog-element',
                            role: 'document',
                            style: [u.value, o.style],
                            class: [v, o.class],
                            onMousedown: A,
                            onMouseup: $,
                          }
                        ),
                        [
                          F('div', { tabindex: 0, ref: i, style: TI }, [
                            E ? E({ originVNode: V }) : V,
                          ]),
                          F('div', { tabindex: 0, ref: a, style: $I }, null),
                        ]
                      ),
                      [[Qo, P]]
                    )
                  : null,
              ],
            }
          )
        }
      },
    }),
    PI = te({
      compatConfig: { MODE: 3 },
      name: 'DialogMask',
      props: { prefixCls: String, visible: Boolean, motionName: String, maskProps: Object },
      setup(e, t) {
        return () => {
          const { prefixCls: n, visible: r, maskProps: o, motionName: i } = e,
            a = nf(i)
          return F(Qt, a, {
            default: () => [Lr(F('div', oe({ class: `${n}-mask` }, o), null), [[Qo, r]])],
          })
        }
      },
    }),
    qp = te({
      compatConfig: { MODE: 3 },
      name: 'VcDialog',
      inheritAttrs: !1,
      props: tn(D(D({}, If()), { getOpenCount: Function, scrollLocker: Object }), {
        mask: !0,
        visible: !1,
        keyboard: !0,
        closable: !0,
        maskClosable: !0,
        destroyOnClose: !1,
        prefixCls: 'rc-dialog',
        getOpenCount: () => null,
        focusTriggerAfterClose: !0,
      }),
      setup(e, t) {
        let { attrs: n, slots: r } = t
        const o = ce(),
          i = ce(),
          a = ce(),
          s = ce(e.visible),
          l = ce(`vcDialogTitle${CI()}`),
          u = (b) => {
            var y, p
            if (b)
              un(i.value, document.activeElement) ||
                ((o.value = document.activeElement),
                (y = a.value) === null || y === void 0 || y.focus())
            else {
              const _ = s.value
              if (((s.value = !1), e.mask && o.value && e.focusTriggerAfterClose)) {
                try {
                  o.value.focus({ preventScroll: !0 })
                } catch {}
                o.value = null
              }
              _ && ((p = e.afterClose) === null || p === void 0 || p.call(e))
            }
          },
          c = (b) => {
            var y
            ;(y = e.onClose) === null || y === void 0 || y.call(e, b)
          },
          d = ce(!1),
          f = ce(),
          h = () => {
            ;(clearTimeout(f.value), (d.value = !0))
          },
          g = () => {
            f.value = setTimeout(() => {
              d.value = !1
            })
          },
          m = (b) => {
            if (!e.maskClosable) return null
            d.value ? (d.value = !1) : i.value === b.target && c(b)
          },
          v = (b) => {
            if (e.keyboard && b.keyCode === ip.ESC) {
              ;(b.stopPropagation(), c(b))
              return
            }
            e.visible && b.keyCode === ip.TAB && a.value.changeActive(!b.shiftKey)
          }
        return (
          me(
            () => e.visible,
            () => {
              e.visible && (s.value = !0)
            },
            { flush: 'post' }
          ),
          je(() => {
            var b
            ;(clearTimeout(f.value), (b = e.scrollLocker) === null || b === void 0 || b.unLock())
          }),
          Et(() => {
            var b, y
            ;((b = e.scrollLocker) === null || b === void 0 || b.unLock(),
              s.value && ((y = e.scrollLocker) === null || y === void 0 || y.lock()))
          }),
          () => {
            const {
                prefixCls: b,
                mask: y,
                visible: p,
                maskTransitionName: _,
                maskAnimation: x,
                zIndex: S,
                wrapClassName: w,
                rootClassName: T,
                wrapStyle: A,
                closable: $,
                maskProps: P,
                maskStyle: E,
                transitionName: z,
                animation: C,
                wrapProps: R,
                title: N = r.title,
              } = e,
              { style: j, class: V } = n
            return F('div', oe({ class: [`${b}-root`, T] }, XT(e, { data: !0 })), [
              F(
                PI,
                {
                  prefixCls: b,
                  visible: y && p,
                  motionName: Mp(b, _, x),
                  style: D({ zIndex: S }, E),
                  maskProps: P,
                },
                null
              ),
              F(
                'div',
                oe(
                  {
                    tabIndex: -1,
                    onKeydown: v,
                    class: xe(`${b}-wrap`, w),
                    ref: i,
                    onClick: m,
                    role: 'dialog',
                    'aria-labelledby': N ? l.value : null,
                    style: D(D({ zIndex: S }, A), { display: s.value ? null : 'none' }),
                  },
                  R
                ),
                [
                  F(
                    OI,
                    oe(
                      oe({}, dt(e, ['scrollLocker'])),
                      {},
                      {
                        style: j,
                        class: V,
                        onMousedown: h,
                        onMouseup: g,
                        ref: a,
                        closable: $,
                        ariaId: l.value,
                        prefixCls: b,
                        visible: p,
                        onClose: c,
                        onVisibleChanged: u,
                        motionName: Mp(b, z, C),
                      }
                    ),
                    r
                  ),
                ]
              ),
            ])
          }
        )
      },
    }),
    II = If(),
    AI = te({
      compatConfig: { MODE: 3 },
      name: 'DialogWrap',
      inheritAttrs: !1,
      props: tn(II, { visible: !1 }),
      setup(e, t) {
        let { attrs: n, slots: r } = t
        const o = de(e.visible)
        return (
          a_({}, { inTriggerContext: !1 }),
          me(
            () => e.visible,
            () => {
              e.visible && (o.value = !0)
            },
            { flush: 'post' }
          ),
          () => {
            const {
              visible: i,
              getContainer: a,
              forceRender: s,
              destroyOnClose: l = !1,
              afterClose: u,
            } = e
            let c = D(D(D({}, e), n), { ref: '_component', key: 'dialog' })
            return a === !1
              ? F(qp, oe(oe({}, c), {}, { getOpenCount: () => 2 }), r)
              : !s && l && !o.value
                ? null
                : F(
                    Z_,
                    { autoLock: !0, visible: i, forceRender: s, getContainer: a },
                    {
                      default: (d) => (
                        (c = D(D(D({}, c), d), {
                          afterClose: () => {
                            ;(u?.(), (o.value = !1))
                          },
                        })),
                        F(qp, c, r)
                      ),
                    }
                  )
          }
        )
      },
    })
  function zp(e) {
    return { position: e, top: 0, insetInlineEnd: 0, bottom: 0, insetInlineStart: 0 }
  }
  const NI = (e) => {
      const { componentCls: t } = e
      return [
        {
          [`${t}-root`]: {
            [`${t}${e.antCls}-zoom-enter, ${t}${e.antCls}-zoom-appear`]: {
              transform: 'none',
              opacity: 0,
              animationDuration: e.motionDurationSlow,
              userSelect: 'none',
            },
            [`${t}${e.antCls}-zoom-leave ${t}-content`]: { pointerEvents: 'none' },
            [`${t}-mask`]: D(D({}, zp('fixed')), {
              zIndex: e.zIndexPopupBase,
              height: '100%',
              backgroundColor: e.colorBgMask,
              [`${t}-hidden`]: { display: 'none' },
            }),
            [`${t}-wrap`]: D(D({}, zp('fixed')), {
              overflow: 'auto',
              outline: 0,
              WebkitOverflowScrolling: 'touch',
            }),
          },
        },
        { [`${t}-root`]: bO(e) },
      ]
    },
    RI = (e) => {
      const { componentCls: t } = e
      return [
        {
          [`${t}-root`]: {
            [`${t}-wrap`]: {
              zIndex: e.zIndexPopupBase,
              position: 'fixed',
              inset: 0,
              overflow: 'auto',
              outline: 0,
              WebkitOverflowScrolling: 'touch',
            },
            [`${t}-wrap-rtl`]: { direction: 'rtl' },
            [`${t}-centered`]: {
              textAlign: 'center',
              '&::before': {
                display: 'inline-block',
                width: 0,
                height: '100%',
                verticalAlign: 'middle',
                content: '""',
              },
              [t]: {
                top: 0,
                display: 'inline-block',
                paddingBottom: 0,
                textAlign: 'start',
                verticalAlign: 'middle',
              },
            },
            [`@media (max-width: ${e.screenSMMax})`]: {
              [t]: { maxWidth: 'calc(100vw - 16px)', margin: `${e.marginXS} auto` },
              [`${t}-centered`]: { [t]: { flex: 1 } },
            },
          },
        },
        {
          [t]: D(D({}, Kn(e)), {
            pointerEvents: 'none',
            position: 'relative',
            top: 100,
            width: 'auto',
            maxWidth: `calc(100vw - ${e.margin * 2}px)`,
            margin: '0 auto',
            paddingBottom: e.paddingLG,
            [`${t}-title`]: {
              margin: 0,
              color: e.modalHeadingColor,
              fontWeight: e.fontWeightStrong,
              fontSize: e.modalHeaderTitleFontSize,
              lineHeight: e.modalHeaderTitleLineHeight,
              wordWrap: 'break-word',
            },
            [`${t}-content`]: {
              position: 'relative',
              backgroundColor: e.modalContentBg,
              backgroundClip: 'padding-box',
              border: 0,
              borderRadius: e.borderRadiusLG,
              boxShadow: e.boxShadowSecondary,
              pointerEvents: 'auto',
              padding: `${e.paddingMD}px ${e.paddingContentHorizontalLG}px`,
            },
            [`${t}-close`]: D(
              {
                position: 'absolute',
                top: (e.modalHeaderCloseSize - e.modalCloseBtnSize) / 2,
                insetInlineEnd: (e.modalHeaderCloseSize - e.modalCloseBtnSize) / 2,
                zIndex: e.zIndexPopupBase + 10,
                padding: 0,
                color: e.modalCloseColor,
                fontWeight: e.fontWeightStrong,
                lineHeight: 1,
                textDecoration: 'none',
                background: 'transparent',
                borderRadius: e.borderRadiusSM,
                width: e.modalConfirmIconSize,
                height: e.modalConfirmIconSize,
                border: 0,
                outline: 0,
                cursor: 'pointer',
                transition: `color ${e.motionDurationMid}, background-color ${e.motionDurationMid}`,
                '&-x': {
                  display: 'block',
                  fontSize: e.fontSizeLG,
                  fontStyle: 'normal',
                  lineHeight: `${e.modalCloseBtnSize}px`,
                  textAlign: 'center',
                  textTransform: 'none',
                  textRendering: 'auto',
                },
                '&:hover': {
                  color: e.modalIconHoverColor,
                  backgroundColor: e.wireframe ? 'transparent' : e.colorFillContent,
                  textDecoration: 'none',
                },
                '&:active': {
                  backgroundColor: e.wireframe ? 'transparent' : e.colorFillContentHover,
                },
              },
              s_(e)
            ),
            [`${t}-header`]: {
              color: e.colorText,
              background: e.modalHeaderBg,
              borderRadius: `${e.borderRadiusLG}px ${e.borderRadiusLG}px 0 0`,
              marginBottom: e.marginXS,
            },
            [`${t}-body`]: {
              fontSize: e.fontSize,
              lineHeight: e.lineHeight,
              wordWrap: 'break-word',
            },
            [`${t}-footer`]: {
              textAlign: 'end',
              background: e.modalFooterBg,
              marginTop: e.marginSM,
              [`${e.antCls}-btn + ${e.antCls}-btn:not(${e.antCls}-dropdown-trigger)`]: {
                marginBottom: 0,
                marginInlineStart: e.marginXS,
              },
            },
            [`${t}-open`]: { overflow: 'hidden' },
          }),
        },
        {
          [`${t}-pure-panel`]: {
            top: 'auto',
            padding: 0,
            display: 'flex',
            flexDirection: 'column',
            [`${t}-content,
          ${t}-body,
          ${t}-confirm-body-wrapper`]: { display: 'flex', flexDirection: 'column', flex: 'auto' },
            [`${t}-confirm-body`]: { marginBottom: 'auto' },
          },
        },
      ]
    },
    MI = (e) => {
      const { componentCls: t } = e,
        n = `${t}-confirm`
      return {
        [n]: {
          '&-rtl': { direction: 'rtl' },
          [`${e.antCls}-modal-header`]: { display: 'none' },
          [`${n}-body-wrapper`]: D({}, l_()),
          [`${n}-body`]: {
            display: 'flex',
            flexWrap: 'wrap',
            alignItems: 'center',
            [`${n}-title`]: {
              flex: '0 0 100%',
              display: 'block',
              overflow: 'hidden',
              color: e.colorTextHeading,
              fontWeight: e.fontWeightStrong,
              fontSize: e.modalHeaderTitleFontSize,
              lineHeight: e.modalHeaderTitleLineHeight,
              [`+ ${n}-content`]: {
                marginBlockStart: e.marginXS,
                flexBasis: '100%',
                maxWidth: `calc(100% - ${e.modalConfirmIconSize + e.marginSM}px)`,
              },
            },
            [`${n}-content`]: { color: e.colorText, fontSize: e.fontSize },
            [`> ${e.iconCls}`]: {
              flex: 'none',
              marginInlineEnd: e.marginSM,
              fontSize: e.modalConfirmIconSize,
              [`+ ${n}-title`]: { flex: 1 },
              [`+ ${n}-title + ${n}-content`]: {
                marginInlineStart: e.modalConfirmIconSize + e.marginSM,
              },
            },
          },
          [`${n}-btns`]: {
            textAlign: 'end',
            marginTop: e.marginSM,
            [`${e.antCls}-btn + ${e.antCls}-btn`]: {
              marginBottom: 0,
              marginInlineStart: e.marginXS,
            },
          },
        },
        [`${n}-error ${n}-body > ${e.iconCls}`]: { color: e.colorError },
        [`${n}-warning ${n}-body > ${e.iconCls},
        ${n}-confirm ${n}-body > ${e.iconCls}`]: { color: e.colorWarning },
        [`${n}-info ${n}-body > ${e.iconCls}`]: { color: e.colorInfo },
        [`${n}-success ${n}-body > ${e.iconCls}`]: { color: e.colorSuccess },
        [`${t}-zoom-leave ${t}-btns`]: { pointerEvents: 'none' },
      }
    },
    DI = (e) => {
      const { componentCls: t } = e
      return {
        [`${t}-root`]: {
          [`${t}-wrap-rtl`]: { direction: 'rtl', [`${t}-confirm-body`]: { direction: 'rtl' } },
        },
      }
    },
    BI = (e) => {
      const { componentCls: t, antCls: n } = e,
        r = `${t}-confirm`
      return {
        [t]: {
          [`${t}-content`]: { padding: 0 },
          [`${t}-header`]: {
            padding: e.modalHeaderPadding,
            borderBottom: `${e.modalHeaderBorderWidth}px ${e.modalHeaderBorderStyle} ${e.modalHeaderBorderColorSplit}`,
            marginBottom: 0,
          },
          [`${t}-body`]: { padding: e.modalBodyPadding },
          [`${t}-footer`]: {
            padding: `${e.modalFooterPaddingVertical}px ${e.modalFooterPaddingHorizontal}px`,
            borderTop: `${e.modalFooterBorderWidth}px ${e.modalFooterBorderStyle} ${e.modalFooterBorderColorSplit}`,
            borderRadius: `0 0 ${e.borderRadiusLG}px ${e.borderRadiusLG}px`,
            marginTop: 0,
          },
        },
        [r]: {
          [`${n}-modal-body`]: {
            padding: `${e.padding * 2}px ${e.padding * 2}px ${e.paddingLG}px`,
          },
          [`${r}-body`]: {
            [`> ${e.iconCls}`]: {
              marginInlineEnd: e.margin,
              [`+ ${r}-title + ${r}-content`]: {
                marginInlineStart: e.modalConfirmIconSize + e.margin,
              },
            },
          },
          [`${r}-btns`]: { marginTop: e.marginLG },
        },
      }
    },
    qI = en('Modal', (e) => {
      const t = e.padding,
        n = e.fontSizeHeading5,
        r = e.lineHeightHeading5,
        o = ot(e, {
          modalBodyPadding: e.paddingLG,
          modalHeaderBg: e.colorBgElevated,
          modalHeaderPadding: `${t}px ${e.paddingLG}px`,
          modalHeaderBorderWidth: e.lineWidth,
          modalHeaderBorderStyle: e.lineType,
          modalHeaderTitleLineHeight: r,
          modalHeaderTitleFontSize: n,
          modalHeaderBorderColorSplit: e.colorSplit,
          modalHeaderCloseSize: r * n + t * 2,
          modalContentBg: e.colorBgElevated,
          modalHeadingColor: e.colorTextHeading,
          modalCloseColor: e.colorTextDescription,
          modalFooterBg: 'transparent',
          modalFooterBorderColorSplit: e.colorSplit,
          modalFooterBorderStyle: e.lineType,
          modalFooterPaddingVertical: e.paddingXS,
          modalFooterPaddingHorizontal: e.padding,
          modalFooterBorderWidth: e.lineWidth,
          modalConfirmTitleFontSize: e.fontSizeLG,
          modalIconHoverColor: e.colorIconHover,
          modalConfirmIconSize: e.fontSize * e.lineHeight,
          modalCloseBtnSize: e.controlHeightLG * 0.55,
        })
      return [RI(o), MI(o), DI(o), NI(o), e.wireframe && BI(o), ow(o, 'zoom')]
    })
  var zI = function (e, t) {
    var n = {}
    for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r])
    if (e != null && typeof Object.getOwnPropertySymbols == 'function')
      for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
        t.indexOf(r[o]) < 0 &&
          Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
          (n[r[o]] = e[r[o]])
    return n
  }
  let Fd
  const LI = (e) => {
    ;((Fd = { x: e.pageX, y: e.pageY }), setTimeout(() => (Fd = null), 100))
  }
  YP() && Rn(document.documentElement, 'click', LI, !0)
  const FI = () => ({
      prefixCls: String,
      visible: { type: Boolean, default: void 0 },
      open: { type: Boolean, default: void 0 },
      confirmLoading: { type: Boolean, default: void 0 },
      title: Q.any,
      closable: { type: Boolean, default: void 0 },
      closeIcon: Q.any,
      onOk: Function,
      onCancel: Function,
      'onUpdate:visible': Function,
      'onUpdate:open': Function,
      onChange: Function,
      afterClose: Function,
      centered: { type: Boolean, default: void 0 },
      width: [String, Number],
      footer: Q.any,
      okText: Q.any,
      okType: String,
      cancelText: Q.any,
      icon: Q.any,
      maskClosable: { type: Boolean, default: void 0 },
      forceRender: { type: Boolean, default: void 0 },
      okButtonProps: st(),
      cancelButtonProps: st(),
      destroyOnClose: { type: Boolean, default: void 0 },
      wrapClassName: String,
      maskTransitionName: String,
      transitionName: String,
      getContainer: { type: [String, Function, Boolean, Object], default: void 0 },
      zIndex: Number,
      bodyStyle: st(),
      maskStyle: st(),
      mask: { type: Boolean, default: void 0 },
      keyboard: { type: Boolean, default: void 0 },
      wrapProps: Object,
      focusTriggerAfterClose: { type: Boolean, default: void 0 },
      modalRender: Function,
      mousePosition: st(),
    }),
    Ze = te({
      compatConfig: { MODE: 3 },
      name: 'AModal',
      inheritAttrs: !1,
      props: tn(FI(), { width: 520, confirmLoading: !1, okType: 'primary' }),
      setup(e, t) {
        let { emit: n, slots: r, attrs: o } = t
        const [i] = sf('Modal'),
          { prefixCls: a, rootPrefixCls: s, direction: l, getPopupContainer: u } = Ge('modal', e),
          [c, d] = qI(a)
        tf(e.visible === void 0)
        const f = (m) => {
            ;(n('update:visible', !1), n('update:open', !1), n('cancel', m), n('change', !1))
          },
          h = (m) => {
            n('ok', m)
          },
          g = () => {
            var m, v
            const {
              okText: b = (m = r.okText) === null || m === void 0 ? void 0 : m.call(r),
              okType: y,
              cancelText: p = (v = r.cancelText) === null || v === void 0 ? void 0 : v.call(r),
              confirmLoading: _,
            } = e
            return F(Re, null, [
              F(_t, oe({ onClick: f }, e.cancelButtonProps), {
                default: () => [p || i.value.cancelText],
              }),
              F(_t, oe(oe({}, dw(y)), {}, { loading: _, onClick: h }, e.okButtonProps), {
                default: () => [b || i.value.okText],
              }),
            ])
          }
        return () => {
          var m, v
          const {
              prefixCls: b,
              visible: y,
              open: p,
              wrapClassName: _,
              centered: x,
              getContainer: S,
              closeIcon: w = (m = r.closeIcon) === null || m === void 0 ? void 0 : m.call(r),
              focusTriggerAfterClose: T = !0,
            } = e,
            A = zI(e, [
              'prefixCls',
              'visible',
              'open',
              'wrapClassName',
              'centered',
              'getContainer',
              'closeIcon',
              'focusTriggerAfterClose',
            ]),
            $ = xe(_, { [`${a.value}-centered`]: !!x, [`${a.value}-wrap-rtl`]: l.value === 'rtl' })
          return c(
            F(
              AI,
              oe(
                oe(oe({}, A), o),
                {},
                {
                  rootClassName: d.value,
                  class: xe(d.value, o.class),
                  getContainer: S || u?.value,
                  prefixCls: a.value,
                  wrapClassName: $,
                  visible: p ?? y,
                  onClose: f,
                  focusTriggerAfterClose: T,
                  transitionName: Er(s.value, 'zoom', e.transitionName),
                  maskTransitionName: Er(s.value, 'fade', e.maskTransitionName),
                  mousePosition: (v = A.mousePosition) !== null && v !== void 0 ? v : Fd,
                }
              ),
              D(D({}, r), {
                footer: r.footer || g,
                closeIcon: () =>
                  F('span', { class: `${a.value}-close-x` }, [
                    w || F(u_, { class: `${a.value}-close-icon` }, null),
                  ]),
              })
            )
          )
        }
      },
    }),
    kI = () => {
      const e = ce(!1)
      return (
        je(() => {
          e.value = !0
        }),
        e
      )
    },
    HI = {
      type: { type: String },
      actionFn: Function,
      close: Function,
      autofocus: Boolean,
      prefixCls: String,
      buttonProps: st(),
      emitEvent: Boolean,
      quitOnNullishReturnValue: Boolean,
    }
  function Lp(e) {
    return !!(e && e.then)
  }
  const Fp = te({
    compatConfig: { MODE: 3 },
    name: 'ActionButton',
    props: HI,
    setup(e, t) {
      let { slots: n } = t
      const r = ce(!1),
        o = ce(),
        i = ce(!1)
      let a
      const s = kI()
      ;(Me(() => {
        e.autofocus &&
          (a = setTimeout(() => {
            var d, f
            return (f = (d = At(o.value)) === null || d === void 0 ? void 0 : d.focus) === null ||
              f === void 0
              ? void 0
              : f.call(d)
          }))
      }),
        je(() => {
          clearTimeout(a)
        }))
      const l = function () {
          for (var d, f = arguments.length, h = new Array(f), g = 0; g < f; g++) h[g] = arguments[g]
          ;(d = e.close) === null || d === void 0 || d.call(e, ...h)
        },
        u = (d) => {
          Lp(d) &&
            ((i.value = !0),
            d.then(
              function () {
                ;(s.value || (i.value = !1), l(...arguments), (r.value = !1))
              },
              (f) => (s.value || (i.value = !1), (r.value = !1), Promise.reject(f))
            ))
        },
        c = (d) => {
          const { actionFn: f } = e
          if (r.value) return
          if (((r.value = !0), !f)) {
            l()
            return
          }
          let h
          if (e.emitEvent) {
            if (((h = f(d)), e.quitOnNullishReturnValue && !Lp(h))) {
              ;((r.value = !1), l(d))
              return
            }
          } else if (f.length) ((h = f(e.close)), (r.value = !1))
          else if (((h = f()), !h)) {
            l()
            return
          }
          u(h)
        }
      return () => {
        const { type: d, prefixCls: f, buttonProps: h } = e
        return F(
          _t,
          oe(
            oe(oe({}, dw(d)), {}, { onClick: c, loading: i.value, prefixCls: f }, h),
            {},
            { ref: o }
          ),
          n
        )
      }
    },
  })
  function In(e) {
    return typeof e == 'function' ? e() : e
  }
  const Tw = te({
      name: 'ConfirmDialog',
      inheritAttrs: !1,
      props: [
        'icon',
        'onCancel',
        'onOk',
        'close',
        'closable',
        'zIndex',
        'afterClose',
        'visible',
        'open',
        'keyboard',
        'centered',
        'getContainer',
        'maskStyle',
        'okButtonProps',
        'cancelButtonProps',
        'okType',
        'prefixCls',
        'okCancel',
        'width',
        'mask',
        'maskClosable',
        'okText',
        'cancelText',
        'autoFocusButton',
        'transitionName',
        'maskTransitionName',
        'type',
        'title',
        'content',
        'direction',
        'rootPrefixCls',
        'bodyStyle',
        'closeIcon',
        'modalRender',
        'focusTriggerAfterClose',
        'wrapClassName',
        'confirmPrefixCls',
        'footer',
      ],
      setup(e, t) {
        let { attrs: n } = t
        const [r] = sf('Modal')
        return () => {
          const {
            icon: o,
            onCancel: i,
            onOk: a,
            close: s,
            okText: l,
            closable: u = !1,
            zIndex: c,
            afterClose: d,
            keyboard: f,
            centered: h,
            getContainer: g,
            maskStyle: m,
            okButtonProps: v,
            cancelButtonProps: b,
            okCancel: y,
            width: p = 416,
            mask: _ = !0,
            maskClosable: x = !1,
            type: S,
            open: w,
            title: T,
            content: A,
            direction: $,
            closeIcon: P,
            modalRender: E,
            focusTriggerAfterClose: z,
            rootPrefixCls: C,
            bodyStyle: R,
            wrapClassName: N,
            footer: j,
          } = e
          let V = o
          if (!o && o !== null)
            switch (S) {
              case 'info':
                V = F(hx, null, null)
                break
              case 'success':
                V = F(fx, null, null)
                break
              case 'error':
                V = F(af, null, null)
                break
              default:
                V = F(dx, null, null)
            }
          const H = e.okType || 'primary',
            G = e.prefixCls || 'ant-modal',
            Y = `${G}-confirm`,
            Z = n.style || {},
            ne = y ?? S === 'confirm',
            B = e.autoFocusButton === null ? !1 : e.autoFocusButton || 'ok',
            L = `${G}-confirm`,
            k = xe(L, `${L}-${e.type}`, { [`${L}-rtl`]: $ === 'rtl' }, n.class),
            U = r.value,
            J =
              ne &&
              F(
                Fp,
                {
                  actionFn: i,
                  close: s,
                  autofocus: B === 'cancel',
                  buttonProps: b,
                  prefixCls: `${C}-btn`,
                },
                { default: () => [In(e.cancelText) || U.cancelText] }
              )
          return F(
            Ze,
            {
              prefixCls: G,
              class: k,
              wrapClassName: xe({ [`${L}-centered`]: !!h }, N),
              onCancel: (re) => s?.({ triggerCancel: !0 }, re),
              open: w,
              title: '',
              footer: '',
              transitionName: Er(C, 'zoom', e.transitionName),
              maskTransitionName: Er(C, 'fade', e.maskTransitionName),
              mask: _,
              maskClosable: x,
              maskStyle: m,
              style: Z,
              bodyStyle: R,
              width: p,
              zIndex: c,
              afterClose: d,
              keyboard: f,
              centered: h,
              getContainer: g,
              closable: u,
              closeIcon: P,
              modalRender: E,
              focusTriggerAfterClose: z,
            },
            {
              default: () => [
                F('div', { class: `${Y}-body-wrapper` }, [
                  F('div', { class: `${Y}-body` }, [
                    In(V),
                    T === void 0 ? null : F('span', { class: `${Y}-title` }, [In(T)]),
                    F('div', { class: `${Y}-content` }, [In(A)]),
                  ]),
                  j !== void 0
                    ? In(j)
                    : F('div', { class: `${Y}-btns` }, [
                        J,
                        F(
                          Fp,
                          {
                            type: H,
                            actionFn: a,
                            close: s,
                            autofocus: B === 'ok',
                            buttonProps: v,
                            prefixCls: `${C}-btn`,
                          },
                          { default: () => [In(l) || (ne ? U.okText : U.justOkText)] }
                        ),
                      ]),
                ]),
              ],
            }
          )
        }
      },
    }),
    hn = [],
    jr = (e) => {
      const t = document.createDocumentFragment()
      let n = D(D({}, dt(e, ['parentContext', 'appContext'])), { close: i, open: !0 }),
        r = null
      function o() {
        r && (Ln(null, t), (r = null))
        for (var u = arguments.length, c = new Array(u), d = 0; d < u; d++) c[d] = arguments[d]
        const f = c.some((h) => h && h.triggerCancel)
        e.onCancel && f && e.onCancel(() => {}, ...c.slice(1))
        for (let h = 0; h < hn.length; h++)
          if (hn[h] === i) {
            hn.splice(h, 1)
            break
          }
      }
      function i() {
        for (var u = arguments.length, c = new Array(u), d = 0; d < u; d++) c[d] = arguments[d]
        ;((n = D(D({}, n), {
          open: !1,
          afterClose: () => {
            ;(typeof e.afterClose == 'function' && e.afterClose(), o.apply(this, c))
          },
        })),
          n.visible && delete n.visible,
          a(n))
      }
      function a(u) {
        ;(typeof u == 'function' ? (n = u(n)) : (n = D(D({}, n), u)), r && kC(r, n, t))
      }
      const s = (u) => {
        const c = px,
          d = c.prefixCls,
          f = u.prefixCls || `${d}-modal`,
          h = c.iconPrefixCls,
          g = vx()
        return F(gx, oe(oe({}, c), {}, { prefixCls: d }), {
          default: () => [
            F(
              Tw,
              oe(
                oe({}, u),
                {},
                {
                  rootPrefixCls: d,
                  prefixCls: f,
                  iconPrefixCls: h,
                  locale: g,
                  cancelText: u.cancelText || g.cancelText,
                }
              ),
              null
            ),
          ],
        })
      }
      function l(u) {
        const c = F(s, D({}, u))
        return ((c.appContext = e.parentContext || e.appContext || c.appContext), Ln(c, t), c)
      }
      return ((r = l(n)), hn.push(i), { destroy: i, update: a })
    }
  function Ow(e) {
    return D(D({}, e), { type: 'warning' })
  }
  function Pw(e) {
    return D(D({}, e), { type: 'info' })
  }
  function Iw(e) {
    return D(D({}, e), { type: 'success' })
  }
  function Aw(e) {
    return D(D({}, e), { type: 'error' })
  }
  function Nw(e) {
    return D(D({}, e), { type: 'confirm' })
  }
  const jI = () => ({
      config: Object,
      afterClose: Function,
      destroyAction: Function,
      open: Boolean,
    }),
    VI = te({
      name: 'HookModal',
      inheritAttrs: !1,
      props: tn(jI(), { config: { width: 520, okType: 'primary' } }),
      setup(e, t) {
        let { expose: n } = t
        var r
        const o = X(() => e.open),
          i = X(() => e.config),
          { direction: a, getPrefixCls: s } = mx(),
          l = s('modal'),
          u = s(),
          c = () => {
            var g, m
            ;(e?.afterClose(), (m = (g = i.value).afterClose) === null || m === void 0 || m.call(g))
          },
          d = function () {
            e.destroyAction(...arguments)
          }
        n({ destroy: d })
        const f = (r = i.value.okCancel) !== null && r !== void 0 ? r : i.value.type === 'confirm',
          [h] = sf('Modal', yx.Modal)
        return () =>
          F(
            Tw,
            oe(
              oe({ prefixCls: l, rootPrefixCls: u }, i.value),
              {},
              {
                close: d,
                open: o.value,
                afterClose: c,
                okText: i.value.okText || (f ? h?.value.okText : h?.value.justOkText),
                direction: i.value.direction || a.value,
                cancelText: i.value.cancelText || h?.value.cancelText,
              }
            ),
            null
          )
      },
    })
  let kp = 0
  const GI = te({
    name: 'ElementsHolder',
    inheritAttrs: !1,
    setup(e, t) {
      let { expose: n } = t
      const r = ce([])
      return (
        n({
          addModal: (i) => (
            r.value.push(i),
            (r.value = r.value.slice()),
            () => {
              r.value = r.value.filter((a) => a !== i)
            }
          ),
        }),
        () => r.value.map((i) => i())
      )
    },
  })
  function WI() {
    const e = ce(null),
      t = ce([])
    me(
      t,
      () => {
        t.value.length &&
          ([...t.value].forEach((a) => {
            a()
          }),
          (t.value = []))
      },
      { immediate: !0 }
    )
    const n = (i) =>
        function (s) {
          var l
          kp += 1
          const u = ce(!0),
            c = ce(null),
            d = ce(K(s)),
            f = ce({})
          me(
            () => s,
            (p) => {
              v(D(D({}, ei(p) ? p.value : p), f.value))
            }
          )
          const h = function () {
            u.value = !1
            for (var p = arguments.length, _ = new Array(p), x = 0; x < p; x++) _[x] = arguments[x]
            const S = _.some((w) => w && w.triggerCancel)
            d.value.onCancel && S && d.value.onCancel(() => {}, ..._.slice(1))
          }
          let g
          const m = () =>
            F(
              VI,
              {
                key: `modal-${kp}`,
                config: i(d.value),
                ref: c,
                open: u.value,
                destroyAction: h,
                afterClose: () => {
                  g?.()
                },
              },
              null
            )
          ;((g = (l = e.value) === null || l === void 0 ? void 0 : l.addModal(m)), g && hn.push(g))
          const v = (p) => {
            d.value = D(D({}, d.value), p)
          }
          return {
            destroy: () => {
              c.value ? h() : (t.value = [...t.value, h])
            },
            update: (p) => {
              ;((f.value = p), c.value ? v(p) : (t.value = [...t.value, () => v(p)]))
            },
          }
        },
      r = X(() => ({ info: n(Pw), success: n(Iw), error: n(Aw), warning: n(Ow), confirm: n(Nw) })),
      o = Symbol('modalHolderKey')
    return [r.value, () => F(GI, { key: o, ref: e }, null)]
  }
  function Rw(e) {
    return jr(Ow(e))
  }
  Ze.useModal = WI
  Ze.info = function (t) {
    return jr(Pw(t))
  }
  Ze.success = function (t) {
    return jr(Iw(t))
  }
  Ze.error = function (t) {
    return jr(Aw(t))
  }
  Ze.warning = Rw
  Ze.warn = Rw
  Ze.confirm = function (t) {
    return jr(Nw(t))
  }
  Ze.destroyAll = function () {
    for (; hn.length; ) {
      const t = hn.pop()
      t && t()
    }
  }
  Ze.install = function (e) {
    return (e.component(Ze.name, Ze), e)
  }
  var UI = {
    icon: {
      tag: 'svg',
      attrs: { viewBox: '64 64 896 896', focusable: 'false' },
      children: [
        {
          tag: 'path',
          attrs: {
            d: 'M924.8 625.7l-65.5-56c3.1-19 4.7-38.4 4.7-57.8s-1.6-38.8-4.7-57.8l65.5-56a32.03 32.03 0 009.3-35.2l-.9-2.6a443.74 443.74 0 00-79.7-137.9l-1.8-2.1a32.12 32.12 0 00-35.1-9.5l-81.3 28.9c-30-24.6-63.5-44-99.7-57.6l-15.7-85a32.05 32.05 0 00-25.8-25.7l-2.7-.5c-52.1-9.4-106.9-9.4-159 0l-2.7.5a32.05 32.05 0 00-25.8 25.7l-15.8 85.4a351.86 351.86 0 00-99 57.4l-81.9-29.1a32 32 0 00-35.1 9.5l-1.8 2.1a446.02 446.02 0 00-79.7 137.9l-.9 2.6c-4.5 12.5-.8 26.5 9.3 35.2l66.3 56.6c-3.1 18.8-4.6 38-4.6 57.1 0 19.2 1.5 38.4 4.6 57.1L99 625.5a32.03 32.03 0 00-9.3 35.2l.9 2.6c18.1 50.4 44.9 96.9 79.7 137.9l1.8 2.1a32.12 32.12 0 0035.1 9.5l81.9-29.1c29.8 24.5 63.1 43.9 99 57.4l15.8 85.4a32.05 32.05 0 0025.8 25.7l2.7.5a449.4 449.4 0 00159 0l2.7-.5a32.05 32.05 0 0025.8-25.7l15.7-85a350 350 0 0099.7-57.6l81.3 28.9a32 32 0 0035.1-9.5l1.8-2.1c34.8-41.1 61.6-87.5 79.7-137.9l.9-2.6c4.5-12.3.8-26.3-9.3-35zM788.3 465.9c2.5 15.1 3.8 30.6 3.8 46.1s-1.3 31-3.8 46.1l-6.6 40.1 74.7 63.9a370.03 370.03 0 01-42.6 73.6L721 702.8l-31.4 25.8c-23.9 19.6-50.5 35-79.3 45.8l-38.1 14.3-17.9 97a377.5 377.5 0 01-85 0l-17.9-97.2-37.8-14.5c-28.5-10.8-55-26.2-78.7-45.7l-31.4-25.9-93.4 33.2c-17-22.9-31.2-47.6-42.6-73.6l75.5-64.5-6.5-40c-2.4-14.9-3.7-30.3-3.7-45.5 0-15.3 1.2-30.6 3.7-45.5l6.5-40-75.5-64.5c11.3-26.1 25.6-50.7 42.6-73.6l93.4 33.2 31.4-25.9c23.7-19.5 50.2-34.9 78.7-45.7l37.9-14.3 17.9-97.2c28.1-3.2 56.8-3.2 85 0l17.9 97 38.1 14.3c28.7 10.8 55.4 26.2 79.3 45.8l31.4 25.8 92.8-32.9c17 22.9 31.2 47.6 42.6 73.6L781.8 426l6.5 39.9zM512 326c-97.2 0-176 78.8-176 176s78.8 176 176 176 176-78.8 176-176-78.8-176-176-176zm79.2 255.2A111.6 111.6 0 01512 614c-29.9 0-58-11.7-79.2-32.8A111.6 111.6 0 01400 502c0-29.9 11.7-58 32.8-79.2C454 401.6 482.1 390 512 390c29.9 0 58 11.6 79.2 32.8A111.6 111.6 0 01624 502c0 29.9-11.7 58-32.8 79.2z',
          },
        },
      ],
    },
    name: 'setting',
    theme: 'outlined',
  }
  function Hp(e) {
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
          YI(e, o, n[o])
        }))
    }
    return e
  }
  function YI(e, t, n) {
    return (
      t in e
        ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 })
        : (e[t] = n),
      e
    )
  }
  var Af = function (t, n) {
    var r = Hp({}, t, n.attrs)
    return F(kr, Hp({}, r, { icon: UI }), null)
  }
  Af.displayName = 'SettingOutlined'
  Af.inheritAttrs = !1
  function Nf(e) {
    throw new Error(
      'Could not dynamically require "' +
        e +
        '". Please configure the dynamicRequireTargets or/and ignoreDynamicRequires option of @rollup/plugin-commonjs appropriately for this require call to work.'
    )
  }
  var Ki, jp
  function XI() {
    if (jp) return Ki
    jp = 1
    function e() {
      ;((this.__data__ = []), (this.size = 0))
    }
    return ((Ki = e), Ki)
  }
  var Zi, Vp
  function Qn() {
    if (Vp) return Zi
    Vp = 1
    function e(t, n) {
      return t === n || (t !== t && n !== n)
    }
    return ((Zi = e), Zi)
  }
  var Ji, Gp
  function si() {
    if (Gp) return Ji
    Gp = 1
    var e = Qn()
    function t(n, r) {
      for (var o = n.length; o--; ) if (e(n[o][0], r)) return o
      return -1
    }
    return ((Ji = t), Ji)
  }
  var Qi, Wp
  function KI() {
    if (Wp) return Qi
    Wp = 1
    var e = si(),
      t = Array.prototype,
      n = t.splice
    function r(o) {
      var i = this.__data__,
        a = e(i, o)
      if (a < 0) return !1
      var s = i.length - 1
      return (a == s ? i.pop() : n.call(i, a, 1), --this.size, !0)
    }
    return ((Qi = r), Qi)
  }
  var ea, Up
  function ZI() {
    if (Up) return ea
    Up = 1
    var e = si()
    function t(n) {
      var r = this.__data__,
        o = e(r, n)
      return o < 0 ? void 0 : r[o][1]
    }
    return ((ea = t), ea)
  }
  var ta, Yp
  function JI() {
    if (Yp) return ta
    Yp = 1
    var e = si()
    function t(n) {
      return e(this.__data__, n) > -1
    }
    return ((ta = t), ta)
  }
  var na, Xp
  function QI() {
    if (Xp) return na
    Xp = 1
    var e = si()
    function t(n, r) {
      var o = this.__data__,
        i = e(o, n)
      return (i < 0 ? (++this.size, o.push([n, r])) : (o[i][1] = r), this)
    }
    return ((na = t), na)
  }
  var ra, Kp
  function li() {
    if (Kp) return ra
    Kp = 1
    var e = XI(),
      t = KI(),
      n = ZI(),
      r = JI(),
      o = QI()
    function i(a) {
      var s = -1,
        l = a == null ? 0 : a.length
      for (this.clear(); ++s < l; ) {
        var u = a[s]
        this.set(u[0], u[1])
      }
    }
    return (
      (i.prototype.clear = e),
      (i.prototype.delete = t),
      (i.prototype.get = n),
      (i.prototype.has = r),
      (i.prototype.set = o),
      (ra = i),
      ra
    )
  }
  var oa, Zp
  function eA() {
    if (Zp) return oa
    Zp = 1
    var e = li()
    function t() {
      ;((this.__data__ = new e()), (this.size = 0))
    }
    return ((oa = t), oa)
  }
  var ia, Jp
  function tA() {
    if (Jp) return ia
    Jp = 1
    function e(t) {
      var n = this.__data__,
        r = n.delete(t)
      return ((this.size = n.size), r)
    }
    return ((ia = e), ia)
  }
  var aa, Qp
  function nA() {
    if (Qp) return aa
    Qp = 1
    function e(t) {
      return this.__data__.get(t)
    }
    return ((aa = e), aa)
  }
  var sa, ev
  function rA() {
    if (ev) return sa
    ev = 1
    function e(t) {
      return this.__data__.has(t)
    }
    return ((sa = e), sa)
  }
  var la, tv
  function Mw() {
    if (tv) return la
    tv = 1
    var e = typeof Qr == 'object' && Qr && Qr.Object === Object && Qr
    return ((la = e), la)
  }
  var ua, nv
  function ht() {
    if (nv) return ua
    nv = 1
    var e = Mw(),
      t = typeof self == 'object' && self && self.Object === Object && self,
      n = e || t || Function('return this')()
    return ((ua = n), ua)
  }
  var ca, rv
  function er() {
    if (rv) return ca
    rv = 1
    var e = ht(),
      t = e.Symbol
    return ((ca = t), ca)
  }
  var da, ov
  function oA() {
    if (ov) return da
    ov = 1
    var e = er(),
      t = Object.prototype,
      n = t.hasOwnProperty,
      r = t.toString,
      o = e ? e.toStringTag : void 0
    function i(a) {
      var s = n.call(a, o),
        l = a[o]
      try {
        a[o] = void 0
        var u = !0
      } catch {}
      var c = r.call(a)
      return (u && (s ? (a[o] = l) : delete a[o]), c)
    }
    return ((da = i), da)
  }
  var fa, iv
  function iA() {
    if (iv) return fa
    iv = 1
    var e = Object.prototype,
      t = e.toString
    function n(r) {
      return t.call(r)
    }
    return ((fa = n), fa)
  }
  var ha, av
  function $n() {
    if (av) return ha
    av = 1
    var e = er(),
      t = oA(),
      n = iA(),
      r = '[object Null]',
      o = '[object Undefined]',
      i = e ? e.toStringTag : void 0
    function a(s) {
      return s == null ? (s === void 0 ? o : r) : i && i in Object(s) ? t(s) : n(s)
    }
    return ((ha = a), ha)
  }
  var pa, sv
  function it() {
    if (sv) return pa
    sv = 1
    function e(t) {
      var n = typeof t
      return t != null && (n == 'object' || n == 'function')
    }
    return ((pa = e), pa)
  }
  var va, lv
  function Vr() {
    if (lv) return va
    lv = 1
    var e = $n(),
      t = it(),
      n = '[object AsyncFunction]',
      r = '[object Function]',
      o = '[object GeneratorFunction]',
      i = '[object Proxy]'
    function a(s) {
      if (!t(s)) return !1
      var l = e(s)
      return l == r || l == o || l == n || l == i
    }
    return ((va = a), va)
  }
  var ga, uv
  function aA() {
    if (uv) return ga
    uv = 1
    var e = ht(),
      t = e['__core-js_shared__']
    return ((ga = t), ga)
  }
  var ma, cv
  function sA() {
    if (cv) return ma
    cv = 1
    var e = aA(),
      t = (function () {
        var r = /[^.]+$/.exec((e && e.keys && e.keys.IE_PROTO) || '')
        return r ? 'Symbol(src)_1.' + r : ''
      })()
    function n(r) {
      return !!t && t in r
    }
    return ((ma = n), ma)
  }
  var ya, dv
  function Dw() {
    if (dv) return ya
    dv = 1
    var e = Function.prototype,
      t = e.toString
    function n(r) {
      if (r != null) {
        try {
          return t.call(r)
        } catch {}
        try {
          return r + ''
        } catch {}
      }
      return ''
    }
    return ((ya = n), ya)
  }
  var ba, fv
  function lA() {
    if (fv) return ba
    fv = 1
    var e = Vr(),
      t = sA(),
      n = it(),
      r = Dw(),
      o = /[\\^$.*+?()[\]{}|]/g,
      i = /^\[object .+?Constructor\]$/,
      a = Function.prototype,
      s = Object.prototype,
      l = a.toString,
      u = s.hasOwnProperty,
      c = RegExp(
        '^' +
          l
            .call(u)
            .replace(o, '\\$&')
            .replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, '$1.*?') +
          '$'
      )
    function d(f) {
      if (!n(f) || t(f)) return !1
      var h = e(f) ? c : i
      return h.test(r(f))
    }
    return ((ba = d), ba)
  }
  var _a, hv
  function uA() {
    if (hv) return _a
    hv = 1
    function e(t, n) {
      return t?.[n]
    }
    return ((_a = e), _a)
  }
  var wa, pv
  function Tn() {
    if (pv) return wa
    pv = 1
    var e = lA(),
      t = uA()
    function n(r, o) {
      var i = t(r, o)
      return e(i) ? i : void 0
    }
    return ((wa = n), wa)
  }
  var Sa, vv
  function Rf() {
    if (vv) return Sa
    vv = 1
    var e = Tn(),
      t = ht(),
      n = e(t, 'Map')
    return ((Sa = n), Sa)
  }
  var xa, gv
  function ui() {
    if (gv) return xa
    gv = 1
    var e = Tn(),
      t = e(Object, 'create')
    return ((xa = t), xa)
  }
  var Ca, mv
  function cA() {
    if (mv) return Ca
    mv = 1
    var e = ui()
    function t() {
      ;((this.__data__ = e ? e(null) : {}), (this.size = 0))
    }
    return ((Ca = t), Ca)
  }
  var Ea, yv
  function dA() {
    if (yv) return Ea
    yv = 1
    function e(t) {
      var n = this.has(t) && delete this.__data__[t]
      return ((this.size -= n ? 1 : 0), n)
    }
    return ((Ea = e), Ea)
  }
  var $a, bv
  function fA() {
    if (bv) return $a
    bv = 1
    var e = ui(),
      t = '__lodash_hash_undefined__',
      n = Object.prototype,
      r = n.hasOwnProperty
    function o(i) {
      var a = this.__data__
      if (e) {
        var s = a[i]
        return s === t ? void 0 : s
      }
      return r.call(a, i) ? a[i] : void 0
    }
    return (($a = o), $a)
  }
  var Ta, _v
  function hA() {
    if (_v) return Ta
    _v = 1
    var e = ui(),
      t = Object.prototype,
      n = t.hasOwnProperty
    function r(o) {
      var i = this.__data__
      return e ? i[o] !== void 0 : n.call(i, o)
    }
    return ((Ta = r), Ta)
  }
  var Oa, wv
  function pA() {
    if (wv) return Oa
    wv = 1
    var e = ui(),
      t = '__lodash_hash_undefined__'
    function n(r, o) {
      var i = this.__data__
      return ((this.size += this.has(r) ? 0 : 1), (i[r] = e && o === void 0 ? t : o), this)
    }
    return ((Oa = n), Oa)
  }
  var Pa, Sv
  function vA() {
    if (Sv) return Pa
    Sv = 1
    var e = cA(),
      t = dA(),
      n = fA(),
      r = hA(),
      o = pA()
    function i(a) {
      var s = -1,
        l = a == null ? 0 : a.length
      for (this.clear(); ++s < l; ) {
        var u = a[s]
        this.set(u[0], u[1])
      }
    }
    return (
      (i.prototype.clear = e),
      (i.prototype.delete = t),
      (i.prototype.get = n),
      (i.prototype.has = r),
      (i.prototype.set = o),
      (Pa = i),
      Pa
    )
  }
  var Ia, xv
  function gA() {
    if (xv) return Ia
    xv = 1
    var e = vA(),
      t = li(),
      n = Rf()
    function r() {
      ;((this.size = 0), (this.__data__ = { hash: new e(), map: new (n || t)(), string: new e() }))
    }
    return ((Ia = r), Ia)
  }
  var Aa, Cv
  function mA() {
    if (Cv) return Aa
    Cv = 1
    function e(t) {
      var n = typeof t
      return n == 'string' || n == 'number' || n == 'symbol' || n == 'boolean'
        ? t !== '__proto__'
        : t === null
    }
    return ((Aa = e), Aa)
  }
  var Na, Ev
  function ci() {
    if (Ev) return Na
    Ev = 1
    var e = mA()
    function t(n, r) {
      var o = n.__data__
      return e(r) ? o[typeof r == 'string' ? 'string' : 'hash'] : o.map
    }
    return ((Na = t), Na)
  }
  var Ra, $v
  function yA() {
    if ($v) return Ra
    $v = 1
    var e = ci()
    function t(n) {
      var r = e(this, n).delete(n)
      return ((this.size -= r ? 1 : 0), r)
    }
    return ((Ra = t), Ra)
  }
  var Ma, Tv
  function bA() {
    if (Tv) return Ma
    Tv = 1
    var e = ci()
    function t(n) {
      return e(this, n).get(n)
    }
    return ((Ma = t), Ma)
  }
  var Da, Ov
  function _A() {
    if (Ov) return Da
    Ov = 1
    var e = ci()
    function t(n) {
      return e(this, n).has(n)
    }
    return ((Da = t), Da)
  }
  var Ba, Pv
  function wA() {
    if (Pv) return Ba
    Pv = 1
    var e = ci()
    function t(n, r) {
      var o = e(this, n),
        i = o.size
      return (o.set(n, r), (this.size += o.size == i ? 0 : 1), this)
    }
    return ((Ba = t), Ba)
  }
  var qa, Iv
  function Mf() {
    if (Iv) return qa
    Iv = 1
    var e = gA(),
      t = yA(),
      n = bA(),
      r = _A(),
      o = wA()
    function i(a) {
      var s = -1,
        l = a == null ? 0 : a.length
      for (this.clear(); ++s < l; ) {
        var u = a[s]
        this.set(u[0], u[1])
      }
    }
    return (
      (i.prototype.clear = e),
      (i.prototype.delete = t),
      (i.prototype.get = n),
      (i.prototype.has = r),
      (i.prototype.set = o),
      (qa = i),
      qa
    )
  }
  var za, Av
  function SA() {
    if (Av) return za
    Av = 1
    var e = li(),
      t = Rf(),
      n = Mf(),
      r = 200
    function o(i, a) {
      var s = this.__data__
      if (s instanceof e) {
        var l = s.__data__
        if (!t || l.length < r - 1) return (l.push([i, a]), (this.size = ++s.size), this)
        s = this.__data__ = new n(l)
      }
      return (s.set(i, a), (this.size = s.size), this)
    }
    return ((za = o), za)
  }
  var La, Nv
  function di() {
    if (Nv) return La
    Nv = 1
    var e = li(),
      t = eA(),
      n = tA(),
      r = nA(),
      o = rA(),
      i = SA()
    function a(s) {
      var l = (this.__data__ = new e(s))
      this.size = l.size
    }
    return (
      (a.prototype.clear = t),
      (a.prototype.delete = n),
      (a.prototype.get = r),
      (a.prototype.has = o),
      (a.prototype.set = i),
      (La = a),
      La
    )
  }
  var Fa, Rv
  function Df() {
    if (Rv) return Fa
    Rv = 1
    function e(t, n) {
      for (var r = -1, o = t == null ? 0 : t.length; ++r < o && n(t[r], r, t) !== !1; );
      return t
    }
    return ((Fa = e), Fa)
  }
  var ka, Mv
  function Bw() {
    if (Mv) return ka
    Mv = 1
    var e = Tn(),
      t = (function () {
        try {
          var n = e(Object, 'defineProperty')
          return (n({}, '', {}), n)
        } catch {}
      })()
    return ((ka = t), ka)
  }
  var Ha, Dv
  function fi() {
    if (Dv) return Ha
    Dv = 1
    var e = Bw()
    function t(n, r, o) {
      r == '__proto__' && e
        ? e(n, r, { configurable: !0, enumerable: !0, value: o, writable: !0 })
        : (n[r] = o)
    }
    return ((Ha = t), Ha)
  }
  var ja, Bv
  function hi() {
    if (Bv) return ja
    Bv = 1
    var e = fi(),
      t = Qn(),
      n = Object.prototype,
      r = n.hasOwnProperty
    function o(i, a, s) {
      var l = i[a]
      ;(!(r.call(i, a) && t(l, s)) || (s === void 0 && !(a in i))) && e(i, a, s)
    }
    return ((ja = o), ja)
  }
  var Va, qv
  function Gr() {
    if (qv) return Va
    qv = 1
    var e = hi(),
      t = fi()
    function n(r, o, i, a) {
      var s = !i
      i || (i = {})
      for (var l = -1, u = o.length; ++l < u; ) {
        var c = o[l],
          d = a ? a(i[c], r[c], c, i, r) : void 0
        ;(d === void 0 && (d = r[c]), s ? t(i, c, d) : e(i, c, d))
      }
      return i
    }
    return ((Va = n), Va)
  }
  var Ga, zv
  function xA() {
    if (zv) return Ga
    zv = 1
    function e(t, n) {
      for (var r = -1, o = Array(t); ++r < t; ) o[r] = n(r)
      return o
    }
    return ((Ga = e), Ga)
  }
  var Wa, Lv
  function $t() {
    if (Lv) return Wa
    Lv = 1
    function e(t) {
      return t != null && typeof t == 'object'
    }
    return ((Wa = e), Wa)
  }
  var Ua, Fv
  function CA() {
    if (Fv) return Ua
    Fv = 1
    var e = $n(),
      t = $t(),
      n = '[object Arguments]'
    function r(o) {
      return t(o) && e(o) == n
    }
    return ((Ua = r), Ua)
  }
  var Ya, kv
  function Wr() {
    if (kv) return Ya
    kv = 1
    var e = CA(),
      t = $t(),
      n = Object.prototype,
      r = n.hasOwnProperty,
      o = n.propertyIsEnumerable,
      i = e(
        (function () {
          return arguments
        })()
      )
        ? e
        : function (a) {
            return t(a) && r.call(a, 'callee') && !o.call(a, 'callee')
          }
    return ((Ya = i), Ya)
  }
  var Xa, Hv
  function qe() {
    if (Hv) return Xa
    Hv = 1
    var e = Array.isArray
    return ((Xa = e), Xa)
  }
  var ur = { exports: {} },
    Ka,
    jv
  function EA() {
    if (jv) return Ka
    jv = 1
    function e() {
      return !1
    }
    return ((Ka = e), Ka)
  }
  ur.exports
  var Vv
  function tr() {
    return (
      Vv ||
        ((Vv = 1),
        (function (e, t) {
          var n = ht(),
            r = EA(),
            o = t && !t.nodeType && t,
            i = o && !0 && e && !e.nodeType && e,
            a = i && i.exports === o,
            s = a ? n.Buffer : void 0,
            l = s ? s.isBuffer : void 0,
            u = l || r
          e.exports = u
        })(ur, ur.exports)),
      ur.exports
    )
  }
  var Za, Gv
  function pi() {
    if (Gv) return Za
    Gv = 1
    var e = 9007199254740991,
      t = /^(?:0|[1-9]\d*)$/
    function n(r, o) {
      var i = typeof r
      return (
        (o = o ?? e),
        !!o && (i == 'number' || (i != 'symbol' && t.test(r))) && r > -1 && r % 1 == 0 && r < o
      )
    }
    return ((Za = n), Za)
  }
  var Ja, Wv
  function Bf() {
    if (Wv) return Ja
    Wv = 1
    var e = 9007199254740991
    function t(n) {
      return typeof n == 'number' && n > -1 && n % 1 == 0 && n <= e
    }
    return ((Ja = t), Ja)
  }
  var Qa, Uv
  function $A() {
    if (Uv) return Qa
    Uv = 1
    var e = $n(),
      t = Bf(),
      n = $t(),
      r = '[object Arguments]',
      o = '[object Array]',
      i = '[object Boolean]',
      a = '[object Date]',
      s = '[object Error]',
      l = '[object Function]',
      u = '[object Map]',
      c = '[object Number]',
      d = '[object Object]',
      f = '[object RegExp]',
      h = '[object Set]',
      g = '[object String]',
      m = '[object WeakMap]',
      v = '[object ArrayBuffer]',
      b = '[object DataView]',
      y = '[object Float32Array]',
      p = '[object Float64Array]',
      _ = '[object Int8Array]',
      x = '[object Int16Array]',
      S = '[object Int32Array]',
      w = '[object Uint8Array]',
      T = '[object Uint8ClampedArray]',
      A = '[object Uint16Array]',
      $ = '[object Uint32Array]',
      P = {}
    ;((P[y] = P[p] = P[_] = P[x] = P[S] = P[w] = P[T] = P[A] = P[$] = !0),
      (P[r] =
        P[o] =
        P[v] =
        P[i] =
        P[b] =
        P[a] =
        P[s] =
        P[l] =
        P[u] =
        P[c] =
        P[d] =
        P[f] =
        P[h] =
        P[g] =
        P[m] =
          !1))
    function E(z) {
      return n(z) && t(z.length) && !!P[e(z)]
    }
    return ((Qa = E), Qa)
  }
  var es, Yv
  function vi() {
    if (Yv) return es
    Yv = 1
    function e(t) {
      return function (n) {
        return t(n)
      }
    }
    return ((es = e), es)
  }
  var cr = { exports: {} }
  cr.exports
  var Xv
  function qf() {
    return (
      Xv ||
        ((Xv = 1),
        (function (e, t) {
          var n = Mw(),
            r = t && !t.nodeType && t,
            o = r && !0 && e && !e.nodeType && e,
            i = o && o.exports === r,
            a = i && n.process,
            s = (function () {
              try {
                var l = o && o.require && o.require('util').types
                return l || (a && a.binding && a.binding('util'))
              } catch {}
            })()
          e.exports = s
        })(cr, cr.exports)),
      cr.exports
    )
  }
  var ts, Kv
  function Ur() {
    if (Kv) return ts
    Kv = 1
    var e = $A(),
      t = vi(),
      n = qf(),
      r = n && n.isTypedArray,
      o = r ? t(r) : e
    return ((ts = o), ts)
  }
  var ns, Zv
  function qw() {
    if (Zv) return ns
    Zv = 1
    var e = xA(),
      t = Wr(),
      n = qe(),
      r = tr(),
      o = pi(),
      i = Ur(),
      a = Object.prototype,
      s = a.hasOwnProperty
    function l(u, c) {
      var d = n(u),
        f = !d && t(u),
        h = !d && !f && r(u),
        g = !d && !f && !h && i(u),
        m = d || f || h || g,
        v = m ? e(u.length, String) : [],
        b = v.length
      for (var y in u)
        (c || s.call(u, y)) &&
          !(
            m &&
            (y == 'length' ||
              (h && (y == 'offset' || y == 'parent')) ||
              (g && (y == 'buffer' || y == 'byteLength' || y == 'byteOffset')) ||
              o(y, b))
          ) &&
          v.push(y)
      return v
    }
    return ((ns = l), ns)
  }
  var rs, Jv
  function gi() {
    if (Jv) return rs
    Jv = 1
    var e = Object.prototype
    function t(n) {
      var r = n && n.constructor,
        o = (typeof r == 'function' && r.prototype) || e
      return n === o
    }
    return ((rs = t), rs)
  }
  var os, Qv
  function zw() {
    if (Qv) return os
    Qv = 1
    function e(t, n) {
      return function (r) {
        return t(n(r))
      }
    }
    return ((os = e), os)
  }
  var is, eg
  function TA() {
    if (eg) return is
    eg = 1
    var e = zw(),
      t = e(Object.keys, Object)
    return ((is = t), is)
  }
  var as, tg
  function zf() {
    if (tg) return as
    tg = 1
    var e = gi(),
      t = TA(),
      n = Object.prototype,
      r = n.hasOwnProperty
    function o(i) {
      if (!e(i)) return t(i)
      var a = []
      for (var s in Object(i)) r.call(i, s) && s != 'constructor' && a.push(s)
      return a
    }
    return ((as = o), as)
  }
  var ss, ng
  function Ft() {
    if (ng) return ss
    ng = 1
    var e = Vr(),
      t = Bf()
    function n(r) {
      return r != null && t(r.length) && !e(r)
    }
    return ((ss = n), ss)
  }
  var ls, rg
  function nn() {
    if (rg) return ls
    rg = 1
    var e = qw(),
      t = zf(),
      n = Ft()
    function r(o) {
      return n(o) ? e(o) : t(o)
    }
    return ((ls = r), ls)
  }
  var us, og
  function OA() {
    if (og) return us
    og = 1
    var e = Gr(),
      t = nn()
    function n(r, o) {
      return r && e(o, t(o), r)
    }
    return ((us = n), us)
  }
  var cs, ig
  function PA() {
    if (ig) return cs
    ig = 1
    function e(t) {
      var n = []
      if (t != null) for (var r in Object(t)) n.push(r)
      return n
    }
    return ((cs = e), cs)
  }
  var ds, ag
  function IA() {
    if (ag) return ds
    ag = 1
    var e = it(),
      t = gi(),
      n = PA(),
      r = Object.prototype,
      o = r.hasOwnProperty
    function i(a) {
      if (!e(a)) return n(a)
      var s = t(a),
        l = []
      for (var u in a) (u == 'constructor' && (s || !o.call(a, u))) || l.push(u)
      return l
    }
    return ((ds = i), ds)
  }
  var fs, sg
  function On() {
    if (sg) return fs
    sg = 1
    var e = qw(),
      t = IA(),
      n = Ft()
    function r(o) {
      return n(o) ? e(o, !0) : t(o)
    }
    return ((fs = r), fs)
  }
  var hs, lg
  function AA() {
    if (lg) return hs
    lg = 1
    var e = Gr(),
      t = On()
    function n(r, o) {
      return r && e(o, t(o), r)
    }
    return ((hs = n), hs)
  }
  var dr = { exports: {} }
  dr.exports
  var ug
  function Lw() {
    return (
      ug ||
        ((ug = 1),
        (function (e, t) {
          var n = ht(),
            r = t && !t.nodeType && t,
            o = r && !0 && e && !e.nodeType && e,
            i = o && o.exports === r,
            a = i ? n.Buffer : void 0,
            s = a ? a.allocUnsafe : void 0
          function l(u, c) {
            if (c) return u.slice()
            var d = u.length,
              f = s ? s(d) : new u.constructor(d)
            return (u.copy(f), f)
          }
          e.exports = l
        })(dr, dr.exports)),
      dr.exports
    )
  }
  var ps, cg
  function Fw() {
    if (cg) return ps
    cg = 1
    function e(t, n) {
      var r = -1,
        o = t.length
      for (n || (n = Array(o)); ++r < o; ) n[r] = t[r]
      return n
    }
    return ((ps = e), ps)
  }
  var vs, dg
  function kw() {
    if (dg) return vs
    dg = 1
    function e(t, n) {
      for (var r = -1, o = t == null ? 0 : t.length, i = 0, a = []; ++r < o; ) {
        var s = t[r]
        n(s, r, t) && (a[i++] = s)
      }
      return a
    }
    return ((vs = e), vs)
  }
  var gs, fg
  function Hw() {
    if (fg) return gs
    fg = 1
    function e() {
      return []
    }
    return ((gs = e), gs)
  }
  var ms, hg
  function Lf() {
    if (hg) return ms
    hg = 1
    var e = kw(),
      t = Hw(),
      n = Object.prototype,
      r = n.propertyIsEnumerable,
      o = Object.getOwnPropertySymbols,
      i = o
        ? function (a) {
            return a == null
              ? []
              : ((a = Object(a)),
                e(o(a), function (s) {
                  return r.call(a, s)
                }))
          }
        : t
    return ((ms = i), ms)
  }
  var ys, pg
  function NA() {
    if (pg) return ys
    pg = 1
    var e = Gr(),
      t = Lf()
    function n(r, o) {
      return e(r, t(r), o)
    }
    return ((ys = n), ys)
  }
  var bs, vg
  function Ff() {
    if (vg) return bs
    vg = 1
    function e(t, n) {
      for (var r = -1, o = n.length, i = t.length; ++r < o; ) t[i + r] = n[r]
      return t
    }
    return ((bs = e), bs)
  }
  var _s, gg
  function mi() {
    if (gg) return _s
    gg = 1
    var e = zw(),
      t = e(Object.getPrototypeOf, Object)
    return ((_s = t), _s)
  }
  var ws, mg
  function jw() {
    if (mg) return ws
    mg = 1
    var e = Ff(),
      t = mi(),
      n = Lf(),
      r = Hw(),
      o = Object.getOwnPropertySymbols,
      i = o
        ? function (a) {
            for (var s = []; a; ) (e(s, n(a)), (a = t(a)))
            return s
          }
        : r
    return ((ws = i), ws)
  }
  var Ss, yg
  function RA() {
    if (yg) return Ss
    yg = 1
    var e = Gr(),
      t = jw()
    function n(r, o) {
      return e(r, t(r), o)
    }
    return ((Ss = n), Ss)
  }
  var xs, bg
  function Vw() {
    if (bg) return xs
    bg = 1
    var e = Ff(),
      t = qe()
    function n(r, o, i) {
      var a = o(r)
      return t(r) ? a : e(a, i(r))
    }
    return ((xs = n), xs)
  }
  var Cs, _g
  function Gw() {
    if (_g) return Cs
    _g = 1
    var e = Vw(),
      t = Lf(),
      n = nn()
    function r(o) {
      return e(o, n, t)
    }
    return ((Cs = r), Cs)
  }
  var Es, wg
  function MA() {
    if (wg) return Es
    wg = 1
    var e = Vw(),
      t = jw(),
      n = On()
    function r(o) {
      return e(o, n, t)
    }
    return ((Es = r), Es)
  }
  var $s, Sg
  function DA() {
    if (Sg) return $s
    Sg = 1
    var e = Tn(),
      t = ht(),
      n = e(t, 'DataView')
    return (($s = n), $s)
  }
  var Ts, xg
  function BA() {
    if (xg) return Ts
    xg = 1
    var e = Tn(),
      t = ht(),
      n = e(t, 'Promise')
    return ((Ts = n), Ts)
  }
  var Os, Cg
  function Ww() {
    if (Cg) return Os
    Cg = 1
    var e = Tn(),
      t = ht(),
      n = e(t, 'Set')
    return ((Os = n), Os)
  }
  var Ps, Eg
  function qA() {
    if (Eg) return Ps
    Eg = 1
    var e = Tn(),
      t = ht(),
      n = e(t, 'WeakMap')
    return ((Ps = n), Ps)
  }
  var Is, $g
  function nr() {
    if ($g) return Is
    $g = 1
    var e = DA(),
      t = Rf(),
      n = BA(),
      r = Ww(),
      o = qA(),
      i = $n(),
      a = Dw(),
      s = '[object Map]',
      l = '[object Object]',
      u = '[object Promise]',
      c = '[object Set]',
      d = '[object WeakMap]',
      f = '[object DataView]',
      h = a(e),
      g = a(t),
      m = a(n),
      v = a(r),
      b = a(o),
      y = i
    return (
      ((e && y(new e(new ArrayBuffer(1))) != f) ||
        (t && y(new t()) != s) ||
        (n && y(n.resolve()) != u) ||
        (r && y(new r()) != c) ||
        (o && y(new o()) != d)) &&
        (y = function (p) {
          var _ = i(p),
            x = _ == l ? p.constructor : void 0,
            S = x ? a(x) : ''
          if (S)
            switch (S) {
              case h:
                return f
              case g:
                return s
              case m:
                return u
              case v:
                return c
              case b:
                return d
            }
          return _
        }),
      (Is = y),
      Is
    )
  }
  var As, Tg
  function zA() {
    if (Tg) return As
    Tg = 1
    var e = Object.prototype,
      t = e.hasOwnProperty
    function n(r) {
      var o = r.length,
        i = new r.constructor(o)
      return (
        o &&
          typeof r[0] == 'string' &&
          t.call(r, 'index') &&
          ((i.index = r.index), (i.input = r.input)),
        i
      )
    }
    return ((As = n), As)
  }
  var Ns, Og
  function Uw() {
    if (Og) return Ns
    Og = 1
    var e = ht(),
      t = e.Uint8Array
    return ((Ns = t), Ns)
  }
  var Rs, Pg
  function kf() {
    if (Pg) return Rs
    Pg = 1
    var e = Uw()
    function t(n) {
      var r = new n.constructor(n.byteLength)
      return (new e(r).set(new e(n)), r)
    }
    return ((Rs = t), Rs)
  }
  var Ms, Ig
  function LA() {
    if (Ig) return Ms
    Ig = 1
    var e = kf()
    function t(n, r) {
      var o = r ? e(n.buffer) : n.buffer
      return new n.constructor(o, n.byteOffset, n.byteLength)
    }
    return ((Ms = t), Ms)
  }
  var Ds, Ag
  function FA() {
    if (Ag) return Ds
    Ag = 1
    var e = /\w*$/
    function t(n) {
      var r = new n.constructor(n.source, e.exec(n))
      return ((r.lastIndex = n.lastIndex), r)
    }
    return ((Ds = t), Ds)
  }
  var Bs, Ng
  function kA() {
    if (Ng) return Bs
    Ng = 1
    var e = er(),
      t = e ? e.prototype : void 0,
      n = t ? t.valueOf : void 0
    function r(o) {
      return n ? Object(n.call(o)) : {}
    }
    return ((Bs = r), Bs)
  }
  var qs, Rg
  function Yw() {
    if (Rg) return qs
    Rg = 1
    var e = kf()
    function t(n, r) {
      var o = r ? e(n.buffer) : n.buffer
      return new n.constructor(o, n.byteOffset, n.length)
    }
    return ((qs = t), qs)
  }
  var zs, Mg
  function HA() {
    if (Mg) return zs
    Mg = 1
    var e = kf(),
      t = LA(),
      n = FA(),
      r = kA(),
      o = Yw(),
      i = '[object Boolean]',
      a = '[object Date]',
      s = '[object Map]',
      l = '[object Number]',
      u = '[object RegExp]',
      c = '[object Set]',
      d = '[object String]',
      f = '[object Symbol]',
      h = '[object ArrayBuffer]',
      g = '[object DataView]',
      m = '[object Float32Array]',
      v = '[object Float64Array]',
      b = '[object Int8Array]',
      y = '[object Int16Array]',
      p = '[object Int32Array]',
      _ = '[object Uint8Array]',
      x = '[object Uint8ClampedArray]',
      S = '[object Uint16Array]',
      w = '[object Uint32Array]'
    function T(A, $, P) {
      var E = A.constructor
      switch ($) {
        case h:
          return e(A)
        case i:
        case a:
          return new E(+A)
        case g:
          return t(A, P)
        case m:
        case v:
        case b:
        case y:
        case p:
        case _:
        case x:
        case S:
        case w:
          return o(A, P)
        case s:
          return new E()
        case l:
        case d:
          return new E(A)
        case u:
          return n(A)
        case c:
          return new E()
        case f:
          return r(A)
      }
    }
    return ((zs = T), zs)
  }
  var Ls, Dg
  function Xw() {
    if (Dg) return Ls
    Dg = 1
    var e = it(),
      t = Object.create,
      n = (function () {
        function r() {}
        return function (o) {
          if (!e(o)) return {}
          if (t) return t(o)
          r.prototype = o
          var i = new r()
          return ((r.prototype = void 0), i)
        }
      })()
    return ((Ls = n), Ls)
  }
  var Fs, Bg
  function Kw() {
    if (Bg) return Fs
    Bg = 1
    var e = Xw(),
      t = mi(),
      n = gi()
    function r(o) {
      return typeof o.constructor == 'function' && !n(o) ? e(t(o)) : {}
    }
    return ((Fs = r), Fs)
  }
  var ks, qg
  function jA() {
    if (qg) return ks
    qg = 1
    var e = nr(),
      t = $t(),
      n = '[object Map]'
    function r(o) {
      return t(o) && e(o) == n
    }
    return ((ks = r), ks)
  }
  var Hs, zg
  function VA() {
    if (zg) return Hs
    zg = 1
    var e = jA(),
      t = vi(),
      n = qf(),
      r = n && n.isMap,
      o = r ? t(r) : e
    return ((Hs = o), Hs)
  }
  var js, Lg
  function GA() {
    if (Lg) return js
    Lg = 1
    var e = nr(),
      t = $t(),
      n = '[object Set]'
    function r(o) {
      return t(o) && e(o) == n
    }
    return ((js = r), js)
  }
  var Vs, Fg
  function WA() {
    if (Fg) return Vs
    Fg = 1
    var e = GA(),
      t = vi(),
      n = qf(),
      r = n && n.isSet,
      o = r ? t(r) : e
    return ((Vs = o), Vs)
  }
  var Gs, kg
  function Zw() {
    if (kg) return Gs
    kg = 1
    var e = di(),
      t = Df(),
      n = hi(),
      r = OA(),
      o = AA(),
      i = Lw(),
      a = Fw(),
      s = NA(),
      l = RA(),
      u = Gw(),
      c = MA(),
      d = nr(),
      f = zA(),
      h = HA(),
      g = Kw(),
      m = qe(),
      v = tr(),
      b = VA(),
      y = it(),
      p = WA(),
      _ = nn(),
      x = On(),
      S = 1,
      w = 2,
      T = 4,
      A = '[object Arguments]',
      $ = '[object Array]',
      P = '[object Boolean]',
      E = '[object Date]',
      z = '[object Error]',
      C = '[object Function]',
      R = '[object GeneratorFunction]',
      N = '[object Map]',
      j = '[object Number]',
      V = '[object Object]',
      H = '[object RegExp]',
      G = '[object Set]',
      Y = '[object String]',
      Z = '[object Symbol]',
      ne = '[object WeakMap]',
      B = '[object ArrayBuffer]',
      L = '[object DataView]',
      k = '[object Float32Array]',
      U = '[object Float64Array]',
      J = '[object Int8Array]',
      re = '[object Int16Array]',
      ie = '[object Int32Array]',
      _e = '[object Uint8Array]',
      ye = '[object Uint8ClampedArray]',
      be = '[object Uint16Array]',
      M = '[object Uint32Array]',
      O = {}
    ;((O[A] =
      O[$] =
      O[B] =
      O[L] =
      O[P] =
      O[E] =
      O[k] =
      O[U] =
      O[J] =
      O[re] =
      O[ie] =
      O[N] =
      O[j] =
      O[V] =
      O[H] =
      O[G] =
      O[Y] =
      O[Z] =
      O[_e] =
      O[ye] =
      O[be] =
      O[M] =
        !0),
      (O[z] = O[C] = O[ne] = !1))
    function q(I, W, ae, fe, le, ue) {
      var ge,
        Se = W & S,
        $e = W & w,
        et = W & T
      if ((ae && (ge = le ? ae(I, fe, le, ue) : ae(I)), ge !== void 0)) return ge
      if (!y(I)) return I
      var Ht = m(I)
      if (Ht) {
        if (((ge = f(I)), !Se)) return a(I, ge)
      } else {
        var jt = d(I),
          Jr = jt == C || jt == R
        if (v(I)) return i(I, Se)
        if (jt == V || jt == A || (Jr && !le)) {
          if (((ge = $e || Jr ? {} : g(I)), !Se)) return $e ? l(I, o(ge, I)) : s(I, r(ge, I))
        } else {
          if (!O[jt]) return le ? I : {}
          ge = h(I, jt, Se)
        }
      }
      ue || (ue = new e())
      var uh = ue.get(I)
      if (uh) return uh
      ;(ue.set(I, ge),
        p(I)
          ? I.forEach(function (Vt) {
              ge.add(q(Vt, W, ae, Vt, I, ue))
            })
          : b(I) &&
            I.forEach(function (Vt, rn) {
              ge.set(rn, q(Vt, W, ae, rn, I, ue))
            }))
      var GS = et ? ($e ? c : u) : $e ? x : _,
        ch = Ht ? void 0 : GS(I)
      return (
        t(ch || I, function (Vt, rn) {
          ;(ch && ((rn = Vt), (Vt = I[rn])), n(ge, rn, q(Vt, W, ae, rn, I, ue)))
        }),
        ge
      )
    }
    return ((Gs = q), Gs)
  }
  var Ws, Hg
  function UA() {
    if (Hg) return Ws
    Hg = 1
    var e = Zw(),
      t = 4
    function n(r) {
      return e(r, t)
    }
    return ((Ws = n), Ws)
  }
  var Us, jg
  function Hf() {
    if (jg) return Us
    jg = 1
    function e(t) {
      return function () {
        return t
      }
    }
    return ((Us = e), Us)
  }
  var Ys, Vg
  function YA() {
    if (Vg) return Ys
    Vg = 1
    function e(t) {
      return function (n, r, o) {
        for (var i = -1, a = Object(n), s = o(n), l = s.length; l--; ) {
          var u = s[t ? l : ++i]
          if (r(a[u], u, a) === !1) break
        }
        return n
      }
    }
    return ((Ys = e), Ys)
  }
  var Xs, Gg
  function jf() {
    if (Gg) return Xs
    Gg = 1
    var e = YA(),
      t = e()
    return ((Xs = t), Xs)
  }
  var Ks, Wg
  function Vf() {
    if (Wg) return Ks
    Wg = 1
    var e = jf(),
      t = nn()
    function n(r, o) {
      return r && e(r, o, t)
    }
    return ((Ks = n), Ks)
  }
  var Zs, Ug
  function XA() {
    if (Ug) return Zs
    Ug = 1
    var e = Ft()
    function t(n, r) {
      return function (o, i) {
        if (o == null) return o
        if (!e(o)) return n(o, i)
        for (
          var a = o.length, s = r ? a : -1, l = Object(o);
          (r ? s-- : ++s < a) && i(l[s], s, l) !== !1;

        );
        return o
      }
    }
    return ((Zs = t), Zs)
  }
  var Js, Yg
  function yi() {
    if (Yg) return Js
    Yg = 1
    var e = Vf(),
      t = XA(),
      n = t(e)
    return ((Js = n), Js)
  }
  var Qs, Xg
  function Pn() {
    if (Xg) return Qs
    Xg = 1
    function e(t) {
      return t
    }
    return ((Qs = e), Qs)
  }
  var el, Kg
  function Jw() {
    if (Kg) return el
    Kg = 1
    var e = Pn()
    function t(n) {
      return typeof n == 'function' ? n : e
    }
    return ((el = t), el)
  }
  var tl, Zg
  function Qw() {
    if (Zg) return tl
    Zg = 1
    var e = Df(),
      t = yi(),
      n = Jw(),
      r = qe()
    function o(i, a) {
      var s = r(i) ? e : t
      return s(i, n(a))
    }
    return ((tl = o), tl)
  }
  var nl, Jg
  function e1() {
    return (Jg || ((Jg = 1), (nl = Qw())), nl)
  }
  var rl, Qg
  function KA() {
    if (Qg) return rl
    Qg = 1
    var e = yi()
    function t(n, r) {
      var o = []
      return (
        e(n, function (i, a, s) {
          r(i, a, s) && o.push(i)
        }),
        o
      )
    }
    return ((rl = t), rl)
  }
  var ol, em
  function ZA() {
    if (em) return ol
    em = 1
    var e = '__lodash_hash_undefined__'
    function t(n) {
      return (this.__data__.set(n, e), this)
    }
    return ((ol = t), ol)
  }
  var il, tm
  function JA() {
    if (tm) return il
    tm = 1
    function e(t) {
      return this.__data__.has(t)
    }
    return ((il = e), il)
  }
  var al, nm
  function t1() {
    if (nm) return al
    nm = 1
    var e = Mf(),
      t = ZA(),
      n = JA()
    function r(o) {
      var i = -1,
        a = o == null ? 0 : o.length
      for (this.__data__ = new e(); ++i < a; ) this.add(o[i])
    }
    return ((r.prototype.add = r.prototype.push = t), (r.prototype.has = n), (al = r), al)
  }
  var sl, rm
  function QA() {
    if (rm) return sl
    rm = 1
    function e(t, n) {
      for (var r = -1, o = t == null ? 0 : t.length; ++r < o; ) if (n(t[r], r, t)) return !0
      return !1
    }
    return ((sl = e), sl)
  }
  var ll, om
  function n1() {
    if (om) return ll
    om = 1
    function e(t, n) {
      return t.has(n)
    }
    return ((ll = e), ll)
  }
  var ul, im
  function r1() {
    if (im) return ul
    im = 1
    var e = t1(),
      t = QA(),
      n = n1(),
      r = 1,
      o = 2
    function i(a, s, l, u, c, d) {
      var f = l & r,
        h = a.length,
        g = s.length
      if (h != g && !(f && g > h)) return !1
      var m = d.get(a),
        v = d.get(s)
      if (m && v) return m == s && v == a
      var b = -1,
        y = !0,
        p = l & o ? new e() : void 0
      for (d.set(a, s), d.set(s, a); ++b < h; ) {
        var _ = a[b],
          x = s[b]
        if (u) var S = f ? u(x, _, b, s, a, d) : u(_, x, b, a, s, d)
        if (S !== void 0) {
          if (S) continue
          y = !1
          break
        }
        if (p) {
          if (
            !t(s, function (w, T) {
              if (!n(p, T) && (_ === w || c(_, w, l, u, d))) return p.push(T)
            })
          ) {
            y = !1
            break
          }
        } else if (!(_ === x || c(_, x, l, u, d))) {
          y = !1
          break
        }
      }
      return (d.delete(a), d.delete(s), y)
    }
    return ((ul = i), ul)
  }
  var cl, am
  function eN() {
    if (am) return cl
    am = 1
    function e(t) {
      var n = -1,
        r = Array(t.size)
      return (
        t.forEach(function (o, i) {
          r[++n] = [i, o]
        }),
        r
      )
    }
    return ((cl = e), cl)
  }
  var dl, sm
  function Gf() {
    if (sm) return dl
    sm = 1
    function e(t) {
      var n = -1,
        r = Array(t.size)
      return (
        t.forEach(function (o) {
          r[++n] = o
        }),
        r
      )
    }
    return ((dl = e), dl)
  }
  var fl, lm
  function tN() {
    if (lm) return fl
    lm = 1
    var e = er(),
      t = Uw(),
      n = Qn(),
      r = r1(),
      o = eN(),
      i = Gf(),
      a = 1,
      s = 2,
      l = '[object Boolean]',
      u = '[object Date]',
      c = '[object Error]',
      d = '[object Map]',
      f = '[object Number]',
      h = '[object RegExp]',
      g = '[object Set]',
      m = '[object String]',
      v = '[object Symbol]',
      b = '[object ArrayBuffer]',
      y = '[object DataView]',
      p = e ? e.prototype : void 0,
      _ = p ? p.valueOf : void 0
    function x(S, w, T, A, $, P, E) {
      switch (T) {
        case y:
          if (S.byteLength != w.byteLength || S.byteOffset != w.byteOffset) return !1
          ;((S = S.buffer), (w = w.buffer))
        case b:
          return !(S.byteLength != w.byteLength || !P(new t(S), new t(w)))
        case l:
        case u:
        case f:
          return n(+S, +w)
        case c:
          return S.name == w.name && S.message == w.message
        case h:
        case m:
          return S == w + ''
        case d:
          var z = o
        case g:
          var C = A & a
          if ((z || (z = i), S.size != w.size && !C)) return !1
          var R = E.get(S)
          if (R) return R == w
          ;((A |= s), E.set(S, w))
          var N = r(z(S), z(w), A, $, P, E)
          return (E.delete(S), N)
        case v:
          if (_) return _.call(S) == _.call(w)
      }
      return !1
    }
    return ((fl = x), fl)
  }
  var hl, um
  function nN() {
    if (um) return hl
    um = 1
    var e = Gw(),
      t = 1,
      n = Object.prototype,
      r = n.hasOwnProperty
    function o(i, a, s, l, u, c) {
      var d = s & t,
        f = e(i),
        h = f.length,
        g = e(a),
        m = g.length
      if (h != m && !d) return !1
      for (var v = h; v--; ) {
        var b = f[v]
        if (!(d ? b in a : r.call(a, b))) return !1
      }
      var y = c.get(i),
        p = c.get(a)
      if (y && p) return y == a && p == i
      var _ = !0
      ;(c.set(i, a), c.set(a, i))
      for (var x = d; ++v < h; ) {
        b = f[v]
        var S = i[b],
          w = a[b]
        if (l) var T = d ? l(w, S, b, a, i, c) : l(S, w, b, i, a, c)
        if (!(T === void 0 ? S === w || u(S, w, s, l, c) : T)) {
          _ = !1
          break
        }
        x || (x = b == 'constructor')
      }
      if (_ && !x) {
        var A = i.constructor,
          $ = a.constructor
        A != $ &&
          'constructor' in i &&
          'constructor' in a &&
          !(typeof A == 'function' && A instanceof A && typeof $ == 'function' && $ instanceof $) &&
          (_ = !1)
      }
      return (c.delete(i), c.delete(a), _)
    }
    return ((hl = o), hl)
  }
  var pl, cm
  function rN() {
    if (cm) return pl
    cm = 1
    var e = di(),
      t = r1(),
      n = tN(),
      r = nN(),
      o = nr(),
      i = qe(),
      a = tr(),
      s = Ur(),
      l = 1,
      u = '[object Arguments]',
      c = '[object Array]',
      d = '[object Object]',
      f = Object.prototype,
      h = f.hasOwnProperty
    function g(m, v, b, y, p, _) {
      var x = i(m),
        S = i(v),
        w = x ? c : o(m),
        T = S ? c : o(v)
      ;((w = w == u ? d : w), (T = T == u ? d : T))
      var A = w == d,
        $ = T == d,
        P = w == T
      if (P && a(m)) {
        if (!a(v)) return !1
        ;((x = !0), (A = !1))
      }
      if (P && !A)
        return (_ || (_ = new e()), x || s(m) ? t(m, v, b, y, p, _) : n(m, v, w, b, y, p, _))
      if (!(b & l)) {
        var E = A && h.call(m, '__wrapped__'),
          z = $ && h.call(v, '__wrapped__')
        if (E || z) {
          var C = E ? m.value() : m,
            R = z ? v.value() : v
          return (_ || (_ = new e()), p(C, R, b, y, _))
        }
      }
      return P ? (_ || (_ = new e()), r(m, v, b, y, p, _)) : !1
    }
    return ((pl = g), pl)
  }
  var vl, dm
  function o1() {
    if (dm) return vl
    dm = 1
    var e = rN(),
      t = $t()
    function n(r, o, i, a, s) {
      return r === o
        ? !0
        : r == null || o == null || (!t(r) && !t(o))
          ? r !== r && o !== o
          : e(r, o, i, a, n, s)
    }
    return ((vl = n), vl)
  }
  var gl, fm
  function oN() {
    if (fm) return gl
    fm = 1
    var e = di(),
      t = o1(),
      n = 1,
      r = 2
    function o(i, a, s, l) {
      var u = s.length,
        c = u,
        d = !l
      if (i == null) return !c
      for (i = Object(i); u--; ) {
        var f = s[u]
        if (d && f[2] ? f[1] !== i[f[0]] : !(f[0] in i)) return !1
      }
      for (; ++u < c; ) {
        f = s[u]
        var h = f[0],
          g = i[h],
          m = f[1]
        if (d && f[2]) {
          if (g === void 0 && !(h in i)) return !1
        } else {
          var v = new e()
          if (l) var b = l(g, m, h, i, a, v)
          if (!(b === void 0 ? t(m, g, n | r, l, v) : b)) return !1
        }
      }
      return !0
    }
    return ((gl = o), gl)
  }
  var ml, hm
  function i1() {
    if (hm) return ml
    hm = 1
    var e = it()
    function t(n) {
      return n === n && !e(n)
    }
    return ((ml = t), ml)
  }
  var yl, pm
  function iN() {
    if (pm) return yl
    pm = 1
    var e = i1(),
      t = nn()
    function n(r) {
      for (var o = t(r), i = o.length; i--; ) {
        var a = o[i],
          s = r[a]
        o[i] = [a, s, e(s)]
      }
      return o
    }
    return ((yl = n), yl)
  }
  var bl, vm
  function a1() {
    if (vm) return bl
    vm = 1
    function e(t, n) {
      return function (r) {
        return r == null ? !1 : r[t] === n && (n !== void 0 || t in Object(r))
      }
    }
    return ((bl = e), bl)
  }
  var _l, gm
  function aN() {
    if (gm) return _l
    gm = 1
    var e = oN(),
      t = iN(),
      n = a1()
    function r(o) {
      var i = t(o)
      return i.length == 1 && i[0][2]
        ? n(i[0][0], i[0][1])
        : function (a) {
            return a === o || e(a, o, i)
          }
    }
    return ((_l = r), _l)
  }
  var wl, mm
  function rr() {
    if (mm) return wl
    mm = 1
    var e = $n(),
      t = $t(),
      n = '[object Symbol]'
    function r(o) {
      return typeof o == 'symbol' || (t(o) && e(o) == n)
    }
    return ((wl = r), wl)
  }
  var Sl, ym
  function Wf() {
    if (ym) return Sl
    ym = 1
    var e = qe(),
      t = rr(),
      n = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/,
      r = /^\w*$/
    function o(i, a) {
      if (e(i)) return !1
      var s = typeof i
      return s == 'number' || s == 'symbol' || s == 'boolean' || i == null || t(i)
        ? !0
        : r.test(i) || !n.test(i) || (a != null && i in Object(a))
    }
    return ((Sl = o), Sl)
  }
  var xl, bm
  function sN() {
    if (bm) return xl
    bm = 1
    var e = Mf(),
      t = 'Expected a function'
    function n(r, o) {
      if (typeof r != 'function' || (o != null && typeof o != 'function')) throw new TypeError(t)
      var i = function () {
        var a = arguments,
          s = o ? o.apply(this, a) : a[0],
          l = i.cache
        if (l.has(s)) return l.get(s)
        var u = r.apply(this, a)
        return ((i.cache = l.set(s, u) || l), u)
      }
      return ((i.cache = new (n.Cache || e)()), i)
    }
    return ((n.Cache = e), (xl = n), xl)
  }
  var Cl, _m
  function lN() {
    if (_m) return Cl
    _m = 1
    var e = sN(),
      t = 500
    function n(r) {
      var o = e(r, function (a) {
          return (i.size === t && i.clear(), a)
        }),
        i = o.cache
      return o
    }
    return ((Cl = n), Cl)
  }
  var El, wm
  function uN() {
    if (wm) return El
    wm = 1
    var e = lN(),
      t =
        /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g,
      n = /\\(\\)?/g,
      r = e(function (o) {
        var i = []
        return (
          o.charCodeAt(0) === 46 && i.push(''),
          o.replace(t, function (a, s, l, u) {
            i.push(l ? u.replace(n, '$1') : s || a)
          }),
          i
        )
      })
    return ((El = r), El)
  }
  var $l, Sm
  function bi() {
    if (Sm) return $l
    Sm = 1
    function e(t, n) {
      for (var r = -1, o = t == null ? 0 : t.length, i = Array(o); ++r < o; ) i[r] = n(t[r], r, t)
      return i
    }
    return (($l = e), $l)
  }
  var Tl, xm
  function cN() {
    if (xm) return Tl
    xm = 1
    var e = er(),
      t = bi(),
      n = qe(),
      r = rr(),
      o = e ? e.prototype : void 0,
      i = o ? o.toString : void 0
    function a(s) {
      if (typeof s == 'string') return s
      if (n(s)) return t(s, a) + ''
      if (r(s)) return i ? i.call(s) : ''
      var l = s + ''
      return l == '0' && 1 / s == -1 / 0 ? '-0' : l
    }
    return ((Tl = a), Tl)
  }
  var Ol, Cm
  function s1() {
    if (Cm) return Ol
    Cm = 1
    var e = cN()
    function t(n) {
      return n == null ? '' : e(n)
    }
    return ((Ol = t), Ol)
  }
  var Pl, Em
  function _i() {
    if (Em) return Pl
    Em = 1
    var e = qe(),
      t = Wf(),
      n = uN(),
      r = s1()
    function o(i, a) {
      return e(i) ? i : t(i, a) ? [i] : n(r(i))
    }
    return ((Pl = o), Pl)
  }
  var Il, $m
  function Yr() {
    if ($m) return Il
    $m = 1
    var e = rr()
    function t(n) {
      if (typeof n == 'string' || e(n)) return n
      var r = n + ''
      return r == '0' && 1 / n == -1 / 0 ? '-0' : r
    }
    return ((Il = t), Il)
  }
  var Al, Tm
  function wi() {
    if (Tm) return Al
    Tm = 1
    var e = _i(),
      t = Yr()
    function n(r, o) {
      o = e(o, r)
      for (var i = 0, a = o.length; r != null && i < a; ) r = r[t(o[i++])]
      return i && i == a ? r : void 0
    }
    return ((Al = n), Al)
  }
  var Nl, Om
  function dN() {
    if (Om) return Nl
    Om = 1
    var e = wi()
    function t(n, r, o) {
      var i = n == null ? void 0 : e(n, r)
      return i === void 0 ? o : i
    }
    return ((Nl = t), Nl)
  }
  var Rl, Pm
  function fN() {
    if (Pm) return Rl
    Pm = 1
    function e(t, n) {
      return t != null && n in Object(t)
    }
    return ((Rl = e), Rl)
  }
  var Ml, Im
  function l1() {
    if (Im) return Ml
    Im = 1
    var e = _i(),
      t = Wr(),
      n = qe(),
      r = pi(),
      o = Bf(),
      i = Yr()
    function a(s, l, u) {
      l = e(l, s)
      for (var c = -1, d = l.length, f = !1; ++c < d; ) {
        var h = i(l[c])
        if (!(f = s != null && u(s, h))) break
        s = s[h]
      }
      return f || ++c != d
        ? f
        : ((d = s == null ? 0 : s.length), !!d && o(d) && r(h, d) && (n(s) || t(s)))
    }
    return ((Ml = a), Ml)
  }
  var Dl, Am
  function u1() {
    if (Am) return Dl
    Am = 1
    var e = fN(),
      t = l1()
    function n(r, o) {
      return r != null && t(r, o, e)
    }
    return ((Dl = n), Dl)
  }
  var Bl, Nm
  function hN() {
    if (Nm) return Bl
    Nm = 1
    var e = o1(),
      t = dN(),
      n = u1(),
      r = Wf(),
      o = i1(),
      i = a1(),
      a = Yr(),
      s = 1,
      l = 2
    function u(c, d) {
      return r(c) && o(d)
        ? i(a(c), d)
        : function (f) {
            var h = t(f, c)
            return h === void 0 && h === d ? n(f, c) : e(d, h, s | l)
          }
    }
    return ((Bl = u), Bl)
  }
  var ql, Rm
  function c1() {
    if (Rm) return ql
    Rm = 1
    function e(t) {
      return function (n) {
        return n?.[t]
      }
    }
    return ((ql = e), ql)
  }
  var zl, Mm
  function pN() {
    if (Mm) return zl
    Mm = 1
    var e = wi()
    function t(n) {
      return function (r) {
        return e(r, n)
      }
    }
    return ((zl = t), zl)
  }
  var Ll, Dm
  function vN() {
    if (Dm) return Ll
    Dm = 1
    var e = c1(),
      t = pN(),
      n = Wf(),
      r = Yr()
    function o(i) {
      return n(i) ? e(r(i)) : t(i)
    }
    return ((Ll = o), Ll)
  }
  var Fl, Bm
  function kt() {
    if (Bm) return Fl
    Bm = 1
    var e = aN(),
      t = hN(),
      n = Pn(),
      r = qe(),
      o = vN()
    function i(a) {
      return typeof a == 'function'
        ? a
        : a == null
          ? n
          : typeof a == 'object'
            ? r(a)
              ? t(a[0], a[1])
              : e(a)
            : o(a)
    }
    return ((Fl = i), Fl)
  }
  var kl, qm
  function d1() {
    if (qm) return kl
    qm = 1
    var e = kw(),
      t = KA(),
      n = kt(),
      r = qe()
    function o(i, a) {
      var s = r(i) ? e : t
      return s(i, n(a, 3))
    }
    return ((kl = o), kl)
  }
  var Hl, zm
  function gN() {
    if (zm) return Hl
    zm = 1
    var e = Object.prototype,
      t = e.hasOwnProperty
    function n(r, o) {
      return r != null && t.call(r, o)
    }
    return ((Hl = n), Hl)
  }
  var jl, Lm
  function f1() {
    if (Lm) return jl
    Lm = 1
    var e = gN(),
      t = l1()
    function n(r, o) {
      return r != null && t(r, o, e)
    }
    return ((jl = n), jl)
  }
  var Vl, Fm
  function mN() {
    if (Fm) return Vl
    Fm = 1
    var e = zf(),
      t = nr(),
      n = Wr(),
      r = qe(),
      o = Ft(),
      i = tr(),
      a = gi(),
      s = Ur(),
      l = '[object Map]',
      u = '[object Set]',
      c = Object.prototype,
      d = c.hasOwnProperty
    function f(h) {
      if (h == null) return !0
      if (
        o(h) &&
        (r(h) || typeof h == 'string' || typeof h.splice == 'function' || i(h) || s(h) || n(h))
      )
        return !h.length
      var g = t(h)
      if (g == l || g == u) return !h.size
      if (a(h)) return !e(h).length
      for (var m in h) if (d.call(h, m)) return !1
      return !0
    }
    return ((Vl = f), Vl)
  }
  var Gl, km
  function h1() {
    if (km) return Gl
    km = 1
    function e(t) {
      return t === void 0
    }
    return ((Gl = e), Gl)
  }
  var Wl, Hm
  function p1() {
    if (Hm) return Wl
    Hm = 1
    var e = yi(),
      t = Ft()
    function n(r, o) {
      var i = -1,
        a = t(r) ? Array(r.length) : []
      return (
        e(r, function (s, l, u) {
          a[++i] = o(s, l, u)
        }),
        a
      )
    }
    return ((Wl = n), Wl)
  }
  var Ul, jm
  function v1() {
    if (jm) return Ul
    jm = 1
    var e = bi(),
      t = kt(),
      n = p1(),
      r = qe()
    function o(i, a) {
      var s = r(i) ? e : n
      return s(i, t(a, 3))
    }
    return ((Ul = o), Ul)
  }
  var Yl, Vm
  function yN() {
    if (Vm) return Yl
    Vm = 1
    function e(t, n, r, o) {
      var i = -1,
        a = t == null ? 0 : t.length
      for (o && a && (r = t[++i]); ++i < a; ) r = n(r, t[i], i, t)
      return r
    }
    return ((Yl = e), Yl)
  }
  var Xl, Gm
  function bN() {
    if (Gm) return Xl
    Gm = 1
    function e(t, n, r, o, i) {
      return (
        i(t, function (a, s, l) {
          r = o ? ((o = !1), a) : n(r, a, s, l)
        }),
        r
      )
    }
    return ((Xl = e), Xl)
  }
  var Kl, Wm
  function g1() {
    if (Wm) return Kl
    Wm = 1
    var e = yN(),
      t = yi(),
      n = kt(),
      r = bN(),
      o = qe()
    function i(a, s, l) {
      var u = o(a) ? e : r,
        c = arguments.length < 3
      return u(a, n(s, 4), l, c, t)
    }
    return ((Kl = i), Kl)
  }
  var Zl, Um
  function _N() {
    if (Um) return Zl
    Um = 1
    var e = $n(),
      t = qe(),
      n = $t(),
      r = '[object String]'
    function o(i) {
      return typeof i == 'string' || (!t(i) && n(i) && e(i) == r)
    }
    return ((Zl = o), Zl)
  }
  var Jl, Ym
  function wN() {
    if (Ym) return Jl
    Ym = 1
    var e = c1(),
      t = e('length')
    return ((Jl = t), Jl)
  }
  var Ql, Xm
  function SN() {
    if (Xm) return Ql
    Xm = 1
    var e = '\\ud800-\\udfff',
      t = '\\u0300-\\u036f',
      n = '\\ufe20-\\ufe2f',
      r = '\\u20d0-\\u20ff',
      o = t + n + r,
      i = '\\ufe0e\\ufe0f',
      a = '\\u200d',
      s = RegExp('[' + a + e + o + i + ']')
    function l(u) {
      return s.test(u)
    }
    return ((Ql = l), Ql)
  }
  var eu, Km
  function xN() {
    if (Km) return eu
    Km = 1
    var e = '\\ud800-\\udfff',
      t = '\\u0300-\\u036f',
      n = '\\ufe20-\\ufe2f',
      r = '\\u20d0-\\u20ff',
      o = t + n + r,
      i = '\\ufe0e\\ufe0f',
      a = '[' + e + ']',
      s = '[' + o + ']',
      l = '\\ud83c[\\udffb-\\udfff]',
      u = '(?:' + s + '|' + l + ')',
      c = '[^' + e + ']',
      d = '(?:\\ud83c[\\udde6-\\uddff]){2}',
      f = '[\\ud800-\\udbff][\\udc00-\\udfff]',
      h = '\\u200d',
      g = u + '?',
      m = '[' + i + ']?',
      v = '(?:' + h + '(?:' + [c, d, f].join('|') + ')' + m + g + ')*',
      b = m + g + v,
      y = '(?:' + [c + s + '?', s, d, f, a].join('|') + ')',
      p = RegExp(l + '(?=' + l + ')|' + y + b, 'g')
    function _(x) {
      for (var S = (p.lastIndex = 0); p.test(x); ) ++S
      return S
    }
    return ((eu = _), eu)
  }
  var tu, Zm
  function CN() {
    if (Zm) return tu
    Zm = 1
    var e = wN(),
      t = SN(),
      n = xN()
    function r(o) {
      return t(o) ? n(o) : e(o)
    }
    return ((tu = r), tu)
  }
  var nu, Jm
  function EN() {
    if (Jm) return nu
    Jm = 1
    var e = zf(),
      t = nr(),
      n = Ft(),
      r = _N(),
      o = CN(),
      i = '[object Map]',
      a = '[object Set]'
    function s(l) {
      if (l == null) return 0
      if (n(l)) return r(l) ? o(l) : l.length
      var u = t(l)
      return u == i || u == a ? l.size : e(l).length
    }
    return ((nu = s), nu)
  }
  var ru, Qm
  function $N() {
    if (Qm) return ru
    Qm = 1
    var e = Df(),
      t = Xw(),
      n = Vf(),
      r = kt(),
      o = mi(),
      i = qe(),
      a = tr(),
      s = Vr(),
      l = it(),
      u = Ur()
    function c(d, f, h) {
      var g = i(d),
        m = g || a(d) || u(d)
      if (((f = r(f, 4)), h == null)) {
        var v = d && d.constructor
        m ? (h = g ? new v() : []) : l(d) ? (h = s(v) ? t(o(d)) : {}) : (h = {})
      }
      return (
        (m ? e : n)(d, function (b, y, p) {
          return f(h, b, y, p)
        }),
        h
      )
    }
    return ((ru = c), ru)
  }
  var ou, ey
  function TN() {
    if (ey) return ou
    ey = 1
    var e = er(),
      t = Wr(),
      n = qe(),
      r = e ? e.isConcatSpreadable : void 0
    function o(i) {
      return n(i) || t(i) || !!(r && i && i[r])
    }
    return ((ou = o), ou)
  }
  var iu, ty
  function Uf() {
    if (ty) return iu
    ty = 1
    var e = Ff(),
      t = TN()
    function n(r, o, i, a, s) {
      var l = -1,
        u = r.length
      for (i || (i = t), s || (s = []); ++l < u; ) {
        var c = r[l]
        o > 0 && i(c) ? (o > 1 ? n(c, o - 1, i, a, s) : e(s, c)) : a || (s[s.length] = c)
      }
      return s
    }
    return ((iu = n), iu)
  }
  var au, ny
  function ON() {
    if (ny) return au
    ny = 1
    function e(t, n, r) {
      switch (r.length) {
        case 0:
          return t.call(n)
        case 1:
          return t.call(n, r[0])
        case 2:
          return t.call(n, r[0], r[1])
        case 3:
          return t.call(n, r[0], r[1], r[2])
      }
      return t.apply(n, r)
    }
    return ((au = e), au)
  }
  var su, ry
  function m1() {
    if (ry) return su
    ry = 1
    var e = ON(),
      t = Math.max
    function n(r, o, i) {
      return (
        (o = t(o === void 0 ? r.length - 1 : o, 0)),
        function () {
          for (var a = arguments, s = -1, l = t(a.length - o, 0), u = Array(l); ++s < l; )
            u[s] = a[o + s]
          s = -1
          for (var c = Array(o + 1); ++s < o; ) c[s] = a[s]
          return ((c[o] = i(u)), e(r, this, c))
        }
      )
    }
    return ((su = n), su)
  }
  var lu, oy
  function PN() {
    if (oy) return lu
    oy = 1
    var e = Hf(),
      t = Bw(),
      n = Pn(),
      r = t
        ? function (o, i) {
            return t(o, 'toString', { configurable: !0, enumerable: !1, value: e(i), writable: !0 })
          }
        : n
    return ((lu = r), lu)
  }
  var uu, iy
  function IN() {
    if (iy) return uu
    iy = 1
    var e = 800,
      t = 16,
      n = Date.now
    function r(o) {
      var i = 0,
        a = 0
      return function () {
        var s = n(),
          l = t - (s - a)
        if (((a = s), l > 0)) {
          if (++i >= e) return arguments[0]
        } else i = 0
        return o.apply(void 0, arguments)
      }
    }
    return ((uu = r), uu)
  }
  var cu, ay
  function y1() {
    if (ay) return cu
    ay = 1
    var e = PN(),
      t = IN(),
      n = t(e)
    return ((cu = n), cu)
  }
  var du, sy
  function Si() {
    if (sy) return du
    sy = 1
    var e = Pn(),
      t = m1(),
      n = y1()
    function r(o, i) {
      return n(t(o, i, e), o + '')
    }
    return ((du = r), du)
  }
  var fu, ly
  function b1() {
    if (ly) return fu
    ly = 1
    function e(t, n, r, o) {
      for (var i = t.length, a = r + (o ? 1 : -1); o ? a-- : ++a < i; ) if (n(t[a], a, t)) return a
      return -1
    }
    return ((fu = e), fu)
  }
  var hu, uy
  function AN() {
    if (uy) return hu
    uy = 1
    function e(t) {
      return t !== t
    }
    return ((hu = e), hu)
  }
  var pu, cy
  function NN() {
    if (cy) return pu
    cy = 1
    function e(t, n, r) {
      for (var o = r - 1, i = t.length; ++o < i; ) if (t[o] === n) return o
      return -1
    }
    return ((pu = e), pu)
  }
  var vu, dy
  function RN() {
    if (dy) return vu
    dy = 1
    var e = b1(),
      t = AN(),
      n = NN()
    function r(o, i, a) {
      return i === i ? n(o, i, a) : e(o, t, a)
    }
    return ((vu = r), vu)
  }
  var gu, fy
  function MN() {
    if (fy) return gu
    fy = 1
    var e = RN()
    function t(n, r) {
      var o = n == null ? 0 : n.length
      return !!o && e(n, r, 0) > -1
    }
    return ((gu = t), gu)
  }
  var mu, hy
  function DN() {
    if (hy) return mu
    hy = 1
    function e(t, n, r) {
      for (var o = -1, i = t == null ? 0 : t.length; ++o < i; ) if (r(n, t[o])) return !0
      return !1
    }
    return ((mu = e), mu)
  }
  var yu, py
  function BN() {
    if (py) return yu
    py = 1
    function e() {}
    return ((yu = e), yu)
  }
  var bu, vy
  function qN() {
    if (vy) return bu
    vy = 1
    var e = Ww(),
      t = BN(),
      n = Gf(),
      r = 1 / 0,
      o =
        e && 1 / n(new e([, -0]))[1] == r
          ? function (i) {
              return new e(i)
            }
          : t
    return ((bu = o), bu)
  }
  var _u, gy
  function zN() {
    if (gy) return _u
    gy = 1
    var e = t1(),
      t = MN(),
      n = DN(),
      r = n1(),
      o = qN(),
      i = Gf(),
      a = 200
    function s(l, u, c) {
      var d = -1,
        f = t,
        h = l.length,
        g = !0,
        m = [],
        v = m
      if (c) ((g = !1), (f = n))
      else if (h >= a) {
        var b = u ? null : o(l)
        if (b) return i(b)
        ;((g = !1), (f = r), (v = new e()))
      } else v = u ? [] : m
      e: for (; ++d < h; ) {
        var y = l[d],
          p = u ? u(y) : y
        if (((y = c || y !== 0 ? y : 0), g && p === p)) {
          for (var _ = v.length; _--; ) if (v[_] === p) continue e
          ;(u && v.push(p), m.push(y))
        } else f(v, p, c) || (v !== m && v.push(p), m.push(y))
      }
      return m
    }
    return ((_u = s), _u)
  }
  var wu, my
  function _1() {
    if (my) return wu
    my = 1
    var e = Ft(),
      t = $t()
    function n(r) {
      return t(r) && e(r)
    }
    return ((wu = n), wu)
  }
  var Su, yy
  function LN() {
    if (yy) return Su
    yy = 1
    var e = Uf(),
      t = Si(),
      n = zN(),
      r = _1(),
      o = t(function (i) {
        return n(e(i, 1, r, !0))
      })
    return ((Su = o), Su)
  }
  var xu, by
  function FN() {
    if (by) return xu
    by = 1
    var e = bi()
    function t(n, r) {
      return e(r, function (o) {
        return n[o]
      })
    }
    return ((xu = t), xu)
  }
  var Cu, _y
  function w1() {
    if (_y) return Cu
    _y = 1
    var e = FN(),
      t = nn()
    function n(r) {
      return r == null ? [] : e(r, t(r))
    }
    return ((Cu = n), Cu)
  }
  var Eu, wy
  function at() {
    if (wy) return Eu
    wy = 1
    var e
    if (typeof Nf == 'function')
      try {
        e = {
          clone: UA(),
          constant: Hf(),
          each: e1(),
          filter: d1(),
          has: f1(),
          isArray: qe(),
          isEmpty: mN(),
          isFunction: Vr(),
          isUndefined: h1(),
          keys: nn(),
          map: v1(),
          reduce: g1(),
          size: EN(),
          transform: $N(),
          union: LN(),
          values: w1(),
        }
      } catch {}
    return (e || (e = window._), (Eu = e), Eu)
  }
  var $u, Sy
  function Yf() {
    if (Sy) return $u
    Sy = 1
    var e = at()
    $u = o
    var t = '\0',
      n = '\0',
      r = ''
    function o(c) {
      ;((this._isDirected = e.has(c, 'directed') ? c.directed : !0),
        (this._isMultigraph = e.has(c, 'multigraph') ? c.multigraph : !1),
        (this._isCompound = e.has(c, 'compound') ? c.compound : !1),
        (this._label = void 0),
        (this._defaultNodeLabelFn = e.constant(void 0)),
        (this._defaultEdgeLabelFn = e.constant(void 0)),
        (this._nodes = {}),
        this._isCompound && ((this._parent = {}), (this._children = {}), (this._children[n] = {})),
        (this._in = {}),
        (this._preds = {}),
        (this._out = {}),
        (this._sucs = {}),
        (this._edgeObjs = {}),
        (this._edgeLabels = {}))
    }
    ;((o.prototype._nodeCount = 0),
      (o.prototype._edgeCount = 0),
      (o.prototype.isDirected = function () {
        return this._isDirected
      }),
      (o.prototype.isMultigraph = function () {
        return this._isMultigraph
      }),
      (o.prototype.isCompound = function () {
        return this._isCompound
      }),
      (o.prototype.setGraph = function (c) {
        return ((this._label = c), this)
      }),
      (o.prototype.graph = function () {
        return this._label
      }),
      (o.prototype.setDefaultNodeLabel = function (c) {
        return (e.isFunction(c) || (c = e.constant(c)), (this._defaultNodeLabelFn = c), this)
      }),
      (o.prototype.nodeCount = function () {
        return this._nodeCount
      }),
      (o.prototype.nodes = function () {
        return e.keys(this._nodes)
      }),
      (o.prototype.sources = function () {
        var c = this
        return e.filter(this.nodes(), function (d) {
          return e.isEmpty(c._in[d])
        })
      }),
      (o.prototype.sinks = function () {
        var c = this
        return e.filter(this.nodes(), function (d) {
          return e.isEmpty(c._out[d])
        })
      }),
      (o.prototype.setNodes = function (c, d) {
        var f = arguments,
          h = this
        return (
          e.each(c, function (g) {
            f.length > 1 ? h.setNode(g, d) : h.setNode(g)
          }),
          this
        )
      }),
      (o.prototype.setNode = function (c, d) {
        return e.has(this._nodes, c)
          ? (arguments.length > 1 && (this._nodes[c] = d), this)
          : ((this._nodes[c] = arguments.length > 1 ? d : this._defaultNodeLabelFn(c)),
            this._isCompound &&
              ((this._parent[c] = n), (this._children[c] = {}), (this._children[n][c] = !0)),
            (this._in[c] = {}),
            (this._preds[c] = {}),
            (this._out[c] = {}),
            (this._sucs[c] = {}),
            ++this._nodeCount,
            this)
      }),
      (o.prototype.node = function (c) {
        return this._nodes[c]
      }),
      (o.prototype.hasNode = function (c) {
        return e.has(this._nodes, c)
      }),
      (o.prototype.removeNode = function (c) {
        var d = this
        if (e.has(this._nodes, c)) {
          var f = function (h) {
            d.removeEdge(d._edgeObjs[h])
          }
          ;(delete this._nodes[c],
            this._isCompound &&
              (this._removeFromParentsChildList(c),
              delete this._parent[c],
              e.each(this.children(c), function (h) {
                d.setParent(h)
              }),
              delete this._children[c]),
            e.each(e.keys(this._in[c]), f),
            delete this._in[c],
            delete this._preds[c],
            e.each(e.keys(this._out[c]), f),
            delete this._out[c],
            delete this._sucs[c],
            --this._nodeCount)
        }
        return this
      }),
      (o.prototype.setParent = function (c, d) {
        if (!this._isCompound) throw new Error('Cannot set parent in a non-compound graph')
        if (e.isUndefined(d)) d = n
        else {
          d += ''
          for (var f = d; !e.isUndefined(f); f = this.parent(f))
            if (f === c)
              throw new Error('Setting ' + d + ' as parent of ' + c + ' would create a cycle')
          this.setNode(d)
        }
        return (
          this.setNode(c),
          this._removeFromParentsChildList(c),
          (this._parent[c] = d),
          (this._children[d][c] = !0),
          this
        )
      }),
      (o.prototype._removeFromParentsChildList = function (c) {
        delete this._children[this._parent[c]][c]
      }),
      (o.prototype.parent = function (c) {
        if (this._isCompound) {
          var d = this._parent[c]
          if (d !== n) return d
        }
      }),
      (o.prototype.children = function (c) {
        if ((e.isUndefined(c) && (c = n), this._isCompound)) {
          var d = this._children[c]
          if (d) return e.keys(d)
        } else {
          if (c === n) return this.nodes()
          if (this.hasNode(c)) return []
        }
      }),
      (o.prototype.predecessors = function (c) {
        var d = this._preds[c]
        if (d) return e.keys(d)
      }),
      (o.prototype.successors = function (c) {
        var d = this._sucs[c]
        if (d) return e.keys(d)
      }),
      (o.prototype.neighbors = function (c) {
        var d = this.predecessors(c)
        if (d) return e.union(d, this.successors(c))
      }),
      (o.prototype.isLeaf = function (c) {
        var d
        return (
          this.isDirected() ? (d = this.successors(c)) : (d = this.neighbors(c)),
          d.length === 0
        )
      }),
      (o.prototype.filterNodes = function (c) {
        var d = new this.constructor({
          directed: this._isDirected,
          multigraph: this._isMultigraph,
          compound: this._isCompound,
        })
        d.setGraph(this.graph())
        var f = this
        ;(e.each(this._nodes, function (m, v) {
          c(v) && d.setNode(v, m)
        }),
          e.each(this._edgeObjs, function (m) {
            d.hasNode(m.v) && d.hasNode(m.w) && d.setEdge(m, f.edge(m))
          }))
        var h = {}
        function g(m) {
          var v = f.parent(m)
          return v === void 0 || d.hasNode(v) ? ((h[m] = v), v) : v in h ? h[v] : g(v)
        }
        return (
          this._isCompound &&
            e.each(d.nodes(), function (m) {
              d.setParent(m, g(m))
            }),
          d
        )
      }),
      (o.prototype.setDefaultEdgeLabel = function (c) {
        return (e.isFunction(c) || (c = e.constant(c)), (this._defaultEdgeLabelFn = c), this)
      }),
      (o.prototype.edgeCount = function () {
        return this._edgeCount
      }),
      (o.prototype.edges = function () {
        return e.values(this._edgeObjs)
      }),
      (o.prototype.setPath = function (c, d) {
        var f = this,
          h = arguments
        return (
          e.reduce(c, function (g, m) {
            return (h.length > 1 ? f.setEdge(g, m, d) : f.setEdge(g, m), m)
          }),
          this
        )
      }),
      (o.prototype.setEdge = function () {
        var c,
          d,
          f,
          h,
          g = !1,
          m = arguments[0]
        ;(typeof m == 'object' && m !== null && 'v' in m
          ? ((c = m.v),
            (d = m.w),
            (f = m.name),
            arguments.length === 2 && ((h = arguments[1]), (g = !0)))
          : ((c = m),
            (d = arguments[1]),
            (f = arguments[3]),
            arguments.length > 2 && ((h = arguments[2]), (g = !0))),
          (c = '' + c),
          (d = '' + d),
          e.isUndefined(f) || (f = '' + f))
        var v = s(this._isDirected, c, d, f)
        if (e.has(this._edgeLabels, v)) return (g && (this._edgeLabels[v] = h), this)
        if (!e.isUndefined(f) && !this._isMultigraph)
          throw new Error('Cannot set a named edge when isMultigraph = false')
        ;(this.setNode(c),
          this.setNode(d),
          (this._edgeLabels[v] = g ? h : this._defaultEdgeLabelFn(c, d, f)))
        var b = l(this._isDirected, c, d, f)
        return (
          (c = b.v),
          (d = b.w),
          Object.freeze(b),
          (this._edgeObjs[v] = b),
          i(this._preds[d], c),
          i(this._sucs[c], d),
          (this._in[d][v] = b),
          (this._out[c][v] = b),
          this._edgeCount++,
          this
        )
      }),
      (o.prototype.edge = function (c, d, f) {
        var h =
          arguments.length === 1 ? u(this._isDirected, arguments[0]) : s(this._isDirected, c, d, f)
        return this._edgeLabels[h]
      }),
      (o.prototype.hasEdge = function (c, d, f) {
        var h =
          arguments.length === 1 ? u(this._isDirected, arguments[0]) : s(this._isDirected, c, d, f)
        return e.has(this._edgeLabels, h)
      }),
      (o.prototype.removeEdge = function (c, d, f) {
        var h =
            arguments.length === 1
              ? u(this._isDirected, arguments[0])
              : s(this._isDirected, c, d, f),
          g = this._edgeObjs[h]
        return (
          g &&
            ((c = g.v),
            (d = g.w),
            delete this._edgeLabels[h],
            delete this._edgeObjs[h],
            a(this._preds[d], c),
            a(this._sucs[c], d),
            delete this._in[d][h],
            delete this._out[c][h],
            this._edgeCount--),
          this
        )
      }),
      (o.prototype.inEdges = function (c, d) {
        var f = this._in[c]
        if (f) {
          var h = e.values(f)
          return d
            ? e.filter(h, function (g) {
                return g.v === d
              })
            : h
        }
      }),
      (o.prototype.outEdges = function (c, d) {
        var f = this._out[c]
        if (f) {
          var h = e.values(f)
          return d
            ? e.filter(h, function (g) {
                return g.w === d
              })
            : h
        }
      }),
      (o.prototype.nodeEdges = function (c, d) {
        var f = this.inEdges(c, d)
        if (f) return f.concat(this.outEdges(c, d))
      }))
    function i(c, d) {
      c[d] ? c[d]++ : (c[d] = 1)
    }
    function a(c, d) {
      --c[d] || delete c[d]
    }
    function s(c, d, f, h) {
      var g = '' + d,
        m = '' + f
      if (!c && g > m) {
        var v = g
        ;((g = m), (m = v))
      }
      return g + r + m + r + (e.isUndefined(h) ? t : h)
    }
    function l(c, d, f, h) {
      var g = '' + d,
        m = '' + f
      if (!c && g > m) {
        var v = g
        ;((g = m), (m = v))
      }
      var b = { v: g, w: m }
      return (h && (b.name = h), b)
    }
    function u(c, d) {
      return s(c, d.v, d.w, d.name)
    }
    return $u
  }
  var Tu, xy
  function kN() {
    return (xy || ((xy = 1), (Tu = '2.1.8')), Tu)
  }
  var Ou, Cy
  function HN() {
    return (Cy || ((Cy = 1), (Ou = { Graph: Yf(), version: kN() })), Ou)
  }
  var Pu, Ey
  function jN() {
    if (Ey) return Pu
    Ey = 1
    var e = at(),
      t = Yf()
    Pu = { write: n, read: i }
    function n(a) {
      var s = {
        options: {
          directed: a.isDirected(),
          multigraph: a.isMultigraph(),
          compound: a.isCompound(),
        },
        nodes: r(a),
        edges: o(a),
      }
      return (e.isUndefined(a.graph()) || (s.value = e.clone(a.graph())), s)
    }
    function r(a) {
      return e.map(a.nodes(), function (s) {
        var l = a.node(s),
          u = a.parent(s),
          c = { v: s }
        return (e.isUndefined(l) || (c.value = l), e.isUndefined(u) || (c.parent = u), c)
      })
    }
    function o(a) {
      return e.map(a.edges(), function (s) {
        var l = a.edge(s),
          u = { v: s.v, w: s.w }
        return (e.isUndefined(s.name) || (u.name = s.name), e.isUndefined(l) || (u.value = l), u)
      })
    }
    function i(a) {
      var s = new t(a.options).setGraph(a.value)
      return (
        e.each(a.nodes, function (l) {
          ;(s.setNode(l.v, l.value), l.parent && s.setParent(l.v, l.parent))
        }),
        e.each(a.edges, function (l) {
          s.setEdge({ v: l.v, w: l.w, name: l.name }, l.value)
        }),
        s
      )
    }
    return Pu
  }
  var Iu, $y
  function VN() {
    if ($y) return Iu
    $y = 1
    var e = at()
    Iu = t
    function t(n) {
      var r = {},
        o = [],
        i
      function a(s) {
        e.has(r, s) ||
          ((r[s] = !0), i.push(s), e.each(n.successors(s), a), e.each(n.predecessors(s), a))
      }
      return (
        e.each(n.nodes(), function (s) {
          ;((i = []), a(s), i.length && o.push(i))
        }),
        o
      )
    }
    return Iu
  }
  var Au, Ty
  function S1() {
    if (Ty) return Au
    Ty = 1
    var e = at()
    Au = t
    function t() {
      ;((this._arr = []), (this._keyIndices = {}))
    }
    return (
      (t.prototype.size = function () {
        return this._arr.length
      }),
      (t.prototype.keys = function () {
        return this._arr.map(function (n) {
          return n.key
        })
      }),
      (t.prototype.has = function (n) {
        return e.has(this._keyIndices, n)
      }),
      (t.prototype.priority = function (n) {
        var r = this._keyIndices[n]
        if (r !== void 0) return this._arr[r].priority
      }),
      (t.prototype.min = function () {
        if (this.size() === 0) throw new Error('Queue underflow')
        return this._arr[0].key
      }),
      (t.prototype.add = function (n, r) {
        var o = this._keyIndices
        if (((n = String(n)), !e.has(o, n))) {
          var i = this._arr,
            a = i.length
          return ((o[n] = a), i.push({ key: n, priority: r }), this._decrease(a), !0)
        }
        return !1
      }),
      (t.prototype.removeMin = function () {
        this._swap(0, this._arr.length - 1)
        var n = this._arr.pop()
        return (delete this._keyIndices[n.key], this._heapify(0), n.key)
      }),
      (t.prototype.decrease = function (n, r) {
        var o = this._keyIndices[n]
        if (r > this._arr[o].priority)
          throw new Error(
            'New priority is greater than current priority. Key: ' +
              n +
              ' Old: ' +
              this._arr[o].priority +
              ' New: ' +
              r
          )
        ;((this._arr[o].priority = r), this._decrease(o))
      }),
      (t.prototype._heapify = function (n) {
        var r = this._arr,
          o = 2 * n,
          i = o + 1,
          a = n
        o < r.length &&
          ((a = r[o].priority < r[a].priority ? o : a),
          i < r.length && (a = r[i].priority < r[a].priority ? i : a),
          a !== n && (this._swap(n, a), this._heapify(a)))
      }),
      (t.prototype._decrease = function (n) {
        for (
          var r = this._arr, o = r[n].priority, i;
          n !== 0 && ((i = n >> 1), !(r[i].priority < o));

        )
          (this._swap(n, i), (n = i))
      }),
      (t.prototype._swap = function (n, r) {
        var o = this._arr,
          i = this._keyIndices,
          a = o[n],
          s = o[r]
        ;((o[n] = s), (o[r] = a), (i[s.key] = n), (i[a.key] = r))
      }),
      Au
    )
  }
  var Nu, Oy
  function x1() {
    if (Oy) return Nu
    Oy = 1
    var e = at(),
      t = S1()
    Nu = r
    var n = e.constant(1)
    function r(i, a, s, l) {
      return o(
        i,
        String(a),
        s || n,
        l ||
          function (u) {
            return i.outEdges(u)
          }
      )
    }
    function o(i, a, s, l) {
      var u = {},
        c = new t(),
        d,
        f,
        h = function (g) {
          var m = g.v !== d ? g.v : g.w,
            v = u[m],
            b = s(g),
            y = f.distance + b
          if (b < 0)
            throw new Error(
              'dijkstra does not allow negative edge weights. Bad edge: ' + g + ' Weight: ' + b
            )
          y < v.distance && ((v.distance = y), (v.predecessor = d), c.decrease(m, y))
        }
      for (
        i.nodes().forEach(function (g) {
          var m = g === a ? 0 : Number.POSITIVE_INFINITY
          ;((u[g] = { distance: m }), c.add(g, m))
        });
        c.size() > 0 && ((d = c.removeMin()), (f = u[d]), f.distance !== Number.POSITIVE_INFINITY);

      )
        l(d).forEach(h)
      return u
    }
    return Nu
  }
  var Ru, Py
  function GN() {
    if (Py) return Ru
    Py = 1
    var e = x1(),
      t = at()
    Ru = n
    function n(r, o, i) {
      return t.transform(
        r.nodes(),
        function (a, s) {
          a[s] = e(r, s, o, i)
        },
        {}
      )
    }
    return Ru
  }
  var Mu, Iy
  function C1() {
    if (Iy) return Mu
    Iy = 1
    var e = at()
    Mu = t
    function t(n) {
      var r = 0,
        o = [],
        i = {},
        a = []
      function s(l) {
        var u = (i[l] = { onStack: !0, lowlink: r, index: r++ })
        if (
          (o.push(l),
          n.successors(l).forEach(function (f) {
            e.has(i, f)
              ? i[f].onStack && (u.lowlink = Math.min(u.lowlink, i[f].index))
              : (s(f), (u.lowlink = Math.min(u.lowlink, i[f].lowlink)))
          }),
          u.lowlink === u.index)
        ) {
          var c = [],
            d
          do ((d = o.pop()), (i[d].onStack = !1), c.push(d))
          while (l !== d)
          a.push(c)
        }
      }
      return (
        n.nodes().forEach(function (l) {
          e.has(i, l) || s(l)
        }),
        a
      )
    }
    return Mu
  }
  var Du, Ay
  function WN() {
    if (Ay) return Du
    Ay = 1
    var e = at(),
      t = C1()
    Du = n
    function n(r) {
      return e.filter(t(r), function (o) {
        return o.length > 1 || (o.length === 1 && r.hasEdge(o[0], o[0]))
      })
    }
    return Du
  }
  var Bu, Ny
  function UN() {
    if (Ny) return Bu
    Ny = 1
    var e = at()
    Bu = n
    var t = e.constant(1)
    function n(o, i, a) {
      return r(
        o,
        i || t,
        a ||
          function (s) {
            return o.outEdges(s)
          }
      )
    }
    function r(o, i, a) {
      var s = {},
        l = o.nodes()
      return (
        l.forEach(function (u) {
          ;((s[u] = {}),
            (s[u][u] = { distance: 0 }),
            l.forEach(function (c) {
              u !== c && (s[u][c] = { distance: Number.POSITIVE_INFINITY })
            }),
            a(u).forEach(function (c) {
              var d = c.v === u ? c.w : c.v,
                f = i(c)
              s[u][d] = { distance: f, predecessor: u }
            }))
        }),
        l.forEach(function (u) {
          var c = s[u]
          l.forEach(function (d) {
            var f = s[d]
            l.forEach(function (h) {
              var g = f[u],
                m = c[h],
                v = f[h],
                b = g.distance + m.distance
              b < v.distance && ((v.distance = b), (v.predecessor = m.predecessor))
            })
          })
        }),
        s
      )
    }
    return Bu
  }
  var qu, Ry
  function E1() {
    if (Ry) return qu
    Ry = 1
    var e = at()
    ;((qu = t), (t.CycleException = n))
    function t(r) {
      var o = {},
        i = {},
        a = []
      function s(l) {
        if (e.has(i, l)) throw new n()
        e.has(o, l) ||
          ((i[l] = !0), (o[l] = !0), e.each(r.predecessors(l), s), delete i[l], a.push(l))
      }
      if ((e.each(r.sinks(), s), e.size(o) !== r.nodeCount())) throw new n()
      return a
    }
    function n() {}
    return ((n.prototype = new Error()), qu)
  }
  var zu, My
  function YN() {
    if (My) return zu
    My = 1
    var e = E1()
    zu = t
    function t(n) {
      try {
        e(n)
      } catch (r) {
        if (r instanceof e.CycleException) return !1
        throw r
      }
      return !0
    }
    return zu
  }
  var Lu, Dy
  function $1() {
    if (Dy) return Lu
    Dy = 1
    var e = at()
    Lu = t
    function t(r, o, i) {
      e.isArray(o) || (o = [o])
      var a = (r.isDirected() ? r.successors : r.neighbors).bind(r),
        s = [],
        l = {}
      return (
        e.each(o, function (u) {
          if (!r.hasNode(u)) throw new Error('Graph does not have node: ' + u)
          n(r, u, i === 'post', l, a, s)
        }),
        s
      )
    }
    function n(r, o, i, a, s, l) {
      e.has(a, o) ||
        ((a[o] = !0),
        i || l.push(o),
        e.each(s(o), function (u) {
          n(r, u, i, a, s, l)
        }),
        i && l.push(o))
    }
    return Lu
  }
  var Fu, By
  function XN() {
    if (By) return Fu
    By = 1
    var e = $1()
    Fu = t
    function t(n, r) {
      return e(n, r, 'post')
    }
    return Fu
  }
  var ku, qy
  function KN() {
    if (qy) return ku
    qy = 1
    var e = $1()
    ku = t
    function t(n, r) {
      return e(n, r, 'pre')
    }
    return ku
  }
  var Hu, zy
  function ZN() {
    if (zy) return Hu
    zy = 1
    var e = at(),
      t = Yf(),
      n = S1()
    Hu = r
    function r(o, i) {
      var a = new t(),
        s = {},
        l = new n(),
        u
      function c(f) {
        var h = f.v === u ? f.w : f.v,
          g = l.priority(h)
        if (g !== void 0) {
          var m = i(f)
          m < g && ((s[h] = u), l.decrease(h, m))
        }
      }
      if (o.nodeCount() === 0) return a
      ;(e.each(o.nodes(), function (f) {
        ;(l.add(f, Number.POSITIVE_INFINITY), a.setNode(f))
      }),
        l.decrease(o.nodes()[0], 0))
      for (var d = !1; l.size() > 0; ) {
        if (((u = l.removeMin()), e.has(s, u))) a.setEdge(u, s[u])
        else {
          if (d) throw new Error('Input graph is not connected: ' + o)
          d = !0
        }
        o.nodeEdges(u).forEach(c)
      }
      return a
    }
    return Hu
  }
  var ju, Ly
  function JN() {
    return (
      Ly ||
        ((Ly = 1),
        (ju = {
          components: VN(),
          dijkstra: x1(),
          dijkstraAll: GN(),
          findCycles: WN(),
          floydWarshall: UN(),
          isAcyclic: YN(),
          postorder: XN(),
          preorder: KN(),
          prim: ZN(),
          tarjan: C1(),
          topsort: E1(),
        })),
      ju
    )
  }
  var Vu, Fy
  function QN() {
    if (Fy) return Vu
    Fy = 1
    var e = HN()
    return ((Vu = { Graph: e.Graph, json: jN(), alg: JN(), version: e.version }), Vu)
  }
  var Gu, ky
  function ft() {
    if (ky) return Gu
    ky = 1
    var e
    if (typeof Nf == 'function')
      try {
        e = QN()
      } catch {}
    return (e || (e = window.graphlib), (Gu = e), Gu)
  }
  var Wu, Hy
  function eR() {
    if (Hy) return Wu
    Hy = 1
    var e = Zw(),
      t = 1,
      n = 4
    function r(o) {
      return e(o, t | n)
    }
    return ((Wu = r), Wu)
  }
  var Uu, jy
  function xi() {
    if (jy) return Uu
    jy = 1
    var e = Qn(),
      t = Ft(),
      n = pi(),
      r = it()
    function o(i, a, s) {
      if (!r(s)) return !1
      var l = typeof a
      return (l == 'number' ? t(s) && n(a, s.length) : l == 'string' && a in s) ? e(s[a], i) : !1
    }
    return ((Uu = o), Uu)
  }
  var Yu, Vy
  function tR() {
    if (Vy) return Yu
    Vy = 1
    var e = Si(),
      t = Qn(),
      n = xi(),
      r = On(),
      o = Object.prototype,
      i = o.hasOwnProperty,
      a = e(function (s, l) {
        s = Object(s)
        var u = -1,
          c = l.length,
          d = c > 2 ? l[2] : void 0
        for (d && n(l[0], l[1], d) && (c = 1); ++u < c; )
          for (var f = l[u], h = r(f), g = -1, m = h.length; ++g < m; ) {
            var v = h[g],
              b = s[v]
            ;(b === void 0 || (t(b, o[v]) && !i.call(s, v))) && (s[v] = f[v])
          }
        return s
      })
    return ((Yu = a), Yu)
  }
  var Xu, Gy
  function nR() {
    if (Gy) return Xu
    Gy = 1
    var e = kt(),
      t = Ft(),
      n = nn()
    function r(o) {
      return function (i, a, s) {
        var l = Object(i)
        if (!t(i)) {
          var u = e(a, 3)
          ;((i = n(i)),
            (a = function (d) {
              return u(l[d], d, l)
            }))
        }
        var c = o(i, a, s)
        return c > -1 ? l[u ? i[c] : c] : void 0
      }
    }
    return ((Xu = r), Xu)
  }
  var Ku, Wy
  function rR() {
    if (Wy) return Ku
    Wy = 1
    var e = /\s/
    function t(n) {
      for (var r = n.length; r-- && e.test(n.charAt(r)); );
      return r
    }
    return ((Ku = t), Ku)
  }
  var Zu, Uy
  function oR() {
    if (Uy) return Zu
    Uy = 1
    var e = rR(),
      t = /^\s+/
    function n(r) {
      return r && r.slice(0, e(r) + 1).replace(t, '')
    }
    return ((Zu = n), Zu)
  }
  var Ju, Yy
  function iR() {
    if (Yy) return Ju
    Yy = 1
    var e = oR(),
      t = it(),
      n = rr(),
      r = NaN,
      o = /^[-+]0x[0-9a-f]+$/i,
      i = /^0b[01]+$/i,
      a = /^0o[0-7]+$/i,
      s = parseInt
    function l(u) {
      if (typeof u == 'number') return u
      if (n(u)) return r
      if (t(u)) {
        var c = typeof u.valueOf == 'function' ? u.valueOf() : u
        u = t(c) ? c + '' : c
      }
      if (typeof u != 'string') return u === 0 ? u : +u
      u = e(u)
      var d = i.test(u)
      return d || a.test(u) ? s(u.slice(2), d ? 2 : 8) : o.test(u) ? r : +u
    }
    return ((Ju = l), Ju)
  }
  var Qu, Xy
  function T1() {
    if (Xy) return Qu
    Xy = 1
    var e = iR(),
      t = 1 / 0,
      n = 17976931348623157e292
    function r(o) {
      if (!o) return o === 0 ? o : 0
      if (((o = e(o)), o === t || o === -t)) {
        var i = o < 0 ? -1 : 1
        return i * n
      }
      return o === o ? o : 0
    }
    return ((Qu = r), Qu)
  }
  var ec, Ky
  function aR() {
    if (Ky) return ec
    Ky = 1
    var e = T1()
    function t(n) {
      var r = e(n),
        o = r % 1
      return r === r ? (o ? r - o : r) : 0
    }
    return ((ec = t), ec)
  }
  var tc, Zy
  function sR() {
    if (Zy) return tc
    Zy = 1
    var e = b1(),
      t = kt(),
      n = aR(),
      r = Math.max
    function o(i, a, s) {
      var l = i == null ? 0 : i.length
      if (!l) return -1
      var u = s == null ? 0 : n(s)
      return (u < 0 && (u = r(l + u, 0)), e(i, t(a, 3), u))
    }
    return ((tc = o), tc)
  }
  var nc, Jy
  function lR() {
    if (Jy) return nc
    Jy = 1
    var e = nR(),
      t = sR(),
      n = e(t)
    return ((nc = n), nc)
  }
  var rc, Qy
  function O1() {
    if (Qy) return rc
    Qy = 1
    var e = Uf()
    function t(n) {
      var r = n == null ? 0 : n.length
      return r ? e(n, 1) : []
    }
    return ((rc = t), rc)
  }
  var oc, eb
  function uR() {
    if (eb) return oc
    eb = 1
    var e = jf(),
      t = Jw(),
      n = On()
    function r(o, i) {
      return o == null ? o : e(o, t(i), n)
    }
    return ((oc = r), oc)
  }
  var ic, tb
  function cR() {
    if (tb) return ic
    tb = 1
    function e(t) {
      var n = t == null ? 0 : t.length
      return n ? t[n - 1] : void 0
    }
    return ((ic = e), ic)
  }
  var ac, nb
  function dR() {
    if (nb) return ac
    nb = 1
    var e = fi(),
      t = Vf(),
      n = kt()
    function r(o, i) {
      var a = {}
      return (
        (i = n(i, 3)),
        t(o, function (s, l, u) {
          e(a, l, i(s, l, u))
        }),
        a
      )
    }
    return ((ac = r), ac)
  }
  var sc, rb
  function Xf() {
    if (rb) return sc
    rb = 1
    var e = rr()
    function t(n, r, o) {
      for (var i = -1, a = n.length; ++i < a; ) {
        var s = n[i],
          l = r(s)
        if (l != null && (u === void 0 ? l === l && !e(l) : o(l, u)))
          var u = l,
            c = s
      }
      return c
    }
    return ((sc = t), sc)
  }
  var lc, ob
  function fR() {
    if (ob) return lc
    ob = 1
    function e(t, n) {
      return t > n
    }
    return ((lc = e), lc)
  }
  var uc, ib
  function hR() {
    if (ib) return uc
    ib = 1
    var e = Xf(),
      t = fR(),
      n = Pn()
    function r(o) {
      return o && o.length ? e(o, n, t) : void 0
    }
    return ((uc = r), uc)
  }
  var cc, ab
  function P1() {
    if (ab) return cc
    ab = 1
    var e = fi(),
      t = Qn()
    function n(r, o, i) {
      ;((i !== void 0 && !t(r[o], i)) || (i === void 0 && !(o in r))) && e(r, o, i)
    }
    return ((cc = n), cc)
  }
  var dc, sb
  function pR() {
    if (sb) return dc
    sb = 1
    var e = $n(),
      t = mi(),
      n = $t(),
      r = '[object Object]',
      o = Function.prototype,
      i = Object.prototype,
      a = o.toString,
      s = i.hasOwnProperty,
      l = a.call(Object)
    function u(c) {
      if (!n(c) || e(c) != r) return !1
      var d = t(c)
      if (d === null) return !0
      var f = s.call(d, 'constructor') && d.constructor
      return typeof f == 'function' && f instanceof f && a.call(f) == l
    }
    return ((dc = u), dc)
  }
  var fc, lb
  function I1() {
    if (lb) return fc
    lb = 1
    function e(t, n) {
      if (!(n === 'constructor' && typeof t[n] == 'function') && n != '__proto__') return t[n]
    }
    return ((fc = e), fc)
  }
  var hc, ub
  function vR() {
    if (ub) return hc
    ub = 1
    var e = Gr(),
      t = On()
    function n(r) {
      return e(r, t(r))
    }
    return ((hc = n), hc)
  }
  var pc, cb
  function gR() {
    if (cb) return pc
    cb = 1
    var e = P1(),
      t = Lw(),
      n = Yw(),
      r = Fw(),
      o = Kw(),
      i = Wr(),
      a = qe(),
      s = _1(),
      l = tr(),
      u = Vr(),
      c = it(),
      d = pR(),
      f = Ur(),
      h = I1(),
      g = vR()
    function m(v, b, y, p, _, x, S) {
      var w = h(v, y),
        T = h(b, y),
        A = S.get(T)
      if (A) {
        e(v, y, A)
        return
      }
      var $ = x ? x(w, T, y + '', v, b, S) : void 0,
        P = $ === void 0
      if (P) {
        var E = a(T),
          z = !E && l(T),
          C = !E && !z && f(T)
        ;(($ = T),
          E || z || C
            ? a(w)
              ? ($ = w)
              : s(w)
                ? ($ = r(w))
                : z
                  ? ((P = !1), ($ = t(T, !0)))
                  : C
                    ? ((P = !1), ($ = n(T, !0)))
                    : ($ = [])
            : d(T) || i(T)
              ? (($ = w), i(w) ? ($ = g(w)) : (!c(w) || u(w)) && ($ = o(T)))
              : (P = !1))
      }
      ;(P && (S.set(T, $), _($, T, p, x, S), S.delete(T)), e(v, y, $))
    }
    return ((pc = m), pc)
  }
  var vc, db
  function mR() {
    if (db) return vc
    db = 1
    var e = di(),
      t = P1(),
      n = jf(),
      r = gR(),
      o = it(),
      i = On(),
      a = I1()
    function s(l, u, c, d, f) {
      l !== u &&
        n(
          u,
          function (h, g) {
            if ((f || (f = new e()), o(h))) r(l, u, g, c, s, d, f)
            else {
              var m = d ? d(a(l, g), h, g + '', l, u, f) : void 0
              ;(m === void 0 && (m = h), t(l, g, m))
            }
          },
          i
        )
    }
    return ((vc = s), vc)
  }
  var gc, fb
  function yR() {
    if (fb) return gc
    fb = 1
    var e = Si(),
      t = xi()
    function n(r) {
      return e(function (o, i) {
        var a = -1,
          s = i.length,
          l = s > 1 ? i[s - 1] : void 0,
          u = s > 2 ? i[2] : void 0
        for (
          l = r.length > 3 && typeof l == 'function' ? (s--, l) : void 0,
            u && t(i[0], i[1], u) && ((l = s < 3 ? void 0 : l), (s = 1)),
            o = Object(o);
          ++a < s;

        ) {
          var c = i[a]
          c && r(o, c, a, l)
        }
        return o
      })
    }
    return ((gc = n), gc)
  }
  var mc, hb
  function bR() {
    if (hb) return mc
    hb = 1
    var e = mR(),
      t = yR(),
      n = t(function (r, o, i) {
        e(r, o, i)
      })
    return ((mc = n), mc)
  }
  var yc, pb
  function A1() {
    if (pb) return yc
    pb = 1
    function e(t, n) {
      return t < n
    }
    return ((yc = e), yc)
  }
  var bc, vb
  function _R() {
    if (vb) return bc
    vb = 1
    var e = Xf(),
      t = A1(),
      n = Pn()
    function r(o) {
      return o && o.length ? e(o, n, t) : void 0
    }
    return ((bc = r), bc)
  }
  var _c, gb
  function wR() {
    if (gb) return _c
    gb = 1
    var e = Xf(),
      t = kt(),
      n = A1()
    function r(o, i) {
      return o && o.length ? e(o, t(i, 2), n) : void 0
    }
    return ((_c = r), _c)
  }
  var wc, mb
  function SR() {
    if (mb) return wc
    mb = 1
    var e = ht(),
      t = function () {
        return e.Date.now()
      }
    return ((wc = t), wc)
  }
  var Sc, yb
  function xR() {
    if (yb) return Sc
    yb = 1
    var e = hi(),
      t = _i(),
      n = pi(),
      r = it(),
      o = Yr()
    function i(a, s, l, u) {
      if (!r(a)) return a
      s = t(s, a)
      for (var c = -1, d = s.length, f = d - 1, h = a; h != null && ++c < d; ) {
        var g = o(s[c]),
          m = l
        if (g === '__proto__' || g === 'constructor' || g === 'prototype') return a
        if (c != f) {
          var v = h[g]
          ;((m = u ? u(v, g, h) : void 0), m === void 0 && (m = r(v) ? v : n(s[c + 1]) ? [] : {}))
        }
        ;(e(h, g, m), (h = h[g]))
      }
      return a
    }
    return ((Sc = i), Sc)
  }
  var xc, bb
  function CR() {
    if (bb) return xc
    bb = 1
    var e = wi(),
      t = xR(),
      n = _i()
    function r(o, i, a) {
      for (var s = -1, l = i.length, u = {}; ++s < l; ) {
        var c = i[s],
          d = e(o, c)
        a(d, c) && t(u, n(c, o), d)
      }
      return u
    }
    return ((xc = r), xc)
  }
  var Cc, _b
  function ER() {
    if (_b) return Cc
    _b = 1
    var e = CR(),
      t = u1()
    function n(r, o) {
      return e(r, o, function (i, a) {
        return t(r, a)
      })
    }
    return ((Cc = n), Cc)
  }
  var Ec, wb
  function $R() {
    if (wb) return Ec
    wb = 1
    var e = O1(),
      t = m1(),
      n = y1()
    function r(o) {
      return n(t(o, void 0, e), o + '')
    }
    return ((Ec = r), Ec)
  }
  var $c, Sb
  function TR() {
    if (Sb) return $c
    Sb = 1
    var e = ER(),
      t = $R(),
      n = t(function (r, o) {
        return r == null ? {} : e(r, o)
      })
    return (($c = n), $c)
  }
  var Tc, xb
  function OR() {
    if (xb) return Tc
    xb = 1
    var e = Math.ceil,
      t = Math.max
    function n(r, o, i, a) {
      for (var s = -1, l = t(e((o - r) / (i || 1)), 0), u = Array(l); l--; )
        ((u[a ? l : ++s] = r), (r += i))
      return u
    }
    return ((Tc = n), Tc)
  }
  var Oc, Cb
  function PR() {
    if (Cb) return Oc
    Cb = 1
    var e = OR(),
      t = xi(),
      n = T1()
    function r(o) {
      return function (i, a, s) {
        return (
          s && typeof s != 'number' && t(i, a, s) && (a = s = void 0),
          (i = n(i)),
          a === void 0 ? ((a = i), (i = 0)) : (a = n(a)),
          (s = s === void 0 ? (i < a ? 1 : -1) : n(s)),
          e(i, a, s, o)
        )
      }
    }
    return ((Oc = r), Oc)
  }
  var Pc, Eb
  function IR() {
    if (Eb) return Pc
    Eb = 1
    var e = PR(),
      t = e()
    return ((Pc = t), Pc)
  }
  var Ic, $b
  function AR() {
    if ($b) return Ic
    $b = 1
    function e(t, n) {
      var r = t.length
      for (t.sort(n); r--; ) t[r] = t[r].value
      return t
    }
    return ((Ic = e), Ic)
  }
  var Ac, Tb
  function NR() {
    if (Tb) return Ac
    Tb = 1
    var e = rr()
    function t(n, r) {
      if (n !== r) {
        var o = n !== void 0,
          i = n === null,
          a = n === n,
          s = e(n),
          l = r !== void 0,
          u = r === null,
          c = r === r,
          d = e(r)
        if (
          (!u && !d && !s && n > r) ||
          (s && l && c && !u && !d) ||
          (i && l && c) ||
          (!o && c) ||
          !a
        )
          return 1
        if (
          (!i && !s && !d && n < r) ||
          (d && o && a && !i && !s) ||
          (u && o && a) ||
          (!l && a) ||
          !c
        )
          return -1
      }
      return 0
    }
    return ((Ac = t), Ac)
  }
  var Nc, Ob
  function RR() {
    if (Ob) return Nc
    Ob = 1
    var e = NR()
    function t(n, r, o) {
      for (var i = -1, a = n.criteria, s = r.criteria, l = a.length, u = o.length; ++i < l; ) {
        var c = e(a[i], s[i])
        if (c) {
          if (i >= u) return c
          var d = o[i]
          return c * (d == 'desc' ? -1 : 1)
        }
      }
      return n.index - r.index
    }
    return ((Nc = t), Nc)
  }
  var Rc, Pb
  function MR() {
    if (Pb) return Rc
    Pb = 1
    var e = bi(),
      t = wi(),
      n = kt(),
      r = p1(),
      o = AR(),
      i = vi(),
      a = RR(),
      s = Pn(),
      l = qe()
    function u(c, d, f) {
      d.length
        ? (d = e(d, function (m) {
            return l(m)
              ? function (v) {
                  return t(v, m.length === 1 ? m[0] : m)
                }
              : m
          }))
        : (d = [s])
      var h = -1
      d = e(d, i(n))
      var g = r(c, function (m, v, b) {
        var y = e(d, function (p) {
          return p(m)
        })
        return { criteria: y, index: ++h, value: m }
      })
      return o(g, function (m, v) {
        return a(m, v, f)
      })
    }
    return ((Rc = u), Rc)
  }
  var Mc, Ib
  function DR() {
    if (Ib) return Mc
    Ib = 1
    var e = Uf(),
      t = MR(),
      n = Si(),
      r = xi(),
      o = n(function (i, a) {
        if (i == null) return []
        var s = a.length
        return (
          s > 1 && r(i, a[0], a[1]) ? (a = []) : s > 2 && r(a[0], a[1], a[2]) && (a = [a[0]]),
          t(i, e(a, 1), [])
        )
      })
    return ((Mc = o), Mc)
  }
  var Dc, Ab
  function BR() {
    if (Ab) return Dc
    Ab = 1
    var e = s1(),
      t = 0
    function n(r) {
      var o = ++t
      return e(r) + o
    }
    return ((Dc = n), Dc)
  }
  var Bc, Nb
  function qR() {
    if (Nb) return Bc
    Nb = 1
    function e(t, n, r) {
      for (var o = -1, i = t.length, a = n.length, s = {}; ++o < i; ) {
        var l = o < a ? n[o] : void 0
        r(s, t[o], l)
      }
      return s
    }
    return ((Bc = e), Bc)
  }
  var qc, Rb
  function zR() {
    if (Rb) return qc
    Rb = 1
    var e = hi(),
      t = qR()
    function n(r, o) {
      return t(r || [], o || [], e)
    }
    return ((qc = n), qc)
  }
  var zc, Mb
  function Ie() {
    if (Mb) return zc
    Mb = 1
    var e
    if (typeof Nf == 'function')
      try {
        e = {
          cloneDeep: eR(),
          constant: Hf(),
          defaults: tR(),
          each: e1(),
          filter: d1(),
          find: lR(),
          flatten: O1(),
          forEach: Qw(),
          forIn: uR(),
          has: f1(),
          isUndefined: h1(),
          last: cR(),
          map: v1(),
          mapValues: dR(),
          max: hR(),
          merge: bR(),
          min: _R(),
          minBy: wR(),
          now: SR(),
          pick: TR(),
          range: IR(),
          reduce: g1(),
          sortBy: DR(),
          uniqueId: BR(),
          values: w1(),
          zipObject: zR(),
        }
      } catch {}
    return (e || (e = window._), (zc = e), zc)
  }
  var Lc, Db
  function LR() {
    if (Db) return Lc
    ;((Db = 1), (Lc = e))
    function e() {
      var r = {}
      ;((r._next = r._prev = r), (this._sentinel = r))
    }
    ;((e.prototype.dequeue = function () {
      var r = this._sentinel,
        o = r._prev
      if (o !== r) return (t(o), o)
    }),
      (e.prototype.enqueue = function (r) {
        var o = this._sentinel
        ;(r._prev && r._next && t(r),
          (r._next = o._next),
          (o._next._prev = r),
          (o._next = r),
          (r._prev = o))
      }),
      (e.prototype.toString = function () {
        for (var r = [], o = this._sentinel, i = o._prev; i !== o; )
          (r.push(JSON.stringify(i, n)), (i = i._prev))
        return '[' + r.join(', ') + ']'
      }))
    function t(r) {
      ;((r._prev._next = r._next), (r._next._prev = r._prev), delete r._next, delete r._prev)
    }
    function n(r, o) {
      if (r !== '_next' && r !== '_prev') return o
    }
    return Lc
  }
  var Fc, Bb
  function FR() {
    if (Bb) return Fc
    Bb = 1
    var e = Ie(),
      t = ft().Graph,
      n = LR()
    Fc = o
    var r = e.constant(1)
    function o(u, c) {
      if (u.nodeCount() <= 1) return []
      var d = s(u, c || r),
        f = i(d.graph, d.buckets, d.zeroIdx)
      return e.flatten(
        e.map(f, function (h) {
          return u.outEdges(h.v, h.w)
        }),
        !0
      )
    }
    function i(u, c, d) {
      for (var f = [], h = c[c.length - 1], g = c[0], m; u.nodeCount(); ) {
        for (; (m = g.dequeue()); ) a(u, c, d, m)
        for (; (m = h.dequeue()); ) a(u, c, d, m)
        if (u.nodeCount()) {
          for (var v = c.length - 2; v > 0; --v)
            if (((m = c[v].dequeue()), m)) {
              f = f.concat(a(u, c, d, m, !0))
              break
            }
        }
      }
      return f
    }
    function a(u, c, d, f, h) {
      var g = h ? [] : void 0
      return (
        e.forEach(u.inEdges(f.v), function (m) {
          var v = u.edge(m),
            b = u.node(m.v)
          ;(h && g.push({ v: m.v, w: m.w }), (b.out -= v), l(c, d, b))
        }),
        e.forEach(u.outEdges(f.v), function (m) {
          var v = u.edge(m),
            b = m.w,
            y = u.node(b)
          ;((y.in -= v), l(c, d, y))
        }),
        u.removeNode(f.v),
        g
      )
    }
    function s(u, c) {
      var d = new t(),
        f = 0,
        h = 0
      ;(e.forEach(u.nodes(), function (v) {
        d.setNode(v, { v, in: 0, out: 0 })
      }),
        e.forEach(u.edges(), function (v) {
          var b = d.edge(v.v, v.w) || 0,
            y = c(v),
            p = b + y
          ;(d.setEdge(v.v, v.w, p),
            (h = Math.max(h, (d.node(v.v).out += y))),
            (f = Math.max(f, (d.node(v.w).in += y))))
        }))
      var g = e.range(h + f + 3).map(function () {
          return new n()
        }),
        m = f + 1
      return (
        e.forEach(d.nodes(), function (v) {
          l(g, m, d.node(v))
        }),
        { graph: d, buckets: g, zeroIdx: m }
      )
    }
    function l(u, c, d) {
      d.out ? (d.in ? u[d.out - d.in + c].enqueue(d) : u[u.length - 1].enqueue(d)) : u[0].enqueue(d)
    }
    return Fc
  }
  var kc, qb
  function kR() {
    if (qb) return kc
    qb = 1
    var e = Ie(),
      t = FR()
    kc = { run: n, undo: o }
    function n(i) {
      var a = i.graph().acyclicer === 'greedy' ? t(i, s(i)) : r(i)
      e.forEach(a, function (l) {
        var u = i.edge(l)
        ;(i.removeEdge(l),
          (u.forwardName = l.name),
          (u.reversed = !0),
          i.setEdge(l.w, l.v, u, e.uniqueId('rev')))
      })
      function s(l) {
        return function (u) {
          return l.edge(u).weight
        }
      }
    }
    function r(i) {
      var a = [],
        s = {},
        l = {}
      function u(c) {
        e.has(l, c) ||
          ((l[c] = !0),
          (s[c] = !0),
          e.forEach(i.outEdges(c), function (d) {
            e.has(s, d.w) ? a.push(d) : u(d.w)
          }),
          delete s[c])
      }
      return (e.forEach(i.nodes(), u), a)
    }
    function o(i) {
      e.forEach(i.edges(), function (a) {
        var s = i.edge(a)
        if (s.reversed) {
          i.removeEdge(a)
          var l = s.forwardName
          ;(delete s.reversed, delete s.forwardName, i.setEdge(a.w, a.v, s, l))
        }
      })
    }
    return kc
  }
  var Hc, zb
  function Ue() {
    if (zb) return Hc
    zb = 1
    var e = Ie(),
      t = ft().Graph
    Hc = {
      addDummyNode: n,
      simplify: r,
      asNonCompoundGraph: o,
      successorWeights: i,
      predecessorWeights: a,
      intersectRect: s,
      buildLayerMatrix: l,
      normalizeRanks: u,
      removeEmptyRanks: c,
      addBorderNode: d,
      maxRank: f,
      partition: h,
      time: g,
      notime: m,
    }
    function n(v, b, y, p) {
      var _
      do _ = e.uniqueId(p)
      while (v.hasNode(_))
      return ((y.dummy = b), v.setNode(_, y), _)
    }
    function r(v) {
      var b = new t().setGraph(v.graph())
      return (
        e.forEach(v.nodes(), function (y) {
          b.setNode(y, v.node(y))
        }),
        e.forEach(v.edges(), function (y) {
          var p = b.edge(y.v, y.w) || { weight: 0, minlen: 1 },
            _ = v.edge(y)
          b.setEdge(y.v, y.w, { weight: p.weight + _.weight, minlen: Math.max(p.minlen, _.minlen) })
        }),
        b
      )
    }
    function o(v) {
      var b = new t({ multigraph: v.isMultigraph() }).setGraph(v.graph())
      return (
        e.forEach(v.nodes(), function (y) {
          v.children(y).length || b.setNode(y, v.node(y))
        }),
        e.forEach(v.edges(), function (y) {
          b.setEdge(y, v.edge(y))
        }),
        b
      )
    }
    function i(v) {
      var b = e.map(v.nodes(), function (y) {
        var p = {}
        return (
          e.forEach(v.outEdges(y), function (_) {
            p[_.w] = (p[_.w] || 0) + v.edge(_).weight
          }),
          p
        )
      })
      return e.zipObject(v.nodes(), b)
    }
    function a(v) {
      var b = e.map(v.nodes(), function (y) {
        var p = {}
        return (
          e.forEach(v.inEdges(y), function (_) {
            p[_.v] = (p[_.v] || 0) + v.edge(_).weight
          }),
          p
        )
      })
      return e.zipObject(v.nodes(), b)
    }
    function s(v, b) {
      var y = v.x,
        p = v.y,
        _ = b.x - y,
        x = b.y - p,
        S = v.width / 2,
        w = v.height / 2
      if (!_ && !x) throw new Error('Not possible to find intersection inside of the rectangle')
      var T, A
      return (
        Math.abs(x) * S > Math.abs(_) * w
          ? (x < 0 && (w = -w), (T = (w * _) / x), (A = w))
          : (_ < 0 && (S = -S), (T = S), (A = (S * x) / _)),
        { x: y + T, y: p + A }
      )
    }
    function l(v) {
      var b = e.map(e.range(f(v) + 1), function () {
        return []
      })
      return (
        e.forEach(v.nodes(), function (y) {
          var p = v.node(y),
            _ = p.rank
          e.isUndefined(_) || (b[_][p.order] = y)
        }),
        b
      )
    }
    function u(v) {
      var b = e.min(
        e.map(v.nodes(), function (y) {
          return v.node(y).rank
        })
      )
      e.forEach(v.nodes(), function (y) {
        var p = v.node(y)
        e.has(p, 'rank') && (p.rank -= b)
      })
    }
    function c(v) {
      var b = e.min(
          e.map(v.nodes(), function (x) {
            return v.node(x).rank
          })
        ),
        y = []
      e.forEach(v.nodes(), function (x) {
        var S = v.node(x).rank - b
        ;(y[S] || (y[S] = []), y[S].push(x))
      })
      var p = 0,
        _ = v.graph().nodeRankFactor
      e.forEach(y, function (x, S) {
        e.isUndefined(x) && S % _ !== 0
          ? --p
          : p &&
            e.forEach(x, function (w) {
              v.node(w).rank += p
            })
      })
    }
    function d(v, b, y, p) {
      var _ = { width: 0, height: 0 }
      return (arguments.length >= 4 && ((_.rank = y), (_.order = p)), n(v, 'border', _, b))
    }
    function f(v) {
      return e.max(
        e.map(v.nodes(), function (b) {
          var y = v.node(b).rank
          if (!e.isUndefined(y)) return y
        })
      )
    }
    function h(v, b) {
      var y = { lhs: [], rhs: [] }
      return (
        e.forEach(v, function (p) {
          b(p) ? y.lhs.push(p) : y.rhs.push(p)
        }),
        y
      )
    }
    function g(v, b) {
      var y = e.now()
      try {
        return b()
      } finally {
        console.log(v + ' time: ' + (e.now() - y) + 'ms')
      }
    }
    function m(v, b) {
      return b()
    }
    return Hc
  }
  var jc, Lb
  function HR() {
    if (Lb) return jc
    Lb = 1
    var e = Ie(),
      t = Ue()
    jc = { run: n, undo: o }
    function n(i) {
      ;((i.graph().dummyChains = []),
        e.forEach(i.edges(), function (a) {
          r(i, a)
        }))
    }
    function r(i, a) {
      var s = a.v,
        l = i.node(s).rank,
        u = a.w,
        c = i.node(u).rank,
        d = a.name,
        f = i.edge(a),
        h = f.labelRank
      if (c !== l + 1) {
        i.removeEdge(a)
        var g, m, v
        for (v = 0, ++l; l < c; ++v, ++l)
          ((f.points = []),
            (m = { width: 0, height: 0, edgeLabel: f, edgeObj: a, rank: l }),
            (g = t.addDummyNode(i, 'edge', m, '_d')),
            l === h &&
              ((m.width = f.width),
              (m.height = f.height),
              (m.dummy = 'edge-label'),
              (m.labelpos = f.labelpos)),
            i.setEdge(s, g, { weight: f.weight }, d),
            v === 0 && i.graph().dummyChains.push(g),
            (s = g))
        i.setEdge(s, u, { weight: f.weight }, d)
      }
    }
    function o(i) {
      e.forEach(i.graph().dummyChains, function (a) {
        var s = i.node(a),
          l = s.edgeLabel,
          u
        for (i.setEdge(s.edgeObj, l); s.dummy; )
          ((u = i.successors(a)[0]),
            i.removeNode(a),
            l.points.push({ x: s.x, y: s.y }),
            s.dummy === 'edge-label' &&
              ((l.x = s.x), (l.y = s.y), (l.width = s.width), (l.height = s.height)),
            (a = u),
            (s = i.node(a)))
      })
    }
    return jc
  }
  var Vc, Fb
  function zo() {
    if (Fb) return Vc
    Fb = 1
    var e = Ie()
    Vc = { longestPath: t, slack: n }
    function t(r) {
      var o = {}
      function i(a) {
        var s = r.node(a)
        if (e.has(o, a)) return s.rank
        o[a] = !0
        var l = e.min(
          e.map(r.outEdges(a), function (u) {
            return i(u.w) - r.edge(u).minlen
          })
        )
        return (
          (l === Number.POSITIVE_INFINITY || l === void 0 || l === null) && (l = 0),
          (s.rank = l)
        )
      }
      e.forEach(r.sources(), i)
    }
    function n(r, o) {
      return r.node(o.w).rank - r.node(o.v).rank - r.edge(o).minlen
    }
    return Vc
  }
  var Gc, kb
  function N1() {
    if (kb) return Gc
    kb = 1
    var e = Ie(),
      t = ft().Graph,
      n = zo().slack
    Gc = r
    function r(s) {
      var l = new t({ directed: !1 }),
        u = s.nodes()[0],
        c = s.nodeCount()
      l.setNode(u, {})
      for (var d, f; o(l, s) < c; )
        ((d = i(l, s)), (f = l.hasNode(d.v) ? n(s, d) : -n(s, d)), a(l, s, f))
      return l
    }
    function o(s, l) {
      function u(c) {
        e.forEach(l.nodeEdges(c), function (d) {
          var f = d.v,
            h = c === f ? d.w : f
          !s.hasNode(h) && !n(l, d) && (s.setNode(h, {}), s.setEdge(c, h, {}), u(h))
        })
      }
      return (e.forEach(s.nodes(), u), s.nodeCount())
    }
    function i(s, l) {
      return e.minBy(l.edges(), function (u) {
        if (s.hasNode(u.v) !== s.hasNode(u.w)) return n(l, u)
      })
    }
    function a(s, l, u) {
      e.forEach(s.nodes(), function (c) {
        l.node(c).rank += u
      })
    }
    return Gc
  }
  var Wc, Hb
  function jR() {
    if (Hb) return Wc
    Hb = 1
    var e = Ie(),
      t = N1(),
      n = zo().slack,
      r = zo().longestPath,
      o = ft().alg.preorder,
      i = ft().alg.postorder,
      a = Ue().simplify
    ;((Wc = s),
      (s.initLowLimValues = d),
      (s.initCutValues = l),
      (s.calcCutValue = c),
      (s.leaveEdge = h),
      (s.enterEdge = g),
      (s.exchangeEdges = m))
    function s(p) {
      ;((p = a(p)), r(p))
      var _ = t(p)
      ;(d(_), l(_, p))
      for (var x, S; (x = h(_)); ) ((S = g(_, p, x)), m(_, p, x, S))
    }
    function l(p, _) {
      var x = i(p, p.nodes())
      ;((x = x.slice(0, x.length - 1)),
        e.forEach(x, function (S) {
          u(p, _, S)
        }))
    }
    function u(p, _, x) {
      var S = p.node(x),
        w = S.parent
      p.edge(x, w).cutvalue = c(p, _, x)
    }
    function c(p, _, x) {
      var S = p.node(x),
        w = S.parent,
        T = !0,
        A = _.edge(x, w),
        $ = 0
      return (
        A || ((T = !1), (A = _.edge(w, x))),
        ($ = A.weight),
        e.forEach(_.nodeEdges(x), function (P) {
          var E = P.v === x,
            z = E ? P.w : P.v
          if (z !== w) {
            var C = E === T,
              R = _.edge(P).weight
            if ((($ += C ? R : -R), b(p, x, z))) {
              var N = p.edge(x, z).cutvalue
              $ += C ? -N : N
            }
          }
        }),
        $
      )
    }
    function d(p, _) {
      ;(arguments.length < 2 && (_ = p.nodes()[0]), f(p, {}, 1, _))
    }
    function f(p, _, x, S, w) {
      var T = x,
        A = p.node(S)
      return (
        (_[S] = !0),
        e.forEach(p.neighbors(S), function ($) {
          e.has(_, $) || (x = f(p, _, x, $, S))
        }),
        (A.low = T),
        (A.lim = x++),
        w ? (A.parent = w) : delete A.parent,
        x
      )
    }
    function h(p) {
      return e.find(p.edges(), function (_) {
        return p.edge(_).cutvalue < 0
      })
    }
    function g(p, _, x) {
      var S = x.v,
        w = x.w
      _.hasEdge(S, w) || ((S = x.w), (w = x.v))
      var T = p.node(S),
        A = p.node(w),
        $ = T,
        P = !1
      T.lim > A.lim && (($ = A), (P = !0))
      var E = e.filter(_.edges(), function (z) {
        return P === y(p, p.node(z.v), $) && P !== y(p, p.node(z.w), $)
      })
      return e.minBy(E, function (z) {
        return n(_, z)
      })
    }
    function m(p, _, x, S) {
      var w = x.v,
        T = x.w
      ;(p.removeEdge(w, T), p.setEdge(S.v, S.w, {}), d(p), l(p, _), v(p, _))
    }
    function v(p, _) {
      var x = e.find(p.nodes(), function (w) {
          return !_.node(w).parent
        }),
        S = o(p, x)
      ;((S = S.slice(1)),
        e.forEach(S, function (w) {
          var T = p.node(w).parent,
            A = _.edge(w, T),
            $ = !1
          ;(A || ((A = _.edge(T, w)), ($ = !0)),
            (_.node(w).rank = _.node(T).rank + ($ ? A.minlen : -A.minlen)))
        }))
    }
    function b(p, _, x) {
      return p.hasEdge(_, x)
    }
    function y(p, _, x) {
      return x.low <= _.lim && _.lim <= x.lim
    }
    return Wc
  }
  var Uc, jb
  function VR() {
    if (jb) return Uc
    jb = 1
    var e = zo(),
      t = e.longestPath,
      n = N1(),
      r = jR()
    Uc = o
    function o(l) {
      switch (l.graph().ranker) {
        case 'network-simplex':
          s(l)
          break
        case 'tight-tree':
          a(l)
          break
        case 'longest-path':
          i(l)
          break
        default:
          s(l)
      }
    }
    var i = t
    function a(l) {
      ;(t(l), n(l))
    }
    function s(l) {
      r(l)
    }
    return Uc
  }
  var Yc, Vb
  function GR() {
    if (Vb) return Yc
    Vb = 1
    var e = Ie()
    Yc = t
    function t(o) {
      var i = r(o)
      e.forEach(o.graph().dummyChains, function (a) {
        for (
          var s = o.node(a),
            l = s.edgeObj,
            u = n(o, i, l.v, l.w),
            c = u.path,
            d = u.lca,
            f = 0,
            h = c[f],
            g = !0;
          a !== l.w;

        ) {
          if (((s = o.node(a)), g)) {
            for (; (h = c[f]) !== d && o.node(h).maxRank < s.rank; ) f++
            h === d && (g = !1)
          }
          if (!g) {
            for (; f < c.length - 1 && o.node((h = c[f + 1])).minRank <= s.rank; ) f++
            h = c[f]
          }
          ;(o.setParent(a, h), (a = o.successors(a)[0]))
        }
      })
    }
    function n(o, i, a, s) {
      var l = [],
        u = [],
        c = Math.min(i[a].low, i[s].low),
        d = Math.max(i[a].lim, i[s].lim),
        f,
        h
      f = a
      do ((f = o.parent(f)), l.push(f))
      while (f && (i[f].low > c || d > i[f].lim))
      for (h = f, f = s; (f = o.parent(f)) !== h; ) u.push(f)
      return { path: l.concat(u.reverse()), lca: h }
    }
    function r(o) {
      var i = {},
        a = 0
      function s(l) {
        var u = a
        ;(e.forEach(o.children(l), s), (i[l] = { low: u, lim: a++ }))
      }
      return (e.forEach(o.children(), s), i)
    }
    return Yc
  }
  var Xc, Gb
  function WR() {
    if (Gb) return Xc
    Gb = 1
    var e = Ie(),
      t = Ue()
    Xc = { run: n, cleanup: a }
    function n(s) {
      var l = t.addDummyNode(s, 'root', {}, '_root'),
        u = o(s),
        c = e.max(e.values(u)) - 1,
        d = 2 * c + 1
      ;((s.graph().nestingRoot = l),
        e.forEach(s.edges(), function (h) {
          s.edge(h).minlen *= d
        }))
      var f = i(s) + 1
      ;(e.forEach(s.children(), function (h) {
        r(s, l, d, f, c, u, h)
      }),
        (s.graph().nodeRankFactor = d))
    }
    function r(s, l, u, c, d, f, h) {
      var g = s.children(h)
      if (!g.length) {
        h !== l && s.setEdge(l, h, { weight: 0, minlen: u })
        return
      }
      var m = t.addBorderNode(s, '_bt'),
        v = t.addBorderNode(s, '_bb'),
        b = s.node(h)
      ;(s.setParent(m, h),
        (b.borderTop = m),
        s.setParent(v, h),
        (b.borderBottom = v),
        e.forEach(g, function (y) {
          r(s, l, u, c, d, f, y)
          var p = s.node(y),
            _ = p.borderTop ? p.borderTop : y,
            x = p.borderBottom ? p.borderBottom : y,
            S = p.borderTop ? c : 2 * c,
            w = _ !== x ? 1 : d - f[h] + 1
          ;(s.setEdge(m, _, { weight: S, minlen: w, nestingEdge: !0 }),
            s.setEdge(x, v, { weight: S, minlen: w, nestingEdge: !0 }))
        }),
        s.parent(h) || s.setEdge(l, m, { weight: 0, minlen: d + f[h] }))
    }
    function o(s) {
      var l = {}
      function u(c, d) {
        var f = s.children(c)
        ;(f &&
          f.length &&
          e.forEach(f, function (h) {
            u(h, d + 1)
          }),
          (l[c] = d))
      }
      return (
        e.forEach(s.children(), function (c) {
          u(c, 1)
        }),
        l
      )
    }
    function i(s) {
      return e.reduce(
        s.edges(),
        function (l, u) {
          return l + s.edge(u).weight
        },
        0
      )
    }
    function a(s) {
      var l = s.graph()
      ;(s.removeNode(l.nestingRoot),
        delete l.nestingRoot,
        e.forEach(s.edges(), function (u) {
          var c = s.edge(u)
          c.nestingEdge && s.removeEdge(u)
        }))
    }
    return Xc
  }
  var Kc, Wb
  function UR() {
    if (Wb) return Kc
    Wb = 1
    var e = Ie(),
      t = Ue()
    Kc = n
    function n(o) {
      function i(a) {
        var s = o.children(a),
          l = o.node(a)
        if ((s.length && e.forEach(s, i), e.has(l, 'minRank'))) {
          ;((l.borderLeft = []), (l.borderRight = []))
          for (var u = l.minRank, c = l.maxRank + 1; u < c; ++u)
            (r(o, 'borderLeft', '_bl', a, l, u), r(o, 'borderRight', '_br', a, l, u))
        }
      }
      e.forEach(o.children(), i)
    }
    function r(o, i, a, s, l, u) {
      var c = { width: 0, height: 0, rank: u, borderType: i },
        d = l[i][u - 1],
        f = t.addDummyNode(o, 'border', c, a)
      ;((l[i][u] = f), o.setParent(f, s), d && o.setEdge(d, f, { weight: 1 }))
    }
    return Kc
  }
  var Zc, Ub
  function YR() {
    if (Ub) return Zc
    Ub = 1
    var e = Ie()
    Zc = { adjust: t, undo: n }
    function t(u) {
      var c = u.graph().rankdir.toLowerCase()
      ;(c === 'lr' || c === 'rl') && r(u)
    }
    function n(u) {
      var c = u.graph().rankdir.toLowerCase()
      ;((c === 'bt' || c === 'rl') && i(u), (c === 'lr' || c === 'rl') && (s(u), r(u)))
    }
    function r(u) {
      ;(e.forEach(u.nodes(), function (c) {
        o(u.node(c))
      }),
        e.forEach(u.edges(), function (c) {
          o(u.edge(c))
        }))
    }
    function o(u) {
      var c = u.width
      ;((u.width = u.height), (u.height = c))
    }
    function i(u) {
      ;(e.forEach(u.nodes(), function (c) {
        a(u.node(c))
      }),
        e.forEach(u.edges(), function (c) {
          var d = u.edge(c)
          ;(e.forEach(d.points, a), e.has(d, 'y') && a(d))
        }))
    }
    function a(u) {
      u.y = -u.y
    }
    function s(u) {
      ;(e.forEach(u.nodes(), function (c) {
        l(u.node(c))
      }),
        e.forEach(u.edges(), function (c) {
          var d = u.edge(c)
          ;(e.forEach(d.points, l), e.has(d, 'x') && l(d))
        }))
    }
    function l(u) {
      var c = u.x
      ;((u.x = u.y), (u.y = c))
    }
    return Zc
  }
  var Jc, Yb
  function XR() {
    if (Yb) return Jc
    Yb = 1
    var e = Ie()
    Jc = t
    function t(n) {
      var r = {},
        o = e.filter(n.nodes(), function (u) {
          return !n.children(u).length
        }),
        i = e.max(
          e.map(o, function (u) {
            return n.node(u).rank
          })
        ),
        a = e.map(e.range(i + 1), function () {
          return []
        })
      function s(u) {
        if (!e.has(r, u)) {
          r[u] = !0
          var c = n.node(u)
          ;(a[c.rank].push(u), e.forEach(n.successors(u), s))
        }
      }
      var l = e.sortBy(o, function (u) {
        return n.node(u).rank
      })
      return (e.forEach(l, s), a)
    }
    return Jc
  }
  var Qc, Xb
  function KR() {
    if (Xb) return Qc
    Xb = 1
    var e = Ie()
    Qc = t
    function t(r, o) {
      for (var i = 0, a = 1; a < o.length; ++a) i += n(r, o[a - 1], o[a])
      return i
    }
    function n(r, o, i) {
      for (
        var a = e.zipObject(
            i,
            e.map(i, function (f, h) {
              return h
            })
          ),
          s = e.flatten(
            e.map(o, function (f) {
              return e.sortBy(
                e.map(r.outEdges(f), function (h) {
                  return { pos: a[h.w], weight: r.edge(h).weight }
                }),
                'pos'
              )
            }),
            !0
          ),
          l = 1;
        l < i.length;

      )
        l <<= 1
      var u = 2 * l - 1
      l -= 1
      var c = e.map(new Array(u), function () {
          return 0
        }),
        d = 0
      return (
        e.forEach(
          s.forEach(function (f) {
            var h = f.pos + l
            c[h] += f.weight
            for (var g = 0; h > 0; )
              (h % 2 && (g += c[h + 1]), (h = (h - 1) >> 1), (c[h] += f.weight))
            d += f.weight * g
          })
        ),
        d
      )
    }
    return Qc
  }
  var ed, Kb
  function ZR() {
    if (Kb) return ed
    Kb = 1
    var e = Ie()
    ed = t
    function t(n, r) {
      return e.map(r, function (o) {
        var i = n.inEdges(o)
        if (i.length) {
          var a = e.reduce(
            i,
            function (s, l) {
              var u = n.edge(l),
                c = n.node(l.v)
              return { sum: s.sum + u.weight * c.order, weight: s.weight + u.weight }
            },
            { sum: 0, weight: 0 }
          )
          return { v: o, barycenter: a.sum / a.weight, weight: a.weight }
        } else return { v: o }
      })
    }
    return ed
  }
  var td, Zb
  function JR() {
    if (Zb) return td
    Zb = 1
    var e = Ie()
    td = t
    function t(o, i) {
      var a = {}
      ;(e.forEach(o, function (l, u) {
        var c = (a[l.v] = { indegree: 0, in: [], out: [], vs: [l.v], i: u })
        e.isUndefined(l.barycenter) || ((c.barycenter = l.barycenter), (c.weight = l.weight))
      }),
        e.forEach(i.edges(), function (l) {
          var u = a[l.v],
            c = a[l.w]
          !e.isUndefined(u) && !e.isUndefined(c) && (c.indegree++, u.out.push(a[l.w]))
        }))
      var s = e.filter(a, function (l) {
        return !l.indegree
      })
      return n(s)
    }
    function n(o) {
      var i = []
      function a(u) {
        return function (c) {
          c.merged ||
            ((e.isUndefined(c.barycenter) ||
              e.isUndefined(u.barycenter) ||
              c.barycenter >= u.barycenter) &&
              r(u, c))
        }
      }
      function s(u) {
        return function (c) {
          ;(c.in.push(u), --c.indegree === 0 && o.push(c))
        }
      }
      for (; o.length; ) {
        var l = o.pop()
        ;(i.push(l), e.forEach(l.in.reverse(), a(l)), e.forEach(l.out, s(l)))
      }
      return e.map(
        e.filter(i, function (u) {
          return !u.merged
        }),
        function (u) {
          return e.pick(u, ['vs', 'i', 'barycenter', 'weight'])
        }
      )
    }
    function r(o, i) {
      var a = 0,
        s = 0
      ;(o.weight && ((a += o.barycenter * o.weight), (s += o.weight)),
        i.weight && ((a += i.barycenter * i.weight), (s += i.weight)),
        (o.vs = i.vs.concat(o.vs)),
        (o.barycenter = a / s),
        (o.weight = s),
        (o.i = Math.min(i.i, o.i)),
        (i.merged = !0))
    }
    return td
  }
  var nd, Jb
  function QR() {
    if (Jb) return nd
    Jb = 1
    var e = Ie(),
      t = Ue()
    nd = n
    function n(i, a) {
      var s = t.partition(i, function (m) {
          return e.has(m, 'barycenter')
        }),
        l = s.lhs,
        u = e.sortBy(s.rhs, function (m) {
          return -m.i
        }),
        c = [],
        d = 0,
        f = 0,
        h = 0
      ;(l.sort(o(!!a)),
        (h = r(c, u, h)),
        e.forEach(l, function (m) {
          ;((h += m.vs.length),
            c.push(m.vs),
            (d += m.barycenter * m.weight),
            (f += m.weight),
            (h = r(c, u, h)))
        }))
      var g = { vs: e.flatten(c, !0) }
      return (f && ((g.barycenter = d / f), (g.weight = f)), g)
    }
    function r(i, a, s) {
      for (var l; a.length && (l = e.last(a)).i <= s; ) (a.pop(), i.push(l.vs), s++)
      return s
    }
    function o(i) {
      return function (a, s) {
        return a.barycenter < s.barycenter
          ? -1
          : a.barycenter > s.barycenter
            ? 1
            : i
              ? s.i - a.i
              : a.i - s.i
      }
    }
    return nd
  }
  var rd, Qb
  function eM() {
    if (Qb) return rd
    Qb = 1
    var e = Ie(),
      t = ZR(),
      n = JR(),
      r = QR()
    rd = o
    function o(s, l, u, c) {
      var d = s.children(l),
        f = s.node(l),
        h = f ? f.borderLeft : void 0,
        g = f ? f.borderRight : void 0,
        m = {}
      h &&
        (d = e.filter(d, function (x) {
          return x !== h && x !== g
        }))
      var v = t(s, d)
      e.forEach(v, function (x) {
        if (s.children(x.v).length) {
          var S = o(s, x.v, u, c)
          ;((m[x.v] = S), e.has(S, 'barycenter') && a(x, S))
        }
      })
      var b = n(v, u)
      i(b, m)
      var y = r(b, c)
      if (h && ((y.vs = e.flatten([h, y.vs, g], !0)), s.predecessors(h).length)) {
        var p = s.node(s.predecessors(h)[0]),
          _ = s.node(s.predecessors(g)[0])
        ;(e.has(y, 'barycenter') || ((y.barycenter = 0), (y.weight = 0)),
          (y.barycenter = (y.barycenter * y.weight + p.order + _.order) / (y.weight + 2)),
          (y.weight += 2))
      }
      return y
    }
    function i(s, l) {
      e.forEach(s, function (u) {
        u.vs = e.flatten(
          u.vs.map(function (c) {
            return l[c] ? l[c].vs : c
          }),
          !0
        )
      })
    }
    function a(s, l) {
      e.isUndefined(s.barycenter)
        ? ((s.barycenter = l.barycenter), (s.weight = l.weight))
        : ((s.barycenter =
            (s.barycenter * s.weight + l.barycenter * l.weight) / (s.weight + l.weight)),
          (s.weight += l.weight))
    }
    return rd
  }
  var od, e0
  function tM() {
    if (e0) return od
    e0 = 1
    var e = Ie(),
      t = ft().Graph
    od = n
    function n(o, i, a) {
      var s = r(o),
        l = new t({ compound: !0 }).setGraph({ root: s }).setDefaultNodeLabel(function (u) {
          return o.node(u)
        })
      return (
        e.forEach(o.nodes(), function (u) {
          var c = o.node(u),
            d = o.parent(u)
          ;(c.rank === i || (c.minRank <= i && i <= c.maxRank)) &&
            (l.setNode(u),
            l.setParent(u, d || s),
            e.forEach(o[a](u), function (f) {
              var h = f.v === u ? f.w : f.v,
                g = l.edge(h, u),
                m = e.isUndefined(g) ? 0 : g.weight
              l.setEdge(h, u, { weight: o.edge(f).weight + m })
            }),
            e.has(c, 'minRank') &&
              l.setNode(u, { borderLeft: c.borderLeft[i], borderRight: c.borderRight[i] }))
        }),
        l
      )
    }
    function r(o) {
      for (var i; o.hasNode((i = e.uniqueId('_root'))); );
      return i
    }
    return od
  }
  var id, t0
  function nM() {
    if (t0) return id
    t0 = 1
    var e = Ie()
    id = t
    function t(n, r, o) {
      var i = {},
        a
      e.forEach(o, function (s) {
        for (var l = n.parent(s), u, c; l; ) {
          if (
            ((u = n.parent(l)), u ? ((c = i[u]), (i[u] = l)) : ((c = a), (a = l)), c && c !== l)
          ) {
            r.setEdge(c, l)
            return
          }
          l = u
        }
      })
    }
    return id
  }
  var ad, n0
  function rM() {
    if (n0) return ad
    n0 = 1
    var e = Ie(),
      t = XR(),
      n = KR(),
      r = eM(),
      o = tM(),
      i = nM(),
      a = ft().Graph,
      s = Ue()
    ad = l
    function l(f) {
      var h = s.maxRank(f),
        g = u(f, e.range(1, h + 1), 'inEdges'),
        m = u(f, e.range(h - 1, -1, -1), 'outEdges'),
        v = t(f)
      d(f, v)
      for (var b = Number.POSITIVE_INFINITY, y, p = 0, _ = 0; _ < 4; ++p, ++_) {
        ;(c(p % 2 ? g : m, p % 4 >= 2), (v = s.buildLayerMatrix(f)))
        var x = n(f, v)
        x < b && ((_ = 0), (y = e.cloneDeep(v)), (b = x))
      }
      d(f, y)
    }
    function u(f, h, g) {
      return e.map(h, function (m) {
        return o(f, m, g)
      })
    }
    function c(f, h) {
      var g = new a()
      e.forEach(f, function (m) {
        var v = m.graph().root,
          b = r(m, v, g, h)
        ;(e.forEach(b.vs, function (y, p) {
          m.node(y).order = p
        }),
          i(m, g, b.vs))
      })
    }
    function d(f, h) {
      e.forEach(h, function (g) {
        e.forEach(g, function (m, v) {
          f.node(m).order = v
        })
      })
    }
    return ad
  }
  var sd, r0
  function oM() {
    if (r0) return sd
    r0 = 1
    var e = Ie(),
      t = ft().Graph,
      n = Ue()
    sd = {
      positionX: g,
      findType1Conflicts: r,
      findType2Conflicts: o,
      addConflict: a,
      hasConflict: s,
      verticalAlignment: l,
      horizontalCompaction: u,
      alignCoordinates: f,
      findSmallestWidthAlignment: d,
      balance: h,
    }
    function r(b, y) {
      var p = {}
      function _(x, S) {
        var w = 0,
          T = 0,
          A = x.length,
          $ = e.last(S)
        return (
          e.forEach(S, function (P, E) {
            var z = i(b, P),
              C = z ? b.node(z).order : A
            ;(z || P === $) &&
              (e.forEach(S.slice(T, E + 1), function (R) {
                e.forEach(b.predecessors(R), function (N) {
                  var j = b.node(N),
                    V = j.order
                  ;(V < w || C < V) && !(j.dummy && b.node(R).dummy) && a(p, N, R)
                })
              }),
              (T = E + 1),
              (w = C))
          }),
          S
        )
      }
      return (e.reduce(y, _), p)
    }
    function o(b, y) {
      var p = {}
      function _(S, w, T, A, $) {
        var P
        e.forEach(e.range(w, T), function (E) {
          ;((P = S[E]),
            b.node(P).dummy &&
              e.forEach(b.predecessors(P), function (z) {
                var C = b.node(z)
                C.dummy && (C.order < A || C.order > $) && a(p, z, P)
              }))
        })
      }
      function x(S, w) {
        var T = -1,
          A,
          $ = 0
        return (
          e.forEach(w, function (P, E) {
            if (b.node(P).dummy === 'border') {
              var z = b.predecessors(P)
              z.length && ((A = b.node(z[0]).order), _(w, $, E, T, A), ($ = E), (T = A))
            }
            _(w, $, w.length, A, S.length)
          }),
          w
        )
      }
      return (e.reduce(y, x), p)
    }
    function i(b, y) {
      if (b.node(y).dummy)
        return e.find(b.predecessors(y), function (p) {
          return b.node(p).dummy
        })
    }
    function a(b, y, p) {
      if (y > p) {
        var _ = y
        ;((y = p), (p = _))
      }
      var x = b[y]
      ;(x || (b[y] = x = {}), (x[p] = !0))
    }
    function s(b, y, p) {
      if (y > p) {
        var _ = y
        ;((y = p), (p = _))
      }
      return e.has(b[y], p)
    }
    function l(b, y, p, _) {
      var x = {},
        S = {},
        w = {}
      return (
        e.forEach(y, function (T) {
          e.forEach(T, function (A, $) {
            ;((x[A] = A), (S[A] = A), (w[A] = $))
          })
        }),
        e.forEach(y, function (T) {
          var A = -1
          e.forEach(T, function ($) {
            var P = _($)
            if (P.length) {
              P = e.sortBy(P, function (N) {
                return w[N]
              })
              for (var E = (P.length - 1) / 2, z = Math.floor(E), C = Math.ceil(E); z <= C; ++z) {
                var R = P[z]
                S[$] === $ &&
                  A < w[R] &&
                  !s(p, $, R) &&
                  ((S[R] = $), (S[$] = x[$] = x[R]), (A = w[R]))
              }
            }
          })
        }),
        { root: x, align: S }
      )
    }
    function u(b, y, p, _, x) {
      var S = {},
        w = c(b, y, p, x),
        T = x ? 'borderLeft' : 'borderRight'
      function A(E, z) {
        for (var C = w.nodes(), R = C.pop(), N = {}; R; )
          (N[R] ? E(R) : ((N[R] = !0), C.push(R), (C = C.concat(z(R)))), (R = C.pop()))
      }
      function $(E) {
        S[E] = w.inEdges(E).reduce(function (z, C) {
          return Math.max(z, S[C.v] + w.edge(C))
        }, 0)
      }
      function P(E) {
        var z = w.outEdges(E).reduce(function (R, N) {
            return Math.min(R, S[N.w] - w.edge(N))
          }, Number.POSITIVE_INFINITY),
          C = b.node(E)
        z !== Number.POSITIVE_INFINITY && C.borderType !== T && (S[E] = Math.max(S[E], z))
      }
      return (
        A($, w.predecessors.bind(w)),
        A(P, w.successors.bind(w)),
        e.forEach(_, function (E) {
          S[E] = S[p[E]]
        }),
        S
      )
    }
    function c(b, y, p, _) {
      var x = new t(),
        S = b.graph(),
        w = m(S.nodesep, S.edgesep, _)
      return (
        e.forEach(y, function (T) {
          var A
          e.forEach(T, function ($) {
            var P = p[$]
            if ((x.setNode(P), A)) {
              var E = p[A],
                z = x.edge(E, P)
              x.setEdge(E, P, Math.max(w(b, $, A), z || 0))
            }
            A = $
          })
        }),
        x
      )
    }
    function d(b, y) {
      return e.minBy(e.values(y), function (p) {
        var _ = Number.NEGATIVE_INFINITY,
          x = Number.POSITIVE_INFINITY
        return (
          e.forIn(p, function (S, w) {
            var T = v(b, w) / 2
            ;((_ = Math.max(S + T, _)), (x = Math.min(S - T, x)))
          }),
          _ - x
        )
      })
    }
    function f(b, y) {
      var p = e.values(y),
        _ = e.min(p),
        x = e.max(p)
      e.forEach(['u', 'd'], function (S) {
        e.forEach(['l', 'r'], function (w) {
          var T = S + w,
            A = b[T],
            $
          if (A !== y) {
            var P = e.values(A)
            ;(($ = w === 'l' ? _ - e.min(P) : x - e.max(P)),
              $ &&
                (b[T] = e.mapValues(A, function (E) {
                  return E + $
                })))
          }
        })
      })
    }
    function h(b, y) {
      return e.mapValues(b.ul, function (p, _) {
        if (y) return b[y.toLowerCase()][_]
        var x = e.sortBy(e.map(b, _))
        return (x[1] + x[2]) / 2
      })
    }
    function g(b) {
      var y = n.buildLayerMatrix(b),
        p = e.merge(r(b, y), o(b, y)),
        _ = {},
        x
      e.forEach(['u', 'd'], function (w) {
        ;((x = w === 'u' ? y : e.values(y).reverse()),
          e.forEach(['l', 'r'], function (T) {
            T === 'r' &&
              (x = e.map(x, function (E) {
                return e.values(E).reverse()
              }))
            var A = (w === 'u' ? b.predecessors : b.successors).bind(b),
              $ = l(b, x, p, A),
              P = u(b, x, $.root, $.align, T === 'r')
            ;(T === 'r' &&
              (P = e.mapValues(P, function (E) {
                return -E
              })),
              (_[w + T] = P))
          }))
      })
      var S = d(b, _)
      return (f(_, S), h(_, b.graph().align))
    }
    function m(b, y, p) {
      return function (_, x, S) {
        var w = _.node(x),
          T = _.node(S),
          A = 0,
          $
        if (((A += w.width / 2), e.has(w, 'labelpos')))
          switch (w.labelpos.toLowerCase()) {
            case 'l':
              $ = -w.width / 2
              break
            case 'r':
              $ = w.width / 2
              break
          }
        if (
          ($ && (A += p ? $ : -$),
          ($ = 0),
          (A += (w.dummy ? y : b) / 2),
          (A += (T.dummy ? y : b) / 2),
          (A += T.width / 2),
          e.has(T, 'labelpos'))
        )
          switch (T.labelpos.toLowerCase()) {
            case 'l':
              $ = T.width / 2
              break
            case 'r':
              $ = -T.width / 2
              break
          }
        return ($ && (A += p ? $ : -$), ($ = 0), A)
      }
    }
    function v(b, y) {
      return b.node(y).width
    }
    return sd
  }
  var ld, o0
  function iM() {
    if (o0) return ld
    o0 = 1
    var e = Ie(),
      t = Ue(),
      n = oM().positionX
    ld = r
    function r(i) {
      ;((i = t.asNonCompoundGraph(i)),
        o(i),
        e.forEach(n(i), function (a, s) {
          i.node(s).x = a
        }))
    }
    function o(i) {
      var a = t.buildLayerMatrix(i),
        s = i.graph().ranksep,
        l = 0
      e.forEach(a, function (u) {
        var c = e.max(
          e.map(u, function (d) {
            return i.node(d).height
          })
        )
        ;(e.forEach(u, function (d) {
          i.node(d).y = l + c / 2
        }),
          (l += c + s))
      })
    }
    return ld
  }
  var ud, i0
  function aM() {
    if (i0) return ud
    i0 = 1
    var e = Ie(),
      t = kR(),
      n = HR(),
      r = VR(),
      o = Ue().normalizeRanks,
      i = GR(),
      a = Ue().removeEmptyRanks,
      s = WR(),
      l = UR(),
      u = YR(),
      c = rM(),
      d = iM(),
      f = Ue(),
      h = ft().Graph
    ud = g
    function g(B, L) {
      var k = L && L.debugTiming ? f.time : f.notime
      k('layout', function () {
        var U = k('  buildLayoutGraph', function () {
          return A(B)
        })
        ;(k('  runLayout', function () {
          m(U, k)
        }),
          k('  updateInputGraph', function () {
            v(B, U)
          }))
      })
    }
    function m(B, L) {
      ;(L('    makeSpaceForEdgeLabels', function () {
        $(B)
      }),
        L('    removeSelfEdges', function () {
          H(B)
        }),
        L('    acyclic', function () {
          t.run(B)
        }),
        L('    nestingGraph.run', function () {
          s.run(B)
        }),
        L('    rank', function () {
          r(f.asNonCompoundGraph(B))
        }),
        L('    injectEdgeLabelProxies', function () {
          P(B)
        }),
        L('    removeEmptyRanks', function () {
          a(B)
        }),
        L('    nestingGraph.cleanup', function () {
          s.cleanup(B)
        }),
        L('    normalizeRanks', function () {
          o(B)
        }),
        L('    assignRankMinMax', function () {
          E(B)
        }),
        L('    removeEdgeLabelProxies', function () {
          z(B)
        }),
        L('    normalize.run', function () {
          n.run(B)
        }),
        L('    parentDummyChains', function () {
          i(B)
        }),
        L('    addBorderSegments', function () {
          l(B)
        }),
        L('    order', function () {
          c(B)
        }),
        L('    insertSelfEdges', function () {
          G(B)
        }),
        L('    adjustCoordinateSystem', function () {
          u.adjust(B)
        }),
        L('    position', function () {
          d(B)
        }),
        L('    positionSelfEdges', function () {
          Y(B)
        }),
        L('    removeBorderNodes', function () {
          V(B)
        }),
        L('    normalize.undo', function () {
          n.undo(B)
        }),
        L('    fixupEdgeLabelCoords', function () {
          N(B)
        }),
        L('    undoCoordinateSystem', function () {
          u.undo(B)
        }),
        L('    translateGraph', function () {
          C(B)
        }),
        L('    assignNodeIntersects', function () {
          R(B)
        }),
        L('    reversePoints', function () {
          j(B)
        }),
        L('    acyclic.undo', function () {
          t.undo(B)
        }))
    }
    function v(B, L) {
      ;(e.forEach(B.nodes(), function (k) {
        var U = B.node(k),
          J = L.node(k)
        U &&
          ((U.x = J.x),
          (U.y = J.y),
          L.children(k).length && ((U.width = J.width), (U.height = J.height)))
      }),
        e.forEach(B.edges(), function (k) {
          var U = B.edge(k),
            J = L.edge(k)
          ;((U.points = J.points), e.has(J, 'x') && ((U.x = J.x), (U.y = J.y)))
        }),
        (B.graph().width = L.graph().width),
        (B.graph().height = L.graph().height))
    }
    var b = ['nodesep', 'edgesep', 'ranksep', 'marginx', 'marginy'],
      y = { ranksep: 50, edgesep: 20, nodesep: 50, rankdir: 'tb' },
      p = ['acyclicer', 'ranker', 'rankdir', 'align'],
      _ = ['width', 'height'],
      x = { width: 0, height: 0 },
      S = ['minlen', 'weight', 'width', 'height', 'labeloffset'],
      w = { minlen: 1, weight: 1, width: 0, height: 0, labeloffset: 10, labelpos: 'r' },
      T = ['labelpos']
    function A(B) {
      var L = new h({ multigraph: !0, compound: !0 }),
        k = ne(B.graph())
      return (
        L.setGraph(e.merge({}, y, Z(k, b), e.pick(k, p))),
        e.forEach(B.nodes(), function (U) {
          var J = ne(B.node(U))
          ;(L.setNode(U, e.defaults(Z(J, _), x)), L.setParent(U, B.parent(U)))
        }),
        e.forEach(B.edges(), function (U) {
          var J = ne(B.edge(U))
          L.setEdge(U, e.merge({}, w, Z(J, S), e.pick(J, T)))
        }),
        L
      )
    }
    function $(B) {
      var L = B.graph()
      ;((L.ranksep /= 2),
        e.forEach(B.edges(), function (k) {
          var U = B.edge(k)
          ;((U.minlen *= 2),
            U.labelpos.toLowerCase() !== 'c' &&
              (L.rankdir === 'TB' || L.rankdir === 'BT'
                ? (U.width += U.labeloffset)
                : (U.height += U.labeloffset)))
        }))
    }
    function P(B) {
      e.forEach(B.edges(), function (L) {
        var k = B.edge(L)
        if (k.width && k.height) {
          var U = B.node(L.v),
            J = B.node(L.w),
            re = { rank: (J.rank - U.rank) / 2 + U.rank, e: L }
          f.addDummyNode(B, 'edge-proxy', re, '_ep')
        }
      })
    }
    function E(B) {
      var L = 0
      ;(e.forEach(B.nodes(), function (k) {
        var U = B.node(k)
        U.borderTop &&
          ((U.minRank = B.node(U.borderTop).rank),
          (U.maxRank = B.node(U.borderBottom).rank),
          (L = e.max(L, U.maxRank)))
      }),
        (B.graph().maxRank = L))
    }
    function z(B) {
      e.forEach(B.nodes(), function (L) {
        var k = B.node(L)
        k.dummy === 'edge-proxy' && ((B.edge(k.e).labelRank = k.rank), B.removeNode(L))
      })
    }
    function C(B) {
      var L = Number.POSITIVE_INFINITY,
        k = 0,
        U = Number.POSITIVE_INFINITY,
        J = 0,
        re = B.graph(),
        ie = re.marginx || 0,
        _e = re.marginy || 0
      function ye(be) {
        var M = be.x,
          O = be.y,
          q = be.width,
          I = be.height
        ;((L = Math.min(L, M - q / 2)),
          (k = Math.max(k, M + q / 2)),
          (U = Math.min(U, O - I / 2)),
          (J = Math.max(J, O + I / 2)))
      }
      ;(e.forEach(B.nodes(), function (be) {
        ye(B.node(be))
      }),
        e.forEach(B.edges(), function (be) {
          var M = B.edge(be)
          e.has(M, 'x') && ye(M)
        }),
        (L -= ie),
        (U -= _e),
        e.forEach(B.nodes(), function (be) {
          var M = B.node(be)
          ;((M.x -= L), (M.y -= U))
        }),
        e.forEach(B.edges(), function (be) {
          var M = B.edge(be)
          ;(e.forEach(M.points, function (O) {
            ;((O.x -= L), (O.y -= U))
          }),
            e.has(M, 'x') && (M.x -= L),
            e.has(M, 'y') && (M.y -= U))
        }),
        (re.width = k - L + ie),
        (re.height = J - U + _e))
    }
    function R(B) {
      e.forEach(B.edges(), function (L) {
        var k = B.edge(L),
          U = B.node(L.v),
          J = B.node(L.w),
          re,
          ie
        ;(k.points
          ? ((re = k.points[0]), (ie = k.points[k.points.length - 1]))
          : ((k.points = []), (re = J), (ie = U)),
          k.points.unshift(f.intersectRect(U, re)),
          k.points.push(f.intersectRect(J, ie)))
      })
    }
    function N(B) {
      e.forEach(B.edges(), function (L) {
        var k = B.edge(L)
        if (e.has(k, 'x'))
          switch (
            ((k.labelpos === 'l' || k.labelpos === 'r') && (k.width -= k.labeloffset), k.labelpos)
          ) {
            case 'l':
              k.x -= k.width / 2 + k.labeloffset
              break
            case 'r':
              k.x += k.width / 2 + k.labeloffset
              break
          }
      })
    }
    function j(B) {
      e.forEach(B.edges(), function (L) {
        var k = B.edge(L)
        k.reversed && k.points.reverse()
      })
    }
    function V(B) {
      ;(e.forEach(B.nodes(), function (L) {
        if (B.children(L).length) {
          var k = B.node(L),
            U = B.node(k.borderTop),
            J = B.node(k.borderBottom),
            re = B.node(e.last(k.borderLeft)),
            ie = B.node(e.last(k.borderRight))
          ;((k.width = Math.abs(ie.x - re.x)),
            (k.height = Math.abs(J.y - U.y)),
            (k.x = re.x + k.width / 2),
            (k.y = U.y + k.height / 2))
        }
      }),
        e.forEach(B.nodes(), function (L) {
          B.node(L).dummy === 'border' && B.removeNode(L)
        }))
    }
    function H(B) {
      e.forEach(B.edges(), function (L) {
        if (L.v === L.w) {
          var k = B.node(L.v)
          ;(k.selfEdges || (k.selfEdges = []),
            k.selfEdges.push({ e: L, label: B.edge(L) }),
            B.removeEdge(L))
        }
      })
    }
    function G(B) {
      var L = f.buildLayerMatrix(B)
      e.forEach(L, function (k) {
        var U = 0
        e.forEach(k, function (J, re) {
          var ie = B.node(J)
          ;((ie.order = re + U),
            e.forEach(ie.selfEdges, function (_e) {
              f.addDummyNode(
                B,
                'selfedge',
                {
                  width: _e.label.width,
                  height: _e.label.height,
                  rank: ie.rank,
                  order: re + ++U,
                  e: _e.e,
                  label: _e.label,
                },
                '_se'
              )
            }),
            delete ie.selfEdges)
        })
      })
    }
    function Y(B) {
      e.forEach(B.nodes(), function (L) {
        var k = B.node(L)
        if (k.dummy === 'selfedge') {
          var U = B.node(k.e.v),
            J = U.x + U.width / 2,
            re = U.y,
            ie = k.x - J,
            _e = U.height / 2
          ;(B.setEdge(k.e, k.label),
            B.removeNode(L),
            (k.label.points = [
              { x: J + (2 * ie) / 3, y: re - _e },
              { x: J + (5 * ie) / 6, y: re - _e },
              { x: J + ie, y: re },
              { x: J + (5 * ie) / 6, y: re + _e },
              { x: J + (2 * ie) / 3, y: re + _e },
            ]),
            (k.label.x = k.x),
            (k.label.y = k.y))
        }
      })
    }
    function Z(B, L) {
      return e.mapValues(e.pick(B, L), Number)
    }
    function ne(B) {
      var L = {}
      return (
        e.forEach(B, function (k, U) {
          L[U.toLowerCase()] = k
        }),
        L
      )
    }
    return ud
  }
  var cd, a0
  function sM() {
    if (a0) return cd
    a0 = 1
    var e = Ie(),
      t = Ue(),
      n = ft().Graph
    cd = { debugOrdering: r }
    function r(o) {
      var i = t.buildLayerMatrix(o),
        a = new n({ compound: !0, multigraph: !0 }).setGraph({})
      return (
        e.forEach(o.nodes(), function (s) {
          ;(a.setNode(s, { label: s }), a.setParent(s, 'layer' + o.node(s).rank))
        }),
        e.forEach(o.edges(), function (s) {
          a.setEdge(s.v, s.w, {}, s.name)
        }),
        e.forEach(i, function (s, l) {
          var u = 'layer' + l
          ;(a.setNode(u, { rank: 'same' }),
            e.reduce(s, function (c, d) {
              return (a.setEdge(c, d, { style: 'invis' }), d)
            }))
        }),
        a
      )
    }
    return cd
  }
  var dd, s0
  function lM() {
    return (s0 || ((s0 = 1), (dd = '0.8.5')), dd)
  }
  var fd, l0
  function uM() {
    return (
      l0 ||
        ((l0 = 1),
        (fd = {
          graphlib: ft(),
          layout: aM(),
          debug: sM(),
          util: { time: Ue().time, notime: Ue().notime },
          version: lM(),
        })),
      fd
    )
  }
  var cM = uM()
  const u0 = bx(cM),
    dM = { idle: '未连接', connecting: '连接中', open: '已连接', closed: '已关闭', error: '异常' },
    fM = {
      idle: 'is-idle',
      connecting: 'is-connecting',
      open: 'is-open',
      closed: 'is-closed',
      error: 'is-error',
    },
    c0 = [],
    Gt = {},
    hM = 1e4,
    d0 = 200,
    f0 = 20,
    h0 = 6e4,
    Kf = _x('managerStore', {
      state: () => ({
        status: 'idle',
        connectionError: '',
        sessions: {},
        selectedSessionId: null,
        currentConfig: null,
        currentTime: Date.now(),
        ticker: void 0,
        ws: null,
        sessionFlowData: {},
      }),
      getters: {
        sortedSessions(e) {
          return Object.values(e.sessions).sort((t, n) => {
            const r = e.currentTime - t.lastUpdated <= 6e4,
              o = e.currentTime - n.lastUpdated <= 6e4
            return r !== o ? Number(o) - Number(r) : n.lastUpdated - t.lastUpdated
          })
        },
        activeSession(e) {
          return e.selectedSessionId ? e.sessions[e.selectedSessionId] : this.sortedSessions[0]
        },
        activeMessages() {
          return this.activeSession?.messages || []
        },
        activeChatMessages() {
          return this.activeSession?.chatMessages || []
        },
        activeFlowData(e) {
          const t = this.activeSession?.id
          return !t || !e.sessionFlowData[t]
            ? { handlerNodes: {}, signalEdges: {}, activeStreams: {} }
            : e.sessionFlowData[t]
        },
        flowNodes() {
          return Object.values(this.activeFlowData.handlerNodes)
        },
        flowEdges() {
          return Object.values(this.activeFlowData.signalEdges)
        },
      },
      actions: {
        ensureSessionFlowData(e) {
          return (
            this.sessionFlowData[e] ||
              (this.sessionFlowData = {
                ...this.sessionFlowData,
                [e]: { handlerNodes: {}, signalEdges: {}, activeStreams: {} },
              }),
            this.sessionFlowData[e]
          )
        },
        getSessionFlowData(e) {
          return this.sessionFlowData[e] || { handlerNodes: {}, signalEdges: {}, activeStreams: {} }
        },
        start() {
          ;(this.connectWS(), this.startTicker())
        },
        stop() {
          ;(this.cleanupWS(), this.cleanupMedia(), this.stopTicker())
        },
        startTicker() {
          this.ticker === void 0 &&
            (this.ticker = window.setInterval(() => {
              ;((this.currentTime = Date.now()), this.checkNodeTimeouts())
            }, 1e3))
        },
        checkNodeTimeouts() {
          const e = Date.now()
          Object.keys(this.sessionFlowData).forEach((t) => {
            this.checkSessionNodeTimeouts(t, e)
          })
        },
        checkSessionNodeTimeouts(e, t) {
          const n = this.sessionFlowData[e]
          if (!n) return
          let r = !1
          ;(Object.keys(n.handlerNodes).forEach((o) => {
            const i = n.handlerNodes[o]
            i.data.status === 'active' &&
              i.data.activeStartTime &&
              t - i.data.activeStartTime > hM &&
              ((n.handlerNodes = {
                ...n.handlerNodes,
                [o]: { ...i, data: { ...i.data, status: 'timeout' } },
              }),
              (n.activeStreams = { ...n.activeStreams, [o]: 'timeout' }),
              (r = !0))
          }),
            r &&
              (Object.keys(n.signalEdges).forEach((o) => {
                const i = n.signalEdges[o],
                  a = n.activeStreams[i.source] === 'active',
                  s = n.activeStreams[i.target] === 'active'
                n.signalEdges = { ...n.signalEdges, [o]: { ...i, animated: a && s } }
              }),
              (this.sessionFlowData = { ...this.sessionFlowData, [e]: { ...n } })))
        },
        stopTicker() {
          this.ticker !== void 0 && (window.clearInterval(this.ticker), (this.ticker = void 0))
        },
        layoutNodes(e) {
          const t = this.sessionFlowData[e]
          if (!t) return
          const n = t.handlerNodes,
            r = t.signalEdges
          if (Object.keys(n).length === 0) return
          const o = new u0.graphlib.Graph()
          ;(o.setDefaultEdgeLabel(() => ({})),
            o.setGraph({ rankdir: 'LR', nodesep: 40, ranksep: 30, marginx: 20, marginy: 20 }))
          const i = 120,
            a = 40
          ;(Object.values(n).forEach((l) => {
            o.setNode(l.id, { width: i, height: a })
          }),
            Object.values(r).forEach((l) => {
              o.setEdge(l.source, l.target)
            }),
            u0.layout(o))
          const s = {}
          ;(Object.values(n).forEach((l) => {
            const u = o.node(l.id)
            u ? (s[l.id] = { ...l, position: { x: u.x - i / 2, y: u.y - a / 2 } }) : (s[l.id] = l)
          }),
            (t.handlerNodes = s),
            (this.sessionFlowData = { ...this.sessionFlowData, [e]: { ...t } }))
        },
        selectSession(e) {
          this.selectedSessionId = e
        },
        timestampToMs(e) {
          return e ? (Array.isArray(e) ? e[0] * 1e3 + e[1] / 1e6 : Math.round(e)) : Date.now()
        },
        ensureSession(e, t) {
          const n = this.sessions[e],
            r = n || { id: e, owner: t, messages: [], chatMessages: [], lastUpdated: Date.now() }
          return (
            n
              ? t && !n.owner && (this.sessions = { ...this.sessions, [e]: { ...n, owner: t } })
              : (this.enforceSessionLimit(),
                (this.sessions = { ...this.sessions, [e]: r }),
                (this.selectedSessionId = e)),
            this.sessions[e] || r
          )
        },
        upsertSession(e) {
          this.sessions = { ...this.sessions, [e.id]: e }
        },
        updateSessionLastUpdated(e) {
          const t = this.sessions[e]
          t && (this.sessions = { ...this.sessions, [e]: { ...t, lastUpdated: Date.now() } })
        },
        removeSession(e) {
          if (!this.sessions[e]) return
          const t = { ...this.sessions }
          if ((delete t[e], (this.sessions = t), this.sessionFlowData[e])) {
            const n = { ...this.sessionFlowData }
            ;(delete n[e], (this.sessionFlowData = n))
          }
          if (
            (Object.keys(Gt).forEach((n) => {
              n.startsWith(`${e}:`) && (window.clearTimeout(Gt[n]), delete Gt[n])
            }),
            this.selectedSessionId === e)
          ) {
            const n = this.sortedSessions
            this.selectedSessionId = n.length > 0 ? n[0].id : null
          }
        },
        enforceSessionLimit() {
          const e = Object.keys(this.sessions).length
          if (e < f0) return
          const t = this.currentTime,
            n = Object.values(this.sessions).sort((o, i) => {
              const a = t - o.lastUpdated <= h0,
                s = t - i.lastUpdated <= h0
              return a !== s ? Number(a) - Number(s) : o.lastUpdated - i.lastUpdated
            }),
            r = e - f0 + 1
          for (let o = 0; o < r && o < n.length; o++) this.removeSession(n[o].id)
        },
        formatTs(e) {
          return new Date(e).toLocaleTimeString('zh-CN', {
            hour12: !1,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
          })
        },
        resolveRoleFromDataType(e) {
          return e?.startsWith('human') ? 'human' : 'avatar'
        },
        addChatMessage(e, t) {
          const r = this.ensureSession(e).chatMessages,
            o = t.ref_streams?.[t.ref_streams?.length - 1] || t.stream
          if (o) {
            let i
            for (let a = r.length - 1; a >= 0; a -= 1) {
              const s = r[a]
              if (
                (s.type === 'chat_message' &&
                  s.textStream?.stream_id === o?.stream_id &&
                  s.textStream?.builder_id === o?.builder_id) ||
                (s.audioStream?.stream_id === o?.stream_id &&
                  s.audioStream?.builder_id === o?.builder_id)
              ) {
                i = s
                break
              }
            }
            i
              ? t.dataType === 'avatar_audio' ||
                t.dataType === 'human_audio' ||
                t.dataType === 'human_duplex_audio'
                ? ((i.audioUrl = t.filePath ? vh(t.filePath) : void 0),
                  (i.audioStream = { ...t.stream, stream_meta: t.stream_meta }))
                : (t.dataType === 'avatar_text' ||
                    t.dataType === 'human_text' ||
                    t.dataType === 'human_duplex_text') &&
                  (t.dataType === 'human_text'
                    ? (i.originalText += t.text || '')
                    : ((i.text += t.text || ''),
                      (i.textStream = { ...t.stream, stream_meta: t.stream_meta })))
              : t.dataType === 'avatar_audio' ||
                  t.dataType === 'human_audio' ||
                  t.dataType === 'human_duplex_audio'
                ? r.push({
                    type: 'chat_message',
                    text: '',
                    role: this.resolveRoleFromDataType(t.dataType),
                    textStream: {},
                    audioStream: { ...t.stream, stream_meta: t.stream_meta },
                    audioUrl: t.filePath ? vh(t.filePath) : void 0,
                    timestamp: t.ts,
                  })
                : (t.dataType === 'avatar_text' ||
                    t.dataType === 'human_text' ||
                    t.dataType === 'human_duplex_text') &&
                  r.push({
                    type: 'chat_message',
                    text: t.text || '',
                    role: this.resolveRoleFromDataType(t.dataType),
                    textStream: { ...t.stream, stream_meta: t.stream_meta },
                    audioStream: void 0,
                    audioUrl: void 0,
                    timestamp: t.ts,
                  })
          }
        },
        updateNodeStatus(e, t, n) {
          const r = this.sessionFlowData[e]
          if (!r) return
          const o = r.handlerNodes[t]
          o &&
            ((r.handlerNodes = {
              ...r.handlerNodes,
              [t]: {
                ...o,
                data: {
                  ...o.data,
                  status: n,
                  lastUpdated: Date.now(),
                  activeStartTime: n === 'active' ? Date.now() : o.data.activeStartTime,
                },
              },
            }),
            (r.activeStreams = { ...r.activeStreams, [t]: n }),
            Object.keys(r.signalEdges).forEach((i) => {
              const a = r.signalEdges[i]
              if (a.source === t || a.target === t) {
                const s = r.activeStreams[a.source] === 'active',
                  l = r.activeStreams[a.target] === 'active'
                r.signalEdges = { ...r.signalEdges, [i]: { ...a, animated: s && l } }
              }
            }),
            (this.sessionFlowData = { ...this.sessionFlowData, [e]: { ...r } }))
        },
        addSignalMessage(e, t) {
          const { type: n, source_type: r, source_name: o, stream: i } = t
          if ((n !== 'stream_begin' && n !== 'stream_end') || r !== 'handler' || !o) return
          const a = this.ensureSessionFlowData(e),
            s = n === 'stream_begin',
            l = o,
            u = Date.now(),
            c = `${e}:${l}`
          if ((Gt[c] && (window.clearTimeout(Gt[c]), delete Gt[c]), a.handlerNodes[l]))
            if (s)
              ((a.handlerNodes = {
                ...a.handlerNodes,
                [l]: {
                  ...a.handlerNodes[l],
                  data: {
                    ...a.handlerNodes[l].data,
                    status: 'active',
                    activeStartTime: u,
                    startTime: t.timestamp,
                    endTime: void 0,
                    lastUpdated: u,
                  },
                },
              }),
                (a.activeStreams = { ...a.activeStreams, [o]: 'active' }))
            else {
              const h = a.handlerNodes[l].data.activeStartTime || 0,
                g = u - h
              if (((a.handlerNodes[l].data.endTime = t.timestamp), g < d0)) {
                const m = d0 - g
                Gt[c] = window.setTimeout(() => {
                  ;(this.updateNodeStatus(e, l, 'inactive'), delete Gt[c])
                }, m)
              } else this.updateNodeStatus(e, l, 'inactive')
            }
          else {
            const h = Object.keys(a.handlerNodes).length,
              g = {
                id: l,
                type: 'handler',
                position: { x: 100 + (h % 4) * 200, y: 100 + Math.floor(h / 4) * 120 },
                data: {
                  label: o,
                  sourceType: r,
                  sourceName: o,
                  status: s ? 'active' : 'inactive',
                  startTime: t.timestamp,
                  endTime: void 0,
                  activeStartTime: s ? u : void 0,
                  lastUpdated: u,
                },
              }
            ;((a.handlerNodes = { ...a.handlerNodes, [l]: g }),
              (a.activeStreams = { ...a.activeStreams, [o]: s ? 'active' : 'inactive' }))
          }
          const d = (h, g) => {
            if (!a.handlerNodes[h]) {
              const b = Object.keys(a.handlerNodes).length,
                y = {
                  id: h,
                  type: 'handler',
                  position: { x: 100 + (b % 4) * 200, y: 100 + Math.floor(b / 4) * 120 },
                  data: {
                    label: h,
                    sourceType: 'handler',
                    sourceName: h,
                    status: 'inactive',
                    lastUpdated: Date.now(),
                  },
                }
              a.handlerNodes = { ...a.handlerNodes, [h]: y }
            }
            const m = `${h}->${l}`,
              v = a.activeStreams[h] === 'active'
            a.signalEdges = {
              ...a.signalEdges,
              [m]: {
                id: m,
                source: h,
                target: l,
                animated: v && s,
                data: { refStreamId: g ? `${g.builder_id}-${g.stream_id}` : void 0 },
              },
            }
          }
          i?.producer && i.producer !== t.source_name && d(i.producer || '', i)
          const { ref_streams: f } = t
          ;(i?.producer === t.source_name &&
            f &&
            f.length > 0 &&
            f.forEach((h) => {
              h.producer && d(h.producer || '', h)
            }),
            Object.keys(a.signalEdges).forEach((h) => {
              const g = a.signalEdges[h]
              if (g.source === l || g.target === l) {
                const m = a.activeStreams[g.source] === 'active',
                  v = a.activeStreams[g.target] === 'active'
                a.signalEdges = { ...a.signalEdges, [h]: { ...g, animated: m && v } }
              }
            }),
            (this.sessionFlowData = { ...this.sessionFlowData, [e]: { ...a } }),
            this.layoutNodes(e))
        },
        handleHeartbeat(e) {
          if (!e.session_id) return
          const t = this.sessionFlowData[e.session_id]
          if (!t) return
          const n = Date.now()
          let r = !1
          const o = (i) => {
            const a = t.handlerNodes[i]
            a &&
              ((t.handlerNodes = {
                ...t.handlerNodes,
                [i]: {
                  ...a,
                  data: { ...a.data, activeStartTime: n, status: 'active', lastUpdated: n },
                },
              }),
              (r = !0))
          }
          ;(e.stream?.producer && o(e.stream.producer),
            e.ref_streams &&
              e.ref_streams.length > 0 &&
              e.ref_streams.forEach((i) => {
                i.producer && o(i.producer)
              }),
            r && (this.sessionFlowData = { ...this.sessionFlowData, [e.session_id]: { ...t } }))
        },
        handleChatData(e) {
          if (!e.session_id) return
          const t = this.timestampToMs(e.timestamp),
            n = Sx()
          if ((this.updateSessionLastUpdated(e.session_id), e.data?.kind === 'heartbeat')) {
            this.handleHeartbeat(e)
            return
          }
          const r = {
            id: n,
            kind: 'chat_data',
            ts: t,
            tsDisplay: this.formatTs(t),
            sessionId: e.session_id,
            dataType: e.data_type,
            stream: e.stream,
            ref_streams: e?.ref_streams,
            text: e.data?.text,
            filePath: e.data?.file_path,
            meta: e.meta,
            stream_meta: e.stream_meta,
          }
          this.addChatMessage(e.session_id, r)
        },
        handleSignal(e) {
          e.session_id &&
            (this.updateSessionLastUpdated(e.session_id), this.addSignalMessage(e.session_id, e))
        },
        handleSnapshot(e) {
          Array.isArray(e.items) && e.items.forEach((t) => this.handleIncoming(t))
        },
        handleCurrentConfig(e) {
          this.currentConfig = e.config || null
        },
        handleIncoming(e) {
          if (!(!e || typeof e != 'object'))
            switch (e.event) {
              case 'current_config':
                this.handleCurrentConfig(e)
                break
              case 'snapshot':
                this.handleSnapshot(e)
                break
              case 'chat_data':
                this.handleChatData(e)
                break
              case 'signal':
                this.handleSignal(e)
                break
            }
        },
        cleanupWS() {
          ;(this.ws?.stop(), (this.ws = null))
        },
        cleanupMedia() {
          ;(c0.forEach((e) => URL.revokeObjectURL(e)), (c0.length = 0))
        },
        disconnect() {
          ;(this.cleanupWS(), (this.status = 'closed'))
        },
        sendInterrupt() {
          const e = this.activeSession?.id
          if (!e) {
            console.warn('No active session to interrupt')
            return
          }
          if (!this.ws || this.ws.engine?.readyState !== WebSocket.OPEN) {
            console.warn('WebSocket is not connected')
            return
          }
          const t = { event: 'interrupt', session_id: e, timestamp: Date.now() }
          ;(this.ws.send(JSON.stringify(t)), console.log('Interrupt signal sent:', t))
        },
        reconnect() {
          ;(this.disconnect(), this.connectWS())
        },
        async connectWS() {
          ;((this.status = 'connecting'), (this.connectionError = ''), this.cleanupWS())
          const e = wx()
          ;((this.ws = e),
            e.on(eo.WS_OPEN, () => {
              this.status = 'open'
            }),
            e.on(eo.WS_CLOSE, () => {
              this.status = 'closed'
            }),
            e.on(eo.WS_ERROR, (t) => {
              ;((this.status = 'error'),
                (this.connectionError = typeof t == 'string' ? t : t?.message || '连接异常'),
                this.connectionError && Po.error(this.connectionError))
            }),
            e.on(eo.WS_MESSAGE, (t) => {
              if (typeof t == 'string')
                try {
                  const n = JSON.parse(t)
                  this.handleIncoming(n)
                } catch (n) {
                  console.warn('数据工具消息解析失败', n)
                }
            }))
        },
      },
    }),
    pM = { class: 'manager__header' },
    vM = { class: 'manager__header-actions' },
    gM = { class: 'auth-form' },
    mM = { class: 'auth-form__item' },
    yM = te({
      __name: 'ManagerHeader',
      props: { status: {}, statusTextMap: {}, statusClassMap: {} },
      emits: ['reconnect'],
      setup(e, { emit: t }) {
        const n = e,
          r = t,
          o = () => {
            r('reconnect')
          },
          i = de(!1),
          a = de(''),
          s = () => {
            ;((a.value = localStorage.getItem('auth_openavatarchat') || ''), (i.value = !0))
          },
          l = () => {
            ;(a.value
              ? localStorage.setItem('auth_openavatarchat', a.value)
              : localStorage.removeItem('auth_openavatarchat'),
              localStorage.removeItem('auth_robot'),
              Po.success('认证信息已保存'),
              (i.value = !1))
          },
          u = () => {
            i.value = !1
          }
        return (c, d) => (
          ee(),
          ve('header', pM, [
            d[7] ||
              (d[7] = he(
                'div',
                null,
                [
                  he('div', { class: 'manager__title' }, 'OpenAvatarChat'),
                  he('div', { class: 'manager__subtitle' }, '实时会话列表 + 详情'),
                ],
                -1
              )),
            he('div', vM, [
              F(
                K(_t),
                { size: 'small', type: 'text', onClick: s },
                {
                  icon: Ve(() => [F(K(Af))]),
                  default: Ve(() => [d[2] || (d[2] = Xt(' 认证设置 ', -1))]),
                  _: 1,
                }
              ),
              he(
                'div',
                { class: ct(['manager__status', n.statusClassMap[n.status]]) },
                [
                  d[4] || (d[4] = he('span', { class: 'manager__status-dot' }, null, -1)),
                  he('span', null, ze(n.statusTextMap[n.status]), 1),
                  F(
                    K(_t),
                    { size: 'small', type: 'link', onClick: o },
                    { default: Ve(() => [...(d[3] || (d[3] = [Xt('重新连接', -1)]))]), _: 1 }
                  ),
                ],
                2
              ),
            ]),
            F(
              K(Ze),
              {
                open: i.value,
                'onUpdate:open': d[1] || (d[1] = (f) => (i.value = f)),
                title: '认证设置',
                width: 480,
                onOk: l,
                onCancel: u,
              },
              {
                default: Ve(() => [
                  he('div', gM, [
                    he('div', mM, [
                      d[5] ||
                        (d[5] = he(
                          'label',
                          { class: 'auth-form__label' },
                          'OpenAvatarChat Token',
                          -1
                        )),
                      F(
                        K(Fe).Password,
                        {
                          value: a.value,
                          'onUpdate:value': d[0] || (d[0] = (f) => (a.value = f)),
                          placeholder: '请输入 auth_openavatarchat',
                          'allow-clear': '',
                        },
                        null,
                        8,
                        ['value']
                      ),
                      d[6] ||
                        (d[6] = he(
                          'div',
                          { class: 'auth-form__hint' },
                          '用于连接 OpenAvatarChat 服务的认证令牌',
                          -1
                        )),
                    ]),
                  ]),
                ]),
                _: 1,
              },
              8,
              ['open']
            ),
          ])
        )
      },
    }),
    bM = xn(yM, [['__scopeId', 'data-v-cd143cc8']]),
    _M = ['disabled'],
    wM = { key: 0, class: 'audio-player__loading' },
    SM = { key: 1, class: 'audio-player__icon', viewBox: '0 0 24 24', fill: 'currentColor' },
    xM = { key: 2, class: 'audio-player__icon', viewBox: '0 0 24 24', fill: 'currentColor' },
    CM = { class: 'audio-player__track' },
    EM = { class: 'audio-player__time' },
    $M = te({
      __name: 'InlineAudioPlayer',
      props: { src: {}, dark: { type: Boolean, default: !1 } },
      emits: ['download'],
      setup(e, { emit: t }) {
        const n = e,
          r = t,
          o = () => {
            r('download')
          },
          i = de(null),
          a = de(!1),
          s = de(!1),
          l = de(0),
          u = de(0),
          c = de(null),
          d = (S) =>
            !S || S.startsWith('http://') || S.startsWith('https://')
              ? S
              : S.startsWith('/')
                ? `${xx}${S}`
                : `${Cx ? 'https://' : 'http://'}${S}`,
          f = async () => {
            const S = d(n.src)
            try {
              const w = localStorage.getItem('auth_openavatarchat'),
                T = {}
              w && (T.Authorization = `Bearer ${w}`)
              const A = await window.fetch(S, { headers: T })
              if (!A.ok) throw new Error(`Failed to load audio: ${A.status}`)
              const $ = await A.blob()
              ;(c.value && URL.revokeObjectURL(c.value),
                (c.value = URL.createObjectURL($)),
                i.value && ((i.value.src = c.value), i.value.load()))
            } catch (w) {
              ;(console.error('加载音频失败，回落到原始URL:', w),
                i.value && ((i.value.src = S), i.value.load()))
            }
          }
        Jo(() => {
          c.value && URL.revokeObjectURL(c.value)
        })
        const h = (S) => {
            if (!isFinite(S) || isNaN(S)) return '0:00'
            const w = Math.floor(S / 60),
              T = Math.floor(S % 60)
            return `${w}:${T.toString().padStart(2, '0')}`
          },
          g = X(() => (u.value === 0 ? 0 : (l.value / u.value) * 100)),
          m = X(() => `${h(l.value)} / ${h(u.value)}`),
          v = () => {
            i.value && ((u.value = i.value.duration), (s.value = !0))
          },
          b = () => {
            i.value && (l.value = i.value.currentTime)
          },
          y = () => {
            ;((a.value = !1), (l.value = 0), i.value && (i.value.currentTime = 0))
          },
          p = de(!1),
          _ = async () => {
            if (!(!i.value || p.value))
              if ((!s.value && !c.value && ((p.value = !0), await f(), (p.value = !1)), a.value))
                (i.value.pause(), (a.value = !1))
              else
                try {
                  ;(await i.value.play(), (a.value = !0))
                } catch (S) {
                  console.error('播放失败:', S)
                }
          },
          x = (S) => {
            if (!i.value || u.value === 0) return
            const T = S.currentTarget.getBoundingClientRect(),
              A = S.clientX - T.left,
              P = Math.max(0, Math.min(A / T.width, 1)) * u.value
            ;((i.value.currentTime = P), (l.value = P))
          }
        return (S, w) => (
          ee(),
          ve(
            'span',
            { class: ct(['audio-player', { 'is-dark': n.dark }]) },
            [
              he(
                'audio',
                {
                  ref_key: 'audioEl',
                  ref: i,
                  preload: 'none',
                  onLoadedmetadata: v,
                  onTimeupdate: b,
                  onEnded: y,
                },
                null,
                544
              ),
              he(
                'button',
                { class: 'audio-player__btn', type: 'button', disabled: p.value, onClick: _ },
                [
                  p.value
                    ? (ee(), ve('span', wM, '⏳'))
                    : a.value
                      ? (ee(),
                        ve('svg', xM, [
                          ...(w[1] ||
                            (w[1] = [
                              he('path', { d: 'M6 4h4v16H6V4zm8 0h4v16h-4V4z' }, null, -1),
                            ])),
                        ]))
                      : (ee(),
                        ve('svg', SM, [
                          ...(w[0] || (w[0] = [he('path', { d: 'M8 5v14l11-7z' }, null, -1)])),
                        ])),
                ],
                8,
                _M
              ),
              he('div', { class: 'audio-player__progress', onClick: x }, [
                he('div', CM, [
                  he(
                    'div',
                    { class: 'audio-player__fill', style: Ct({ width: `${g.value}%` }) },
                    null,
                    4
                  ),
                ]),
              ]),
              he('span', EM, ze(m.value), 1),
              he('span', { class: 'audio-player__download', onClick: o }, '📥'),
            ],
            2
          )
        )
      },
    }),
    TM = xn($M, [['__scopeId', 'data-v-da15cadd']])
  function R1(e) {
    return lf() ? (gr(e), !0) : !1
  }
  function Ci(e) {
    return typeof e == 'function' ? e() : K(e)
  }
  const Zf = typeof window < 'u' && typeof document < 'u'
  typeof WorkerGlobalScope < 'u' && globalThis instanceof WorkerGlobalScope
  const OM = Object.prototype.toString,
    PM = (e) => OM.call(e) === '[object Object]',
    IM = () => {}
  function AM(e) {
    let t
    function n() {
      return (t || (t = e()), t)
    }
    return (
      (n.reset = async () => {
        const r = t
        ;((t = void 0), r && (await r))
      }),
      n
    )
  }
  function NM(e, t, n = {}) {
    const { immediate: r = !0 } = n,
      o = de(!1)
    let i = null
    function a() {
      i && (clearTimeout(i), (i = null))
    }
    function s() {
      ;((o.value = !1), a())
    }
    function l(...u) {
      ;(a(),
        (o.value = !0),
        (i = setTimeout(() => {
          ;((o.value = !1), (i = null), e(...u))
        }, Ci(t))))
    }
    return (r && ((o.value = !0), Zf && l()), R1(s), { isPending: c_(o), start: l, stop: s })
  }
  function RM(e) {
    var t
    const n = Ci(e)
    return (t = n?.$el) != null ? t : n
  }
  const MM = Zf ? window : void 0,
    M1 = Zf ? window.navigator : void 0
  function D1(...e) {
    let t, n, r, o
    if (
      (typeof e[0] == 'string' || Array.isArray(e[0])
        ? (([n, r, o] = e), (t = MM))
        : ([t, n, r, o] = e),
      !t)
    )
      return IM
    ;(Array.isArray(n) || (n = [n]), Array.isArray(r) || (r = [r]))
    const i = [],
      a = () => {
        ;(i.forEach((c) => c()), (i.length = 0))
      },
      s = (c, d, f, h) => (c.addEventListener(d, f, h), () => c.removeEventListener(d, f, h)),
      l = me(
        () => [RM(t), Ci(o)],
        ([c, d]) => {
          if ((a(), !c)) return
          const f = PM(d) ? { ...d } : d
          i.push(...n.flatMap((h) => r.map((g) => s(c, h, g, f))))
        },
        { immediate: !0, flush: 'post' }
      ),
      u = () => {
        ;(l(), a())
      }
    return (R1(u), u)
  }
  function DM() {
    const e = de(!1),
      t = Qe()
    return (
      t &&
        Me(() => {
          e.value = !0
        }, t),
      e
    )
  }
  function B1(e) {
    const t = DM()
    return X(() => (t.value, !!e()))
  }
  function p0(e, t = {}) {
    const { controls: n = !1, navigator: r = M1 } = t,
      o = B1(() => r && 'permissions' in r)
    let i
    const a = typeof e == 'string' ? { name: e } : e,
      s = de(),
      l = () => {
        i && (s.value = i.state)
      },
      u = AM(async () => {
        if (o.value) {
          if (!i)
            try {
              ;((i = await r.permissions.query(a)), D1(i, 'change', l), l())
            } catch {
              s.value = 'prompt'
            }
          return i
        }
      })
    return (u(), n ? { state: s, isSupported: o, query: u } : s)
  }
  function BM(e = {}) {
    const {
        navigator: t = M1,
        read: n = !1,
        source: r,
        copiedDuring: o = 1500,
        legacy: i = !1,
      } = e,
      a = B1(() => t && 'clipboard' in t),
      s = p0('clipboard-read'),
      l = p0('clipboard-write'),
      u = X(() => a.value || i),
      c = de(''),
      d = de(!1),
      f = NM(() => (d.value = !1), o)
    function h() {
      a.value && b(s.value)
        ? t.clipboard.readText().then((y) => {
            c.value = y
          })
        : (c.value = v())
    }
    u.value && n && D1(['copy', 'cut'], h)
    async function g(y = Ci(r)) {
      u.value &&
        y != null &&
        (a.value && b(l.value) ? await t.clipboard.writeText(y) : m(y),
        (c.value = y),
        (d.value = !0),
        f.start())
    }
    function m(y) {
      const p = document.createElement('textarea')
      ;((p.value = y ?? ''),
        (p.style.position = 'absolute'),
        (p.style.opacity = '0'),
        document.body.appendChild(p),
        p.select(),
        document.execCommand('copy'),
        p.remove())
    }
    function v() {
      var y, p, _
      return (_ =
        (p = (y = document?.getSelection) == null ? void 0 : y.call(document)) == null
          ? void 0
          : p.toString()) != null
        ? _
        : ''
    }
    function b(y) {
      return y === 'granted' || y === 'prompt'
    }
    return { isSupported: u, text: c, copied: d, copy: g }
  }
  const qM = ['data-kind'],
    zM = { class: 'manager__message-body' },
    LM = { key: 0, class: 'manager__text' },
    FM = { style: { verticalAlign: 'middle' } },
    kM = { key: 1, class: 'manager__text is-muted' },
    HM = { key: 2, class: 'manager__media' },
    jM = ['src'],
    VM = { key: 0, class: 'manager__message-time' },
    GM = { key: 0 },
    WM = { style: { userSelect: 'text' } },
    UM = { key: 1 },
    YM = { style: { userSelect: 'text' } },
    XM = ['onClick'],
    KM = te({
      __name: 'MessageList',
      props: { messages: {} },
      setup(e) {
        const t = e,
          n = de(null),
          r = de(!1),
          o = X(() =>
            t.messages
              .filter((d) => d.type === 'chat_message')
              .map((d, f) => {
                const h = d.textStream?.builder_id,
                  g = d.textStream?.stream_id,
                  m = h !== void 0 || g !== void 0 ? `${h ?? 'nb'}-${g ?? 'ns'}` : `msg-${f}`
                return { ...d, builderId: h, streamId: g, key: m }
              })
          ),
          i = (d) => {
            if (!d) return ''
            const f = new Date(d * 1e3),
              h = f.getHours().toString().padStart(2, '0'),
              g = f.getMinutes().toString().padStart(2, '0'),
              m = f.getSeconds().toString().padStart(2, '0')
            return `${h}:${g}:${m}`
          },
          a = () => {
            n.value && ((n.value.scrollTop = n.value.scrollHeight), (r.value = !1))
          },
          s = () => {
            if (!n.value) return
            const { scrollTop: d, clientHeight: f, scrollHeight: h } = n.value
            r.value = d + f < h - 40
          }
        ;(Me(() => {
          ;(a(), n.value?.addEventListener('scroll', s), s())
        }),
          je(() => {
            n.value?.removeEventListener('scroll', s)
          }),
          me(
            () => o.value.length,
            async () => {
              ;(await Ne(), a())
            }
          ),
          me(
            () => o.value.map((d) => `${d.key}:${d.text ?? ''}`).join('||'),
            async () => {
              ;(await Ne(), a())
            }
          ))
        const { copy: l } = BM(),
          u = (d) => {
            l(
              JSON.stringify({
                timestamp: d.timestamp,
                audioStreamMeta: d.audioStream?.stream_meta,
                textStreamMeta: d.textStream?.stream_meta,
              })
            )
          },
          c = async (d) => {
            if (!d.audioUrl) return
            const f = d.audioUrl
            let h = 'audio'
            d.audioStream?.stream_meta?.task_id
              ? (h = 'tts_' + d.audioStream?.stream_meta?.task_id)
              : d.textStream?.stream_meta?.task_id &&
                (h = 'asr_' + d.textStream?.stream_meta?.task_id)
            try {
              const g = localStorage.getItem('auth_openavatarchat'),
                m = {}
              g && (m.Authorization = `Bearer ${g}`)
              const v = await window.fetch(f, { headers: m })
              if (!v.ok) throw new Error(`Failed to download audio: ${v.status}`)
              const b = await v.blob(),
                y = URL.createObjectURL(b),
                p = document.createElement('a')
              ;((p.href = y),
                (p.download = `${h}.wav`),
                p.click(),
                p.remove(),
                URL.revokeObjectURL(y))
            } catch (g) {
              console.error('下载音频失败，回落到原始URL:', g)
              const m = document.createElement('a')
              ;((m.href = f), (m.download = `${h}.wav`), m.click(), m.remove())
            }
          }
        return (d, f) => (
          ee(),
          ve(
            'div',
            { ref_key: 'scrollEl', ref: n, class: 'manager__messages' },
            [
              (ee(!0),
              ve(
                Re,
                null,
                yn(
                  o.value,
                  (h) => (
                    ee(),
                    ve(
                      'div',
                      {
                        key: h.key,
                        class: ct([
                          'manager__message-wrapper',
                          h.role === 'avatar' ? 'is-avatar' : 'is-human',
                        ]),
                      },
                      [
                        he(
                          'div',
                          {
                            class: ct([
                              'manager__message-card',
                              h.role === 'avatar' ? 'is-avatar' : 'is-human',
                            ]),
                            'data-kind': h.type,
                          },
                          [
                            he('div', zM, [
                              h.type === 'chat_message'
                                ? (ee(),
                                  ve(
                                    Re,
                                    { key: 0 },
                                    [
                                      h.text
                                        ? (ee(),
                                          ve('p', LM, [
                                            he('span', FM, ze(h.text), 1),
                                            h.audioUrl
                                              ? (ee(),
                                                ke(
                                                  TM,
                                                  {
                                                    key: 0,
                                                    src: h.audioUrl,
                                                    dark: h.role === 'avatar',
                                                    onDownload: (g) => c(h),
                                                  },
                                                  null,
                                                  8,
                                                  ['src', 'dark', 'onDownload']
                                                ))
                                              : Pe('', !0),
                                          ]))
                                        : (ee(), ve('p', kM, '无文本内容')),
                                      h.imageUrl
                                        ? (ee(),
                                          ve('div', HM, [
                                            he(
                                              'img',
                                              {
                                                class: 'manager__image',
                                                src: h.imageUrl,
                                                alt: 'image',
                                              },
                                              null,
                                              8,
                                              jM
                                            ),
                                          ]))
                                        : Pe('', !0),
                                    ],
                                    64
                                  ))
                                : Pe('', !0),
                            ]),
                          ],
                          10,
                          qM
                        ),
                        h.timestamp
                          ? (ee(),
                            ve('div', VM, [
                              Xt(ze(i(h.timestamp)) + ' ', 1),
                              F(
                                K(QO),
                                { trigger: 'click', 'auto-adjust-overflow': !0 },
                                {
                                  title: Ve(() => [
                                    h.audioStream?.stream_meta
                                      ? (ee(),
                                        ve('div', GM, [
                                          f[0] || (f[0] = he('span', null, 'audio:', -1)),
                                          he('span', WM, ze(h.audioStream?.stream_meta.task_id), 1),
                                        ]))
                                      : Pe('', !0),
                                    h.textStream?.stream_meta
                                      ? (ee(),
                                        ve('div', UM, [
                                          f[1] || (f[1] = he('span', null, 'text:', -1)),
                                          he('span', YM, ze(h.textStream?.stream_meta.task_id), 1),
                                        ]))
                                      : Pe('', !0),
                                  ]),
                                  default: Ve(() => [
                                    he(
                                      'span',
                                      { class: 'manager__copy-icon', onClick: (g) => u(h) },
                                      '📋',
                                      8,
                                      XM
                                    ),
                                  ]),
                                  _: 2,
                                },
                                1024
                              ),
                            ]))
                          : Pe('', !0),
                      ],
                      2
                    )
                  )
                ),
                128
              )),
              r.value
                ? (ee(),
                  ve(
                    'button',
                    { key: 0, class: 'manager__scroll-bottom', type: 'button', onClick: a },
                    ' ↓ 滚动到底部 '
                  ))
                : Pe('', !0),
            ],
            512
          )
        )
      },
    }),
    ZM = xn(KM, [['__scopeId', 'data-v-b656e935']]),
    JM = te({
      name: 'SessionList',
      props: {
        sessions: { type: Array, required: !0 },
        now: { type: Number, required: !0 },
        activeSessionId: { type: String, default: null },
      },
      emits: ['select', 'close'],
      setup(e, { emit: t }) {
        function n(i) {
          t('select', i)
        }
        function r(i, a) {
          ;(a.stopPropagation(), t('close', i))
        }
        const o = X(() => {
          const i = {}
          for (const a of e.sessions) i[a.id] = e.now - a.lastUpdated <= 6e4
          return i
        })
        return { props: e, handleSelect: n, handleClose: r, liveStatusMap: o }
      },
    }),
    QM = { class: 'manager__sessions' },
    eD = { class: 'manager__tabs-header' },
    tD = { class: 'manager__session-count' },
    nD = { key: 0, class: 'manager__empty' },
    rD = { key: 1, class: 'manager__tab-strip', role: 'tablist' },
    oD = ['onClick'],
    iD = { class: 'manager__tab-text' },
    aD = ['onClick']
  function sD(e, t, n, r, o, i) {
    return (
      ee(),
      ve('header', QM, [
        he('div', eD, [
          t[0] || (t[0] = he('div', { class: 'manager__section-title' }, '会话', -1)),
          he('div', tD, ze(e.props.sessions.length) + ' 个', 1),
        ]),
        e.props.sessions.length === 0
          ? (ee(), ve('div', nD, '暂无会话'))
          : (ee(),
            ve('div', rD, [
              (ee(!0),
              ve(
                Re,
                null,
                yn(
                  e.props.sessions,
                  (a) => (
                    ee(),
                    ve(
                      'button',
                      {
                        key: a.id,
                        type: 'button',
                        role: 'tab',
                        class: ct([
                          'manager__tab',
                          a.id === e.props.activeSessionId ? 'is-active' : '',
                        ]),
                        onClick: (s) => e.handleSelect(a.id),
                      },
                      [
                        he(
                          'span',
                          {
                            class: ct([
                              'manager__status-dot',
                              e.liveStatusMap[a.id] ? 'is-live' : 'is-idle',
                            ]),
                          },
                          null,
                          2
                        ),
                        he('span', iD, ze(a.id), 1),
                        he(
                          'span',
                          {
                            class: 'manager__tab-close',
                            title: '关闭会话',
                            onClick: (s) => e.handleClose(a.id, s),
                          },
                          ' × ',
                          8,
                          aD
                        ),
                      ],
                      10,
                      oD
                    )
                  )
                ),
                128
              )),
            ])),
      ])
    )
  }
  const lD = xn(JM, [
    ['render', sD],
    ['__scopeId', 'data-v-4ddeaf49'],
  ])
  function Ar(e) {
    return lf() ? (gr(e), !0) : !1
  }
  function It(e) {
    return typeof e == 'function' ? e() : K(e)
  }
  const uD = typeof window < 'u' && typeof document < 'u',
    cD = (e) => typeof e < 'u',
    dD = Object.prototype.toString,
    fD = (e) => dD.call(e) === '[object Object]',
    hD = () => {}
  function pD(e, t) {
    function n(...r) {
      return new Promise((o, i) => {
        Promise.resolve(e(() => t.apply(this, r), { fn: t, thisArg: this, args: r }))
          .then(o)
          .catch(i)
      })
    }
    return n
  }
  const q1 = (e) => e()
  function vD(e = q1) {
    const t = de(!0)
    function n() {
      t.value = !1
    }
    function r() {
      t.value = !0
    }
    const o = (...i) => {
      t.value && e(...i)
    }
    return { isActive: c_(t), pause: n, resume: r, eventFilter: o }
  }
  function v0(e, t = !1, n = 'Timeout') {
    return new Promise((r, o) => {
      setTimeout(t ? () => o(n) : r, e)
    })
  }
  function gD(e, t, n = {}) {
    const { eventFilter: r = q1, ...o } = n
    return me(e, pD(r, t), o)
  }
  function An(e, t, n = {}) {
    const { eventFilter: r, ...o } = n,
      { eventFilter: i, pause: a, resume: s, isActive: l } = vD(r)
    return { stop: gD(e, t, { ...o, eventFilter: i }), pause: a, resume: s, isActive: l }
  }
  function mD(e, t = {}) {
    if (!ei(e)) return Px(e)
    const n = Array.isArray(e.value) ? Array.from({ length: e.value.length }) : {}
    for (const r in e.value)
      n[r] = Ix(() => ({
        get() {
          return e.value[r]
        },
        set(o) {
          var i
          if ((i = It(t.replaceRef)) != null ? i : !0)
            if (Array.isArray(e.value)) {
              const s = [...e.value]
              ;((s[r] = o), (e.value = s))
            } else {
              const s = { ...e.value, [r]: o }
              ;(Object.setPrototypeOf(s, Object.getPrototypeOf(e.value)), (e.value = s))
            }
          else e.value[r] = o
        },
      }))
    return n
  }
  function kd(e, t = !1) {
    function n(d, { flush: f = 'sync', deep: h = !1, timeout: g, throwOnTimeout: m } = {}) {
      let v = null
      const y = [
        new Promise((p) => {
          v = me(
            e,
            (_) => {
              d(_) !== t && (v?.(), p(_))
            },
            { flush: f, deep: h, immediate: !0 }
          )
        }),
      ]
      return (
        g != null &&
          y.push(
            v0(g, m)
              .then(() => It(e))
              .finally(() => v?.())
          ),
        Promise.race(y)
      )
    }
    function r(d, f) {
      if (!ei(d)) return n((_) => _ === d, f)
      const { flush: h = 'sync', deep: g = !1, timeout: m, throwOnTimeout: v } = f ?? {}
      let b = null
      const p = [
        new Promise((_) => {
          b = me(
            [e, d],
            ([x, S]) => {
              t !== (x === S) && (b?.(), _(x))
            },
            { flush: h, deep: g, immediate: !0 }
          )
        }),
      ]
      return (
        m != null &&
          p.push(
            v0(m, v)
              .then(() => It(e))
              .finally(() => (b?.(), It(e)))
          ),
        Promise.race(p)
      )
    }
    function o(d) {
      return n((f) => !!f, d)
    }
    function i(d) {
      return r(null, d)
    }
    function a(d) {
      return r(void 0, d)
    }
    function s(d) {
      return n(Number.isNaN, d)
    }
    function l(d, f) {
      return n((h) => {
        const g = Array.from(h)
        return g.includes(d) || g.includes(It(d))
      }, f)
    }
    function u(d) {
      return c(1, d)
    }
    function c(d = 1, f) {
      let h = -1
      return n(() => ((h += 1), h >= d), f)
    }
    return Array.isArray(It(e))
      ? {
          toMatch: n,
          toContains: l,
          changed: u,
          changedTimes: c,
          get not() {
            return kd(e, !t)
          },
        }
      : {
          toMatch: n,
          toBe: r,
          toBeTruthy: o,
          toBeNull: i,
          toBeNaN: s,
          toBeUndefined: a,
          changed: u,
          changedTimes: c,
          get not() {
            return kd(e, !t)
          },
        }
  }
  function Hd(e) {
    return kd(e)
  }
  function yD(e) {
    var t
    const n = It(e)
    return (t = n?.$el) != null ? t : n
  }
  const z1 = uD ? window : void 0
  function L1(...e) {
    let t, n, r, o
    if (
      (typeof e[0] == 'string' || Array.isArray(e[0])
        ? (([n, r, o] = e), (t = z1))
        : ([t, n, r, o] = e),
      !t)
    )
      return hD
    ;(Array.isArray(n) || (n = [n]), Array.isArray(r) || (r = [r]))
    const i = [],
      a = () => {
        ;(i.forEach((c) => c()), (i.length = 0))
      },
      s = (c, d, f, h) => (c.addEventListener(d, f, h), () => c.removeEventListener(d, f, h)),
      l = me(
        () => [yD(t), It(o)],
        ([c, d]) => {
          if ((a(), !c)) return
          const f = fD(d) ? { ...d } : d
          i.push(...n.flatMap((h) => r.map((g) => s(c, h, g, f))))
        },
        { immediate: !0, flush: 'post' }
      ),
      u = () => {
        ;(l(), a())
      }
    return (Ar(u), u)
  }
  function bD(e) {
    return typeof e == 'function'
      ? e
      : typeof e == 'string'
        ? (t) => t.key === e
        : Array.isArray(e)
          ? (t) => e.includes(t.key)
          : () => !0
  }
  function g0(...e) {
    let t,
      n,
      r = {}
    e.length === 3
      ? ((t = e[0]), (n = e[1]), (r = e[2]))
      : e.length === 2
        ? typeof e[1] == 'object'
          ? ((t = !0), (n = e[0]), (r = e[1]))
          : ((t = e[0]), (n = e[1]))
        : ((t = !0), (n = e[0]))
    const { target: o = z1, eventName: i = 'keydown', passive: a = !1, dedupe: s = !1 } = r,
      l = bD(t)
    return L1(
      o,
      i,
      (c) => {
        ;(c.repeat && It(s)) || (l(c) && n(c))
      },
      a
    )
  }
  function _D(e) {
    return JSON.parse(JSON.stringify(e))
  }
  function hd(e, t, n, r = {}) {
    var o, i, a
    const {
        clone: s = !1,
        passive: l = !1,
        eventName: u,
        deep: c = !1,
        defaultValue: d,
        shouldEmit: f,
      } = r,
      h = Qe(),
      g =
        n ||
        h?.emit ||
        ((o = h?.$emit) == null ? void 0 : o.bind(h)) ||
        ((a = (i = h?.proxy) == null ? void 0 : i.$emit) == null ? void 0 : a.bind(h?.proxy))
    let m = u
    ;(t || (t = 'modelValue'), (m = m || `update:${t.toString()}`))
    const v = (p) => (s ? (typeof s == 'function' ? s(p) : _D(p)) : p),
      b = () => (cD(e[t]) ? v(e[t]) : d),
      y = (p) => {
        f ? f(p) && g(m, p) : g(m, p)
      }
    if (l) {
      const p = b(),
        _ = de(p)
      let x = !1
      return (
        me(
          () => e[t],
          (S) => {
            x || ((x = !0), (_.value = v(S)), Ne(() => (x = !1)))
          }
        ),
        me(
          _,
          (S) => {
            !x && (S !== e[t] || c) && y(S)
          },
          { deep: c }
        ),
        _
      )
    } else
      return X({
        get() {
          return b()
        },
        set(p) {
          y(p)
        },
      })
  }
  var wD = { value: () => {} }
  function Ei() {
    for (var e = 0, t = arguments.length, n = {}, r; e < t; ++e) {
      if (!(r = arguments[e] + '') || r in n || /[\s.]/.test(r))
        throw new Error('illegal type: ' + r)
      n[r] = []
    }
    return new So(n)
  }
  function So(e) {
    this._ = e
  }
  function SD(e, t) {
    return e
      .trim()
      .split(/^|\s+/)
      .map(function (n) {
        var r = '',
          o = n.indexOf('.')
        if ((o >= 0 && ((r = n.slice(o + 1)), (n = n.slice(0, o))), n && !t.hasOwnProperty(n)))
          throw new Error('unknown type: ' + n)
        return { type: n, name: r }
      })
  }
  So.prototype = Ei.prototype = {
    constructor: So,
    on: function (e, t) {
      var n = this._,
        r = SD(e + '', n),
        o,
        i = -1,
        a = r.length
      if (arguments.length < 2) {
        for (; ++i < a; ) if ((o = (e = r[i]).type) && (o = xD(n[o], e.name))) return o
        return
      }
      if (t != null && typeof t != 'function') throw new Error('invalid callback: ' + t)
      for (; ++i < a; )
        if ((o = (e = r[i]).type)) n[o] = m0(n[o], e.name, t)
        else if (t == null) for (o in n) n[o] = m0(n[o], e.name, null)
      return this
    },
    copy: function () {
      var e = {},
        t = this._
      for (var n in t) e[n] = t[n].slice()
      return new So(e)
    },
    call: function (e, t) {
      if ((o = arguments.length - 2) > 0)
        for (var n = new Array(o), r = 0, o, i; r < o; ++r) n[r] = arguments[r + 2]
      if (!this._.hasOwnProperty(e)) throw new Error('unknown type: ' + e)
      for (i = this._[e], r = 0, o = i.length; r < o; ++r) i[r].value.apply(t, n)
    },
    apply: function (e, t, n) {
      if (!this._.hasOwnProperty(e)) throw new Error('unknown type: ' + e)
      for (var r = this._[e], o = 0, i = r.length; o < i; ++o) r[o].value.apply(t, n)
    },
  }
  function xD(e, t) {
    for (var n = 0, r = e.length, o; n < r; ++n) if ((o = e[n]).name === t) return o.value
  }
  function m0(e, t, n) {
    for (var r = 0, o = e.length; r < o; ++r)
      if (e[r].name === t) {
        ;((e[r] = wD), (e = e.slice(0, r).concat(e.slice(r + 1))))
        break
      }
    return (n != null && e.push({ name: t, value: n }), e)
  }
  var jd = 'http://www.w3.org/1999/xhtml'
  const y0 = {
    svg: 'http://www.w3.org/2000/svg',
    xhtml: jd,
    xlink: 'http://www.w3.org/1999/xlink',
    xml: 'http://www.w3.org/XML/1998/namespace',
    xmlns: 'http://www.w3.org/2000/xmlns/',
  }
  function $i(e) {
    var t = (e += ''),
      n = t.indexOf(':')
    return (
      n >= 0 && (t = e.slice(0, n)) !== 'xmlns' && (e = e.slice(n + 1)),
      y0.hasOwnProperty(t) ? { space: y0[t], local: e } : e
    )
  }
  function CD(e) {
    return function () {
      var t = this.ownerDocument,
        n = this.namespaceURI
      return n === jd && t.documentElement.namespaceURI === jd
        ? t.createElement(e)
        : t.createElementNS(n, e)
    }
  }
  function ED(e) {
    return function () {
      return this.ownerDocument.createElementNS(e.space, e.local)
    }
  }
  function F1(e) {
    var t = $i(e)
    return (t.local ? ED : CD)(t)
  }
  function $D() {}
  function Jf(e) {
    return e == null
      ? $D
      : function () {
          return this.querySelector(e)
        }
  }
  function TD(e) {
    typeof e != 'function' && (e = Jf(e))
    for (var t = this._groups, n = t.length, r = new Array(n), o = 0; o < n; ++o)
      for (var i = t[o], a = i.length, s = (r[o] = new Array(a)), l, u, c = 0; c < a; ++c)
        (l = i[c]) &&
          (u = e.call(l, l.__data__, c, i)) &&
          ('__data__' in l && (u.__data__ = l.__data__), (s[c] = u))
    return new Je(r, this._parents)
  }
  function OD(e) {
    return e == null ? [] : Array.isArray(e) ? e : Array.from(e)
  }
  function PD() {
    return []
  }
  function k1(e) {
    return e == null
      ? PD
      : function () {
          return this.querySelectorAll(e)
        }
  }
  function ID(e) {
    return function () {
      return OD(e.apply(this, arguments))
    }
  }
  function AD(e) {
    typeof e == 'function' ? (e = ID(e)) : (e = k1(e))
    for (var t = this._groups, n = t.length, r = [], o = [], i = 0; i < n; ++i)
      for (var a = t[i], s = a.length, l, u = 0; u < s; ++u)
        (l = a[u]) && (r.push(e.call(l, l.__data__, u, a)), o.push(l))
    return new Je(r, o)
  }
  function H1(e) {
    return function () {
      return this.matches(e)
    }
  }
  function j1(e) {
    return function (t) {
      return t.matches(e)
    }
  }
  var ND = Array.prototype.find
  function RD(e) {
    return function () {
      return ND.call(this.children, e)
    }
  }
  function MD() {
    return this.firstElementChild
  }
  function DD(e) {
    return this.select(e == null ? MD : RD(typeof e == 'function' ? e : j1(e)))
  }
  var BD = Array.prototype.filter
  function qD() {
    return Array.from(this.children)
  }
  function zD(e) {
    return function () {
      return BD.call(this.children, e)
    }
  }
  function LD(e) {
    return this.selectAll(e == null ? qD : zD(typeof e == 'function' ? e : j1(e)))
  }
  function FD(e) {
    typeof e != 'function' && (e = H1(e))
    for (var t = this._groups, n = t.length, r = new Array(n), o = 0; o < n; ++o)
      for (var i = t[o], a = i.length, s = (r[o] = []), l, u = 0; u < a; ++u)
        (l = i[u]) && e.call(l, l.__data__, u, i) && s.push(l)
    return new Je(r, this._parents)
  }
  function V1(e) {
    return new Array(e.length)
  }
  function kD() {
    return new Je(this._enter || this._groups.map(V1), this._parents)
  }
  function Lo(e, t) {
    ;((this.ownerDocument = e.ownerDocument),
      (this.namespaceURI = e.namespaceURI),
      (this._next = null),
      (this._parent = e),
      (this.__data__ = t))
  }
  Lo.prototype = {
    constructor: Lo,
    appendChild: function (e) {
      return this._parent.insertBefore(e, this._next)
    },
    insertBefore: function (e, t) {
      return this._parent.insertBefore(e, t)
    },
    querySelector: function (e) {
      return this._parent.querySelector(e)
    },
    querySelectorAll: function (e) {
      return this._parent.querySelectorAll(e)
    },
  }
  function HD(e) {
    return function () {
      return e
    }
  }
  function jD(e, t, n, r, o, i) {
    for (var a = 0, s, l = t.length, u = i.length; a < u; ++a)
      (s = t[a]) ? ((s.__data__ = i[a]), (r[a] = s)) : (n[a] = new Lo(e, i[a]))
    for (; a < l; ++a) (s = t[a]) && (o[a] = s)
  }
  function VD(e, t, n, r, o, i, a) {
    var s,
      l,
      u = new Map(),
      c = t.length,
      d = i.length,
      f = new Array(c),
      h
    for (s = 0; s < c; ++s)
      (l = t[s]) &&
        ((f[s] = h = a.call(l, l.__data__, s, t) + ''), u.has(h) ? (o[s] = l) : u.set(h, l))
    for (s = 0; s < d; ++s)
      ((h = a.call(e, i[s], s, i) + ''),
        (l = u.get(h)) ? ((r[s] = l), (l.__data__ = i[s]), u.delete(h)) : (n[s] = new Lo(e, i[s])))
    for (s = 0; s < c; ++s) (l = t[s]) && u.get(f[s]) === l && (o[s] = l)
  }
  function GD(e) {
    return e.__data__
  }
  function WD(e, t) {
    if (!arguments.length) return Array.from(this, GD)
    var n = t ? VD : jD,
      r = this._parents,
      o = this._groups
    typeof e != 'function' && (e = HD(e))
    for (
      var i = o.length, a = new Array(i), s = new Array(i), l = new Array(i), u = 0;
      u < i;
      ++u
    ) {
      var c = r[u],
        d = o[u],
        f = d.length,
        h = UD(e.call(c, c && c.__data__, u, r)),
        g = h.length,
        m = (s[u] = new Array(g)),
        v = (a[u] = new Array(g)),
        b = (l[u] = new Array(f))
      n(c, d, m, v, b, h, t)
      for (var y = 0, p = 0, _, x; y < g; ++y)
        if ((_ = m[y])) {
          for (y >= p && (p = y + 1); !(x = v[p]) && ++p < g; );
          _._next = x || null
        }
    }
    return ((a = new Je(a, r)), (a._enter = s), (a._exit = l), a)
  }
  function UD(e) {
    return typeof e == 'object' && 'length' in e ? e : Array.from(e)
  }
  function YD() {
    return new Je(this._exit || this._groups.map(V1), this._parents)
  }
  function XD(e, t, n) {
    var r = this.enter(),
      o = this,
      i = this.exit()
    return (
      typeof e == 'function' ? ((r = e(r)), r && (r = r.selection())) : (r = r.append(e + '')),
      t != null && ((o = t(o)), o && (o = o.selection())),
      n == null ? i.remove() : n(i),
      r && o ? r.merge(o).order() : o
    )
  }
  function KD(e) {
    for (
      var t = e.selection ? e.selection() : e,
        n = this._groups,
        r = t._groups,
        o = n.length,
        i = r.length,
        a = Math.min(o, i),
        s = new Array(o),
        l = 0;
      l < a;
      ++l
    )
      for (var u = n[l], c = r[l], d = u.length, f = (s[l] = new Array(d)), h, g = 0; g < d; ++g)
        (h = u[g] || c[g]) && (f[g] = h)
    for (; l < o; ++l) s[l] = n[l]
    return new Je(s, this._parents)
  }
  function ZD() {
    for (var e = this._groups, t = -1, n = e.length; ++t < n; )
      for (var r = e[t], o = r.length - 1, i = r[o], a; --o >= 0; )
        (a = r[o]) &&
          (i && a.compareDocumentPosition(i) ^ 4 && i.parentNode.insertBefore(a, i), (i = a))
    return this
  }
  function JD(e) {
    e || (e = QD)
    function t(d, f) {
      return d && f ? e(d.__data__, f.__data__) : !d - !f
    }
    for (var n = this._groups, r = n.length, o = new Array(r), i = 0; i < r; ++i) {
      for (var a = n[i], s = a.length, l = (o[i] = new Array(s)), u, c = 0; c < s; ++c)
        (u = a[c]) && (l[c] = u)
      l.sort(t)
    }
    return new Je(o, this._parents).order()
  }
  function QD(e, t) {
    return e < t ? -1 : e > t ? 1 : e >= t ? 0 : NaN
  }
  function e2() {
    var e = arguments[0]
    return ((arguments[0] = this), e.apply(null, arguments), this)
  }
  function t2() {
    return Array.from(this)
  }
  function n2() {
    for (var e = this._groups, t = 0, n = e.length; t < n; ++t)
      for (var r = e[t], o = 0, i = r.length; o < i; ++o) {
        var a = r[o]
        if (a) return a
      }
    return null
  }
  function r2() {
    let e = 0
    for (const t of this) ++e
    return e
  }
  function o2() {
    return !this.node()
  }
  function i2(e) {
    for (var t = this._groups, n = 0, r = t.length; n < r; ++n)
      for (var o = t[n], i = 0, a = o.length, s; i < a; ++i)
        (s = o[i]) && e.call(s, s.__data__, i, o)
    return this
  }
  function a2(e) {
    return function () {
      this.removeAttribute(e)
    }
  }
  function s2(e) {
    return function () {
      this.removeAttributeNS(e.space, e.local)
    }
  }
  function l2(e, t) {
    return function () {
      this.setAttribute(e, t)
    }
  }
  function u2(e, t) {
    return function () {
      this.setAttributeNS(e.space, e.local, t)
    }
  }
  function c2(e, t) {
    return function () {
      var n = t.apply(this, arguments)
      n == null ? this.removeAttribute(e) : this.setAttribute(e, n)
    }
  }
  function d2(e, t) {
    return function () {
      var n = t.apply(this, arguments)
      n == null
        ? this.removeAttributeNS(e.space, e.local)
        : this.setAttributeNS(e.space, e.local, n)
    }
  }
  function f2(e, t) {
    var n = $i(e)
    if (arguments.length < 2) {
      var r = this.node()
      return n.local ? r.getAttributeNS(n.space, n.local) : r.getAttribute(n)
    }
    return this.each(
      (t == null
        ? n.local
          ? s2
          : a2
        : typeof t == 'function'
          ? n.local
            ? d2
            : c2
          : n.local
            ? u2
            : l2)(n, t)
    )
  }
  function G1(e) {
    return (e.ownerDocument && e.ownerDocument.defaultView) || (e.document && e) || e.defaultView
  }
  function h2(e) {
    return function () {
      this.style.removeProperty(e)
    }
  }
  function p2(e, t, n) {
    return function () {
      this.style.setProperty(e, t, n)
    }
  }
  function v2(e, t, n) {
    return function () {
      var r = t.apply(this, arguments)
      r == null ? this.style.removeProperty(e) : this.style.setProperty(e, r, n)
    }
  }
  function g2(e, t, n) {
    return arguments.length > 1
      ? this.each((t == null ? h2 : typeof t == 'function' ? v2 : p2)(e, t, n ?? ''))
      : Vn(this.node(), e)
  }
  function Vn(e, t) {
    return e.style.getPropertyValue(t) || G1(e).getComputedStyle(e, null).getPropertyValue(t)
  }
  function m2(e) {
    return function () {
      delete this[e]
    }
  }
  function y2(e, t) {
    return function () {
      this[e] = t
    }
  }
  function b2(e, t) {
    return function () {
      var n = t.apply(this, arguments)
      n == null ? delete this[e] : (this[e] = n)
    }
  }
  function _2(e, t) {
    return arguments.length > 1
      ? this.each((t == null ? m2 : typeof t == 'function' ? b2 : y2)(e, t))
      : this.node()[e]
  }
  function W1(e) {
    return e.trim().split(/^|\s+/)
  }
  function Qf(e) {
    return e.classList || new U1(e)
  }
  function U1(e) {
    ;((this._node = e), (this._names = W1(e.getAttribute('class') || '')))
  }
  U1.prototype = {
    add: function (e) {
      var t = this._names.indexOf(e)
      t < 0 && (this._names.push(e), this._node.setAttribute('class', this._names.join(' ')))
    },
    remove: function (e) {
      var t = this._names.indexOf(e)
      t >= 0 && (this._names.splice(t, 1), this._node.setAttribute('class', this._names.join(' ')))
    },
    contains: function (e) {
      return this._names.indexOf(e) >= 0
    },
  }
  function Y1(e, t) {
    for (var n = Qf(e), r = -1, o = t.length; ++r < o; ) n.add(t[r])
  }
  function X1(e, t) {
    for (var n = Qf(e), r = -1, o = t.length; ++r < o; ) n.remove(t[r])
  }
  function w2(e) {
    return function () {
      Y1(this, e)
    }
  }
  function S2(e) {
    return function () {
      X1(this, e)
    }
  }
  function x2(e, t) {
    return function () {
      ;(t.apply(this, arguments) ? Y1 : X1)(this, e)
    }
  }
  function C2(e, t) {
    var n = W1(e + '')
    if (arguments.length < 2) {
      for (var r = Qf(this.node()), o = -1, i = n.length; ++o < i; )
        if (!r.contains(n[o])) return !1
      return !0
    }
    return this.each((typeof t == 'function' ? x2 : t ? w2 : S2)(n, t))
  }
  function E2() {
    this.textContent = ''
  }
  function $2(e) {
    return function () {
      this.textContent = e
    }
  }
  function T2(e) {
    return function () {
      var t = e.apply(this, arguments)
      this.textContent = t ?? ''
    }
  }
  function O2(e) {
    return arguments.length
      ? this.each(e == null ? E2 : (typeof e == 'function' ? T2 : $2)(e))
      : this.node().textContent
  }
  function P2() {
    this.innerHTML = ''
  }
  function I2(e) {
    return function () {
      this.innerHTML = e
    }
  }
  function A2(e) {
    return function () {
      var t = e.apply(this, arguments)
      this.innerHTML = t ?? ''
    }
  }
  function N2(e) {
    return arguments.length
      ? this.each(e == null ? P2 : (typeof e == 'function' ? A2 : I2)(e))
      : this.node().innerHTML
  }
  function R2() {
    this.nextSibling && this.parentNode.appendChild(this)
  }
  function M2() {
    return this.each(R2)
  }
  function D2() {
    this.previousSibling && this.parentNode.insertBefore(this, this.parentNode.firstChild)
  }
  function B2() {
    return this.each(D2)
  }
  function q2(e) {
    var t = typeof e == 'function' ? e : F1(e)
    return this.select(function () {
      return this.appendChild(t.apply(this, arguments))
    })
  }
  function z2() {
    return null
  }
  function L2(e, t) {
    var n = typeof e == 'function' ? e : F1(e),
      r = t == null ? z2 : typeof t == 'function' ? t : Jf(t)
    return this.select(function () {
      return this.insertBefore(n.apply(this, arguments), r.apply(this, arguments) || null)
    })
  }
  function F2() {
    var e = this.parentNode
    e && e.removeChild(this)
  }
  function k2() {
    return this.each(F2)
  }
  function H2() {
    var e = this.cloneNode(!1),
      t = this.parentNode
    return t ? t.insertBefore(e, this.nextSibling) : e
  }
  function j2() {
    var e = this.cloneNode(!0),
      t = this.parentNode
    return t ? t.insertBefore(e, this.nextSibling) : e
  }
  function V2(e) {
    return this.select(e ? j2 : H2)
  }
  function G2(e) {
    return arguments.length ? this.property('__data__', e) : this.node().__data__
  }
  function W2(e) {
    return function (t) {
      e.call(this, t, this.__data__)
    }
  }
  function U2(e) {
    return e
      .trim()
      .split(/^|\s+/)
      .map(function (t) {
        var n = '',
          r = t.indexOf('.')
        return (r >= 0 && ((n = t.slice(r + 1)), (t = t.slice(0, r))), { type: t, name: n })
      })
  }
  function Y2(e) {
    return function () {
      var t = this.__on
      if (t) {
        for (var n = 0, r = -1, o = t.length, i; n < o; ++n)
          ((i = t[n]),
            (!e.type || i.type === e.type) && i.name === e.name
              ? this.removeEventListener(i.type, i.listener, i.options)
              : (t[++r] = i))
        ++r ? (t.length = r) : delete this.__on
      }
    }
  }
  function X2(e, t, n) {
    return function () {
      var r = this.__on,
        o,
        i = W2(t)
      if (r) {
        for (var a = 0, s = r.length; a < s; ++a)
          if ((o = r[a]).type === e.type && o.name === e.name) {
            ;(this.removeEventListener(o.type, o.listener, o.options),
              this.addEventListener(o.type, (o.listener = i), (o.options = n)),
              (o.value = t))
            return
          }
      }
      ;(this.addEventListener(e.type, i, n),
        (o = { type: e.type, name: e.name, value: t, listener: i, options: n }),
        r ? r.push(o) : (this.__on = [o]))
    }
  }
  function K2(e, t, n) {
    var r = U2(e + ''),
      o,
      i = r.length,
      a
    if (arguments.length < 2) {
      var s = this.node().__on
      if (s) {
        for (var l = 0, u = s.length, c; l < u; ++l)
          for (o = 0, c = s[l]; o < i; ++o)
            if ((a = r[o]).type === c.type && a.name === c.name) return c.value
      }
      return
    }
    for (s = t ? X2 : Y2, o = 0; o < i; ++o) this.each(s(r[o], t, n))
    return this
  }
  function K1(e, t, n) {
    var r = G1(e),
      o = r.CustomEvent
    ;(typeof o == 'function'
      ? (o = new o(t, n))
      : ((o = r.document.createEvent('Event')),
        n
          ? (o.initEvent(t, n.bubbles, n.cancelable), (o.detail = n.detail))
          : o.initEvent(t, !1, !1)),
      e.dispatchEvent(o))
  }
  function Z2(e, t) {
    return function () {
      return K1(this, e, t)
    }
  }
  function J2(e, t) {
    return function () {
      return K1(this, e, t.apply(this, arguments))
    }
  }
  function Q2(e, t) {
    return this.each((typeof t == 'function' ? J2 : Z2)(e, t))
  }
  function* eB() {
    for (var e = this._groups, t = 0, n = e.length; t < n; ++t)
      for (var r = e[t], o = 0, i = r.length, a; o < i; ++o) (a = r[o]) && (yield a)
  }
  var Z1 = [null]
  function Je(e, t) {
    ;((this._groups = e), (this._parents = t))
  }
  function Xr() {
    return new Je([[document.documentElement]], Z1)
  }
  function tB() {
    return this
  }
  Je.prototype = Xr.prototype = {
    constructor: Je,
    select: TD,
    selectAll: AD,
    selectChild: DD,
    selectChildren: LD,
    filter: FD,
    data: WD,
    enter: kD,
    exit: YD,
    join: XD,
    merge: KD,
    selection: tB,
    order: ZD,
    sort: JD,
    call: e2,
    nodes: t2,
    node: n2,
    size: r2,
    empty: o2,
    each: i2,
    attr: f2,
    style: g2,
    property: _2,
    classed: C2,
    text: O2,
    html: N2,
    raise: M2,
    lower: B2,
    append: q2,
    insert: L2,
    remove: k2,
    clone: V2,
    datum: G2,
    on: K2,
    dispatch: Q2,
    [Symbol.iterator]: eB,
  }
  function lt(e) {
    return typeof e == 'string'
      ? new Je([[document.querySelector(e)]], [document.documentElement])
      : new Je([[e]], Z1)
  }
  function nB(e) {
    let t
    for (; (t = e.sourceEvent); ) e = t
    return e
  }
  function vt(e, t) {
    if (((e = nB(e)), t === void 0 && (t = e.currentTarget), t)) {
      var n = t.ownerSVGElement || t
      if (n.createSVGPoint) {
        var r = n.createSVGPoint()
        return (
          (r.x = e.clientX),
          (r.y = e.clientY),
          (r = r.matrixTransform(t.getScreenCTM().inverse())),
          [r.x, r.y]
        )
      }
      if (t.getBoundingClientRect) {
        var o = t.getBoundingClientRect()
        return [e.clientX - o.left - t.clientLeft, e.clientY - o.top - t.clientTop]
      }
    }
    return [e.pageX, e.pageY]
  }
  const rB = { passive: !1 },
    Nr = { capture: !0, passive: !1 }
  function pd(e) {
    e.stopImmediatePropagation()
  }
  function Bn(e) {
    ;(e.preventDefault(), e.stopImmediatePropagation())
  }
  function J1(e) {
    var t = e.document.documentElement,
      n = lt(e).on('dragstart.drag', Bn, Nr)
    'onselectstart' in t
      ? n.on('selectstart.drag', Bn, Nr)
      : ((t.__noselect = t.style.MozUserSelect), (t.style.MozUserSelect = 'none'))
  }
  function Q1(e, t) {
    var n = e.document.documentElement,
      r = lt(e).on('dragstart.drag', null)
    ;(t &&
      (r.on('click.drag', Bn, Nr),
      setTimeout(function () {
        r.on('click.drag', null)
      }, 0)),
      'onselectstart' in n
        ? r.on('selectstart.drag', null)
        : ((n.style.MozUserSelect = n.__noselect), delete n.__noselect))
  }
  const uo = (e) => () => e
  function Vd(
    e,
    {
      sourceEvent: t,
      subject: n,
      target: r,
      identifier: o,
      active: i,
      x: a,
      y: s,
      dx: l,
      dy: u,
      dispatch: c,
    }
  ) {
    Object.defineProperties(this, {
      type: { value: e, enumerable: !0, configurable: !0 },
      sourceEvent: { value: t, enumerable: !0, configurable: !0 },
      subject: { value: n, enumerable: !0, configurable: !0 },
      target: { value: r, enumerable: !0, configurable: !0 },
      identifier: { value: o, enumerable: !0, configurable: !0 },
      active: { value: i, enumerable: !0, configurable: !0 },
      x: { value: a, enumerable: !0, configurable: !0 },
      y: { value: s, enumerable: !0, configurable: !0 },
      dx: { value: l, enumerable: !0, configurable: !0 },
      dy: { value: u, enumerable: !0, configurable: !0 },
      _: { value: c },
    })
  }
  Vd.prototype.on = function () {
    var e = this._.on.apply(this._, arguments)
    return e === this._ ? this : e
  }
  function oB(e) {
    return !e.ctrlKey && !e.button
  }
  function iB() {
    return this.parentNode
  }
  function aB(e, t) {
    return t ?? { x: e.x, y: e.y }
  }
  function sB() {
    return navigator.maxTouchPoints || 'ontouchstart' in this
  }
  function lB() {
    var e = oB,
      t = iB,
      n = aB,
      r = sB,
      o = {},
      i = Ei('start', 'drag', 'end'),
      a = 0,
      s,
      l,
      u,
      c,
      d = 0
    function f(_) {
      _.on('mousedown.drag', h)
        .filter(r)
        .on('touchstart.drag', v)
        .on('touchmove.drag', b, rB)
        .on('touchend.drag touchcancel.drag', y)
        .style('touch-action', 'none')
        .style('-webkit-tap-highlight-color', 'rgba(0,0,0,0)')
    }
    function h(_, x) {
      if (!(c || !e.call(this, _, x))) {
        var S = p(this, t.call(this, _, x), _, x, 'mouse')
        S &&
          (lt(_.view).on('mousemove.drag', g, Nr).on('mouseup.drag', m, Nr),
          J1(_.view),
          pd(_),
          (u = !1),
          (s = _.clientX),
          (l = _.clientY),
          S('start', _))
      }
    }
    function g(_) {
      if ((Bn(_), !u)) {
        var x = _.clientX - s,
          S = _.clientY - l
        u = x * x + S * S > d
      }
      o.mouse('drag', _)
    }
    function m(_) {
      ;(lt(_.view).on('mousemove.drag mouseup.drag', null), Q1(_.view, u), Bn(_), o.mouse('end', _))
    }
    function v(_, x) {
      if (e.call(this, _, x)) {
        var S = _.changedTouches,
          w = t.call(this, _, x),
          T = S.length,
          A,
          $
        for (A = 0; A < T; ++A)
          ($ = p(this, w, _, x, S[A].identifier, S[A])) && (pd(_), $('start', _, S[A]))
      }
    }
    function b(_) {
      var x = _.changedTouches,
        S = x.length,
        w,
        T
      for (w = 0; w < S; ++w) (T = o[x[w].identifier]) && (Bn(_), T('drag', _, x[w]))
    }
    function y(_) {
      var x = _.changedTouches,
        S = x.length,
        w,
        T
      for (
        c && clearTimeout(c),
          c = setTimeout(function () {
            c = null
          }, 500),
          w = 0;
        w < S;
        ++w
      )
        (T = o[x[w].identifier]) && (pd(_), T('end', _, x[w]))
    }
    function p(_, x, S, w, T, A) {
      var $ = i.copy(),
        P = vt(A || S, x),
        E,
        z,
        C
      if (
        (C = n.call(
          _,
          new Vd('beforestart', {
            sourceEvent: S,
            target: f,
            identifier: T,
            active: a,
            x: P[0],
            y: P[1],
            dx: 0,
            dy: 0,
            dispatch: $,
          }),
          w
        )) != null
      )
        return (
          (E = C.x - P[0] || 0),
          (z = C.y - P[1] || 0),
          function R(N, j, V) {
            var H = P,
              G
            switch (N) {
              case 'start':
                ;((o[T] = R), (G = a++))
                break
              case 'end':
                ;(delete o[T], --a)
              case 'drag':
                ;((P = vt(V || j, x)), (G = a))
                break
            }
            $.call(
              N,
              _,
              new Vd(N, {
                sourceEvent: j,
                subject: C,
                target: f,
                identifier: T,
                active: G,
                x: P[0] + E,
                y: P[1] + z,
                dx: P[0] - H[0],
                dy: P[1] - H[1],
                dispatch: $,
              }),
              w
            )
          }
        )
    }
    return (
      (f.filter = function (_) {
        return arguments.length ? ((e = typeof _ == 'function' ? _ : uo(!!_)), f) : e
      }),
      (f.container = function (_) {
        return arguments.length ? ((t = typeof _ == 'function' ? _ : uo(_)), f) : t
      }),
      (f.subject = function (_) {
        return arguments.length ? ((n = typeof _ == 'function' ? _ : uo(_)), f) : n
      }),
      (f.touchable = function (_) {
        return arguments.length ? ((r = typeof _ == 'function' ? _ : uo(!!_)), f) : r
      }),
      (f.on = function () {
        var _ = i.on.apply(i, arguments)
        return _ === i ? f : _
      }),
      (f.clickDistance = function (_) {
        return arguments.length ? ((d = (_ = +_) * _), f) : Math.sqrt(d)
      }),
      f
    )
  }
  function eh(e, t, n) {
    ;((e.prototype = t.prototype = n), (n.constructor = e))
  }
  function eS(e, t) {
    var n = Object.create(e.prototype)
    for (var r in t) n[r] = t[r]
    return n
  }
  function Kr() {}
  var Rr = 0.7,
    Fo = 1 / Rr,
    qn = '\\s*([+-]?\\d+)\\s*',
    Mr = '\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)\\s*',
    wt = '\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)%\\s*',
    uB = /^#([0-9a-f]{3,8})$/,
    cB = new RegExp(`^rgb\\(${qn},${qn},${qn}\\)$`),
    dB = new RegExp(`^rgb\\(${wt},${wt},${wt}\\)$`),
    fB = new RegExp(`^rgba\\(${qn},${qn},${qn},${Mr}\\)$`),
    hB = new RegExp(`^rgba\\(${wt},${wt},${wt},${Mr}\\)$`),
    pB = new RegExp(`^hsl\\(${Mr},${wt},${wt}\\)$`),
    vB = new RegExp(`^hsla\\(${Mr},${wt},${wt},${Mr}\\)$`),
    b0 = {
      aliceblue: 15792383,
      antiquewhite: 16444375,
      aqua: 65535,
      aquamarine: 8388564,
      azure: 15794175,
      beige: 16119260,
      bisque: 16770244,
      black: 0,
      blanchedalmond: 16772045,
      blue: 255,
      blueviolet: 9055202,
      brown: 10824234,
      burlywood: 14596231,
      cadetblue: 6266528,
      chartreuse: 8388352,
      chocolate: 13789470,
      coral: 16744272,
      cornflowerblue: 6591981,
      cornsilk: 16775388,
      crimson: 14423100,
      cyan: 65535,
      darkblue: 139,
      darkcyan: 35723,
      darkgoldenrod: 12092939,
      darkgray: 11119017,
      darkgreen: 25600,
      darkgrey: 11119017,
      darkkhaki: 12433259,
      darkmagenta: 9109643,
      darkolivegreen: 5597999,
      darkorange: 16747520,
      darkorchid: 10040012,
      darkred: 9109504,
      darksalmon: 15308410,
      darkseagreen: 9419919,
      darkslateblue: 4734347,
      darkslategray: 3100495,
      darkslategrey: 3100495,
      darkturquoise: 52945,
      darkviolet: 9699539,
      deeppink: 16716947,
      deepskyblue: 49151,
      dimgray: 6908265,
      dimgrey: 6908265,
      dodgerblue: 2003199,
      firebrick: 11674146,
      floralwhite: 16775920,
      forestgreen: 2263842,
      fuchsia: 16711935,
      gainsboro: 14474460,
      ghostwhite: 16316671,
      gold: 16766720,
      goldenrod: 14329120,
      gray: 8421504,
      green: 32768,
      greenyellow: 11403055,
      grey: 8421504,
      honeydew: 15794160,
      hotpink: 16738740,
      indianred: 13458524,
      indigo: 4915330,
      ivory: 16777200,
      khaki: 15787660,
      lavender: 15132410,
      lavenderblush: 16773365,
      lawngreen: 8190976,
      lemonchiffon: 16775885,
      lightblue: 11393254,
      lightcoral: 15761536,
      lightcyan: 14745599,
      lightgoldenrodyellow: 16448210,
      lightgray: 13882323,
      lightgreen: 9498256,
      lightgrey: 13882323,
      lightpink: 16758465,
      lightsalmon: 16752762,
      lightseagreen: 2142890,
      lightskyblue: 8900346,
      lightslategray: 7833753,
      lightslategrey: 7833753,
      lightsteelblue: 11584734,
      lightyellow: 16777184,
      lime: 65280,
      limegreen: 3329330,
      linen: 16445670,
      magenta: 16711935,
      maroon: 8388608,
      mediumaquamarine: 6737322,
      mediumblue: 205,
      mediumorchid: 12211667,
      mediumpurple: 9662683,
      mediumseagreen: 3978097,
      mediumslateblue: 8087790,
      mediumspringgreen: 64154,
      mediumturquoise: 4772300,
      mediumvioletred: 13047173,
      midnightblue: 1644912,
      mintcream: 16121850,
      mistyrose: 16770273,
      moccasin: 16770229,
      navajowhite: 16768685,
      navy: 128,
      oldlace: 16643558,
      olive: 8421376,
      olivedrab: 7048739,
      orange: 16753920,
      orangered: 16729344,
      orchid: 14315734,
      palegoldenrod: 15657130,
      palegreen: 10025880,
      paleturquoise: 11529966,
      palevioletred: 14381203,
      papayawhip: 16773077,
      peachpuff: 16767673,
      peru: 13468991,
      pink: 16761035,
      plum: 14524637,
      powderblue: 11591910,
      purple: 8388736,
      rebeccapurple: 6697881,
      red: 16711680,
      rosybrown: 12357519,
      royalblue: 4286945,
      saddlebrown: 9127187,
      salmon: 16416882,
      sandybrown: 16032864,
      seagreen: 3050327,
      seashell: 16774638,
      sienna: 10506797,
      silver: 12632256,
      skyblue: 8900331,
      slateblue: 6970061,
      slategray: 7372944,
      slategrey: 7372944,
      snow: 16775930,
      springgreen: 65407,
      steelblue: 4620980,
      tan: 13808780,
      teal: 32896,
      thistle: 14204888,
      tomato: 16737095,
      turquoise: 4251856,
      violet: 15631086,
      wheat: 16113331,
      white: 16777215,
      whitesmoke: 16119285,
      yellow: 16776960,
      yellowgreen: 10145074,
    }
  eh(Kr, _n, {
    copy(e) {
      return Object.assign(new this.constructor(), this, e)
    },
    displayable() {
      return this.rgb().displayable()
    },
    hex: _0,
    formatHex: _0,
    formatHex8: gB,
    formatHsl: mB,
    formatRgb: w0,
    toString: w0,
  })
  function _0() {
    return this.rgb().formatHex()
  }
  function gB() {
    return this.rgb().formatHex8()
  }
  function mB() {
    return tS(this).formatHsl()
  }
  function w0() {
    return this.rgb().formatRgb()
  }
  function _n(e) {
    var t, n
    return (
      (e = (e + '').trim().toLowerCase()),
      (t = uB.exec(e))
        ? ((n = t[1].length),
          (t = parseInt(t[1], 16)),
          n === 6
            ? S0(t)
            : n === 3
              ? new We(
                  ((t >> 8) & 15) | ((t >> 4) & 240),
                  ((t >> 4) & 15) | (t & 240),
                  ((t & 15) << 4) | (t & 15),
                  1
                )
              : n === 8
                ? co((t >> 24) & 255, (t >> 16) & 255, (t >> 8) & 255, (t & 255) / 255)
                : n === 4
                  ? co(
                      ((t >> 12) & 15) | ((t >> 8) & 240),
                      ((t >> 8) & 15) | ((t >> 4) & 240),
                      ((t >> 4) & 15) | (t & 240),
                      (((t & 15) << 4) | (t & 15)) / 255
                    )
                  : null)
        : (t = cB.exec(e))
          ? new We(t[1], t[2], t[3], 1)
          : (t = dB.exec(e))
            ? new We((t[1] * 255) / 100, (t[2] * 255) / 100, (t[3] * 255) / 100, 1)
            : (t = fB.exec(e))
              ? co(t[1], t[2], t[3], t[4])
              : (t = hB.exec(e))
                ? co((t[1] * 255) / 100, (t[2] * 255) / 100, (t[3] * 255) / 100, t[4])
                : (t = pB.exec(e))
                  ? E0(t[1], t[2] / 100, t[3] / 100, 1)
                  : (t = vB.exec(e))
                    ? E0(t[1], t[2] / 100, t[3] / 100, t[4])
                    : b0.hasOwnProperty(e)
                      ? S0(b0[e])
                      : e === 'transparent'
                        ? new We(NaN, NaN, NaN, 0)
                        : null
    )
  }
  function S0(e) {
    return new We((e >> 16) & 255, (e >> 8) & 255, e & 255, 1)
  }
  function co(e, t, n, r) {
    return (r <= 0 && (e = t = n = NaN), new We(e, t, n, r))
  }
  function yB(e) {
    return (
      e instanceof Kr || (e = _n(e)),
      e ? ((e = e.rgb()), new We(e.r, e.g, e.b, e.opacity)) : new We()
    )
  }
  function Gd(e, t, n, r) {
    return arguments.length === 1 ? yB(e) : new We(e, t, n, r ?? 1)
  }
  function We(e, t, n, r) {
    ;((this.r = +e), (this.g = +t), (this.b = +n), (this.opacity = +r))
  }
  eh(
    We,
    Gd,
    eS(Kr, {
      brighter(e) {
        return (
          (e = e == null ? Fo : Math.pow(Fo, e)),
          new We(this.r * e, this.g * e, this.b * e, this.opacity)
        )
      },
      darker(e) {
        return (
          (e = e == null ? Rr : Math.pow(Rr, e)),
          new We(this.r * e, this.g * e, this.b * e, this.opacity)
        )
      },
      rgb() {
        return this
      },
      clamp() {
        return new We(gn(this.r), gn(this.g), gn(this.b), ko(this.opacity))
      },
      displayable() {
        return (
          -0.5 <= this.r &&
          this.r < 255.5 &&
          -0.5 <= this.g &&
          this.g < 255.5 &&
          -0.5 <= this.b &&
          this.b < 255.5 &&
          0 <= this.opacity &&
          this.opacity <= 1
        )
      },
      hex: x0,
      formatHex: x0,
      formatHex8: bB,
      formatRgb: C0,
      toString: C0,
    })
  )
  function x0() {
    return `#${pn(this.r)}${pn(this.g)}${pn(this.b)}`
  }
  function bB() {
    return `#${pn(this.r)}${pn(this.g)}${pn(this.b)}${pn((isNaN(this.opacity) ? 1 : this.opacity) * 255)}`
  }
  function C0() {
    const e = ko(this.opacity)
    return `${e === 1 ? 'rgb(' : 'rgba('}${gn(this.r)}, ${gn(this.g)}, ${gn(this.b)}${e === 1 ? ')' : `, ${e})`}`
  }
  function ko(e) {
    return isNaN(e) ? 1 : Math.max(0, Math.min(1, e))
  }
  function gn(e) {
    return Math.max(0, Math.min(255, Math.round(e) || 0))
  }
  function pn(e) {
    return ((e = gn(e)), (e < 16 ? '0' : '') + e.toString(16))
  }
  function E0(e, t, n, r) {
    return (
      r <= 0 ? (e = t = n = NaN) : n <= 0 || n >= 1 ? (e = t = NaN) : t <= 0 && (e = NaN),
      new ut(e, t, n, r)
    )
  }
  function tS(e) {
    if (e instanceof ut) return new ut(e.h, e.s, e.l, e.opacity)
    if ((e instanceof Kr || (e = _n(e)), !e)) return new ut()
    if (e instanceof ut) return e
    e = e.rgb()
    var t = e.r / 255,
      n = e.g / 255,
      r = e.b / 255,
      o = Math.min(t, n, r),
      i = Math.max(t, n, r),
      a = NaN,
      s = i - o,
      l = (i + o) / 2
    return (
      s
        ? (t === i
            ? (a = (n - r) / s + (n < r) * 6)
            : n === i
              ? (a = (r - t) / s + 2)
              : (a = (t - n) / s + 4),
          (s /= l < 0.5 ? i + o : 2 - i - o),
          (a *= 60))
        : (s = l > 0 && l < 1 ? 0 : a),
      new ut(a, s, l, e.opacity)
    )
  }
  function _B(e, t, n, r) {
    return arguments.length === 1 ? tS(e) : new ut(e, t, n, r ?? 1)
  }
  function ut(e, t, n, r) {
    ;((this.h = +e), (this.s = +t), (this.l = +n), (this.opacity = +r))
  }
  eh(
    ut,
    _B,
    eS(Kr, {
      brighter(e) {
        return (
          (e = e == null ? Fo : Math.pow(Fo, e)),
          new ut(this.h, this.s, this.l * e, this.opacity)
        )
      },
      darker(e) {
        return (
          (e = e == null ? Rr : Math.pow(Rr, e)),
          new ut(this.h, this.s, this.l * e, this.opacity)
        )
      },
      rgb() {
        var e = (this.h % 360) + (this.h < 0) * 360,
          t = isNaN(e) || isNaN(this.s) ? 0 : this.s,
          n = this.l,
          r = n + (n < 0.5 ? n : 1 - n) * t,
          o = 2 * n - r
        return new We(
          vd(e >= 240 ? e - 240 : e + 120, o, r),
          vd(e, o, r),
          vd(e < 120 ? e + 240 : e - 120, o, r),
          this.opacity
        )
      },
      clamp() {
        return new ut($0(this.h), fo(this.s), fo(this.l), ko(this.opacity))
      },
      displayable() {
        return (
          ((0 <= this.s && this.s <= 1) || isNaN(this.s)) &&
          0 <= this.l &&
          this.l <= 1 &&
          0 <= this.opacity &&
          this.opacity <= 1
        )
      },
      formatHsl() {
        const e = ko(this.opacity)
        return `${e === 1 ? 'hsl(' : 'hsla('}${$0(this.h)}, ${fo(this.s) * 100}%, ${fo(this.l) * 100}%${e === 1 ? ')' : `, ${e})`}`
      },
    })
  )
  function $0(e) {
    return ((e = (e || 0) % 360), e < 0 ? e + 360 : e)
  }
  function fo(e) {
    return Math.max(0, Math.min(1, e || 0))
  }
  function vd(e, t, n) {
    return (
      (e < 60
        ? t + ((n - t) * e) / 60
        : e < 180
          ? n
          : e < 240
            ? t + ((n - t) * (240 - e)) / 60
            : t) * 255
    )
  }
  const th = (e) => () => e
  function wB(e, t) {
    return function (n) {
      return e + n * t
    }
  }
  function SB(e, t, n) {
    return (
      (e = Math.pow(e, n)),
      (t = Math.pow(t, n) - e),
      (n = 1 / n),
      function (r) {
        return Math.pow(e + r * t, n)
      }
    )
  }
  function xB(e) {
    return (e = +e) == 1
      ? nS
      : function (t, n) {
          return n - t ? SB(t, n, e) : th(isNaN(t) ? n : t)
        }
  }
  function nS(e, t) {
    var n = t - e
    return n ? wB(e, n) : th(isNaN(e) ? t : e)
  }
  const Ho = (function e(t) {
    var n = xB(t)
    function r(o, i) {
      var a = n((o = Gd(o)).r, (i = Gd(i)).r),
        s = n(o.g, i.g),
        l = n(o.b, i.b),
        u = nS(o.opacity, i.opacity)
      return function (c) {
        return ((o.r = a(c)), (o.g = s(c)), (o.b = l(c)), (o.opacity = u(c)), o + '')
      }
    }
    return ((r.gamma = e), r)
  })(1)
  function CB(e, t) {
    t || (t = [])
    var n = e ? Math.min(t.length, e.length) : 0,
      r = t.slice(),
      o
    return function (i) {
      for (o = 0; o < n; ++o) r[o] = e[o] * (1 - i) + t[o] * i
      return r
    }
  }
  function EB(e) {
    return ArrayBuffer.isView(e) && !(e instanceof DataView)
  }
  function $B(e, t) {
    var n = t ? t.length : 0,
      r = e ? Math.min(n, e.length) : 0,
      o = new Array(r),
      i = new Array(n),
      a
    for (a = 0; a < r; ++a) o[a] = wr(e[a], t[a])
    for (; a < n; ++a) i[a] = t[a]
    return function (s) {
      for (a = 0; a < r; ++a) i[a] = o[a](s)
      return i
    }
  }
  function TB(e, t) {
    var n = new Date()
    return (
      (e = +e),
      (t = +t),
      function (r) {
        return (n.setTime(e * (1 - r) + t * r), n)
      }
    )
  }
  function gt(e, t) {
    return (
      (e = +e),
      (t = +t),
      function (n) {
        return e * (1 - n) + t * n
      }
    )
  }
  function OB(e, t) {
    var n = {},
      r = {},
      o
    ;((e === null || typeof e != 'object') && (e = {}),
      (t === null || typeof t != 'object') && (t = {}))
    for (o in t) o in e ? (n[o] = wr(e[o], t[o])) : (r[o] = t[o])
    return function (i) {
      for (o in n) r[o] = n[o](i)
      return r
    }
  }
  var Wd = /[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?/g,
    gd = new RegExp(Wd.source, 'g')
  function PB(e) {
    return function () {
      return e
    }
  }
  function IB(e) {
    return function (t) {
      return e(t) + ''
    }
  }
  function rS(e, t) {
    var n = (Wd.lastIndex = gd.lastIndex = 0),
      r,
      o,
      i,
      a = -1,
      s = [],
      l = []
    for (e = e + '', t = t + ''; (r = Wd.exec(e)) && (o = gd.exec(t)); )
      ((i = o.index) > n && ((i = t.slice(n, i)), s[a] ? (s[a] += i) : (s[++a] = i)),
        (r = r[0]) === (o = o[0])
          ? s[a]
            ? (s[a] += o)
            : (s[++a] = o)
          : ((s[++a] = null), l.push({ i: a, x: gt(r, o) })),
        (n = gd.lastIndex))
    return (
      n < t.length && ((i = t.slice(n)), s[a] ? (s[a] += i) : (s[++a] = i)),
      s.length < 2
        ? l[0]
          ? IB(l[0].x)
          : PB(t)
        : ((t = l.length),
          function (u) {
            for (var c = 0, d; c < t; ++c) s[(d = l[c]).i] = d.x(u)
            return s.join('')
          })
    )
  }
  function wr(e, t) {
    var n = typeof t,
      r
    return t == null || n === 'boolean'
      ? th(t)
      : (n === 'number'
          ? gt
          : n === 'string'
            ? (r = _n(t))
              ? ((t = r), Ho)
              : rS
            : t instanceof _n
              ? Ho
              : t instanceof Date
                ? TB
                : EB(t)
                  ? CB
                  : Array.isArray(t)
                    ? $B
                    : (typeof t.valueOf != 'function' && typeof t.toString != 'function') ||
                        isNaN(t)
                      ? OB
                      : gt)(e, t)
  }
  var T0 = 180 / Math.PI,
    Ud = { translateX: 0, translateY: 0, rotate: 0, skewX: 0, scaleX: 1, scaleY: 1 }
  function oS(e, t, n, r, o, i) {
    var a, s, l
    return (
      (a = Math.sqrt(e * e + t * t)) && ((e /= a), (t /= a)),
      (l = e * n + t * r) && ((n -= e * l), (r -= t * l)),
      (s = Math.sqrt(n * n + r * r)) && ((n /= s), (r /= s), (l /= s)),
      e * r < t * n && ((e = -e), (t = -t), (l = -l), (a = -a)),
      {
        translateX: o,
        translateY: i,
        rotate: Math.atan2(t, e) * T0,
        skewX: Math.atan(l) * T0,
        scaleX: a,
        scaleY: s,
      }
    )
  }
  var ho
  function AB(e) {
    const t = new (typeof DOMMatrix == 'function' ? DOMMatrix : WebKitCSSMatrix)(e + '')
    return t.isIdentity ? Ud : oS(t.a, t.b, t.c, t.d, t.e, t.f)
  }
  function NB(e) {
    return e == null ||
      (ho || (ho = document.createElementNS('http://www.w3.org/2000/svg', 'g')),
      ho.setAttribute('transform', e),
      !(e = ho.transform.baseVal.consolidate()))
      ? Ud
      : ((e = e.matrix), oS(e.a, e.b, e.c, e.d, e.e, e.f))
  }
  function iS(e, t, n, r) {
    function o(u) {
      return u.length ? u.pop() + ' ' : ''
    }
    function i(u, c, d, f, h, g) {
      if (u !== d || c !== f) {
        var m = h.push('translate(', null, t, null, n)
        g.push({ i: m - 4, x: gt(u, d) }, { i: m - 2, x: gt(c, f) })
      } else (d || f) && h.push('translate(' + d + t + f + n)
    }
    function a(u, c, d, f) {
      u !== c
        ? (u - c > 180 ? (c += 360) : c - u > 180 && (u += 360),
          f.push({ i: d.push(o(d) + 'rotate(', null, r) - 2, x: gt(u, c) }))
        : c && d.push(o(d) + 'rotate(' + c + r)
    }
    function s(u, c, d, f) {
      u !== c
        ? f.push({ i: d.push(o(d) + 'skewX(', null, r) - 2, x: gt(u, c) })
        : c && d.push(o(d) + 'skewX(' + c + r)
    }
    function l(u, c, d, f, h, g) {
      if (u !== d || c !== f) {
        var m = h.push(o(h) + 'scale(', null, ',', null, ')')
        g.push({ i: m - 4, x: gt(u, d) }, { i: m - 2, x: gt(c, f) })
      } else (d !== 1 || f !== 1) && h.push(o(h) + 'scale(' + d + ',' + f + ')')
    }
    return function (u, c) {
      var d = [],
        f = []
      return (
        (u = e(u)),
        (c = e(c)),
        i(u.translateX, u.translateY, c.translateX, c.translateY, d, f),
        a(u.rotate, c.rotate, d, f),
        s(u.skewX, c.skewX, d, f),
        l(u.scaleX, u.scaleY, c.scaleX, c.scaleY, d, f),
        (u = c = null),
        function (h) {
          for (var g = -1, m = f.length, v; ++g < m; ) d[(v = f[g]).i] = v.x(h)
          return d.join('')
        }
      )
    }
  }
  var RB = iS(AB, 'px, ', 'px)', 'deg)'),
    MB = iS(NB, ', ', ')', ')'),
    DB = 1e-12
  function O0(e) {
    return ((e = Math.exp(e)) + 1 / e) / 2
  }
  function BB(e) {
    return ((e = Math.exp(e)) - 1 / e) / 2
  }
  function qB(e) {
    return ((e = Math.exp(2 * e)) - 1) / (e + 1)
  }
  const xo = (function e(t, n, r) {
    function o(i, a) {
      var s = i[0],
        l = i[1],
        u = i[2],
        c = a[0],
        d = a[1],
        f = a[2],
        h = c - s,
        g = d - l,
        m = h * h + g * g,
        v,
        b
      if (m < DB)
        ((b = Math.log(f / u) / t),
          (v = function (w) {
            return [s + w * h, l + w * g, u * Math.exp(t * w * b)]
          }))
      else {
        var y = Math.sqrt(m),
          p = (f * f - u * u + r * m) / (2 * u * n * y),
          _ = (f * f - u * u - r * m) / (2 * f * n * y),
          x = Math.log(Math.sqrt(p * p + 1) - p),
          S = Math.log(Math.sqrt(_ * _ + 1) - _)
        ;((b = (S - x) / t),
          (v = function (w) {
            var T = w * b,
              A = O0(x),
              $ = (u / (n * y)) * (A * qB(t * T + x) - BB(x))
            return [s + $ * h, l + $ * g, (u * A) / O0(t * T + x)]
          }))
      }
      return ((v.duration = (b * 1e3 * t) / Math.SQRT2), v)
    }
    return (
      (o.rho = function (i) {
        var a = Math.max(0.001, +i),
          s = a * a,
          l = s * s
        return e(a, s, l)
      }),
      o
    )
  })(Math.SQRT2, 2, 4)
  var Gn = 0,
    fr = 0,
    ar = 0,
    aS = 1e3,
    jo,
    hr,
    Vo = 0,
    wn = 0,
    Ti = 0,
    Dr = typeof performance == 'object' && performance.now ? performance : Date,
    sS =
      typeof window == 'object' && window.requestAnimationFrame
        ? window.requestAnimationFrame.bind(window)
        : function (e) {
            setTimeout(e, 17)
          }
  function nh() {
    return wn || (sS(zB), (wn = Dr.now() + Ti))
  }
  function zB() {
    wn = 0
  }
  function Go() {
    this._call = this._time = this._next = null
  }
  Go.prototype = lS.prototype = {
    constructor: Go,
    restart: function (e, t, n) {
      if (typeof e != 'function') throw new TypeError('callback is not a function')
      ;((n = (n == null ? nh() : +n) + (t == null ? 0 : +t)),
        !this._next && hr !== this && (hr ? (hr._next = this) : (jo = this), (hr = this)),
        (this._call = e),
        (this._time = n),
        Yd())
    },
    stop: function () {
      this._call && ((this._call = null), (this._time = 1 / 0), Yd())
    },
  }
  function lS(e, t, n) {
    var r = new Go()
    return (r.restart(e, t, n), r)
  }
  function LB() {
    ;(nh(), ++Gn)
    for (var e = jo, t; e; ) ((t = wn - e._time) >= 0 && e._call.call(void 0, t), (e = e._next))
    --Gn
  }
  function P0() {
    ;((wn = (Vo = Dr.now()) + Ti), (Gn = fr = 0))
    try {
      LB()
    } finally {
      ;((Gn = 0), kB(), (wn = 0))
    }
  }
  function FB() {
    var e = Dr.now(),
      t = e - Vo
    t > aS && ((Ti -= t), (Vo = e))
  }
  function kB() {
    for (var e, t = jo, n, r = 1 / 0; t; )
      t._call
        ? (r > t._time && (r = t._time), (e = t), (t = t._next))
        : ((n = t._next), (t._next = null), (t = e ? (e._next = n) : (jo = n)))
    ;((hr = e), Yd(r))
  }
  function Yd(e) {
    if (!Gn) {
      fr && (fr = clearTimeout(fr))
      var t = e - wn
      t > 24
        ? (e < 1 / 0 && (fr = setTimeout(P0, e - Dr.now() - Ti)), ar && (ar = clearInterval(ar)))
        : (ar || ((Vo = Dr.now()), (ar = setInterval(FB, aS))), (Gn = 1), sS(P0))
    }
  }
  function I0(e, t, n) {
    var r = new Go()
    return (
      (t = t == null ? 0 : +t),
      r.restart(
        (o) => {
          ;(r.stop(), e(o + t))
        },
        t,
        n
      ),
      r
    )
  }
  var HB = Ei('start', 'end', 'cancel', 'interrupt'),
    jB = [],
    uS = 0,
    A0 = 1,
    Xd = 2,
    Co = 3,
    N0 = 4,
    Kd = 5,
    Eo = 6
  function Oi(e, t, n, r, o, i) {
    var a = e.__transition
    if (!a) e.__transition = {}
    else if (n in a) return
    VB(e, n, {
      name: t,
      index: r,
      group: o,
      on: HB,
      tween: jB,
      time: i.time,
      delay: i.delay,
      duration: i.duration,
      ease: i.ease,
      timer: null,
      state: uS,
    })
  }
  function rh(e, t) {
    var n = pt(e, t)
    if (n.state > uS) throw new Error('too late; already scheduled')
    return n
  }
  function Tt(e, t) {
    var n = pt(e, t)
    if (n.state > Co) throw new Error('too late; already running')
    return n
  }
  function pt(e, t) {
    var n = e.__transition
    if (!n || !(n = n[t])) throw new Error('transition not found')
    return n
  }
  function VB(e, t, n) {
    var r = e.__transition,
      o
    ;((r[t] = n), (n.timer = lS(i, 0, n.time)))
    function i(u) {
      ;((n.state = A0), n.timer.restart(a, n.delay, n.time), n.delay <= u && a(u - n.delay))
    }
    function a(u) {
      var c, d, f, h
      if (n.state !== A0) return l()
      for (c in r)
        if (((h = r[c]), h.name === n.name)) {
          if (h.state === Co) return I0(a)
          h.state === N0
            ? ((h.state = Eo),
              h.timer.stop(),
              h.on.call('interrupt', e, e.__data__, h.index, h.group),
              delete r[c])
            : +c < t &&
              ((h.state = Eo),
              h.timer.stop(),
              h.on.call('cancel', e, e.__data__, h.index, h.group),
              delete r[c])
        }
      if (
        (I0(function () {
          n.state === Co && ((n.state = N0), n.timer.restart(s, n.delay, n.time), s(u))
        }),
        (n.state = Xd),
        n.on.call('start', e, e.__data__, n.index, n.group),
        n.state === Xd)
      ) {
        for (n.state = Co, o = new Array((f = n.tween.length)), c = 0, d = -1; c < f; ++c)
          (h = n.tween[c].value.call(e, e.__data__, n.index, n.group)) && (o[++d] = h)
        o.length = d + 1
      }
    }
    function s(u) {
      for (
        var c =
            u < n.duration
              ? n.ease.call(null, u / n.duration)
              : (n.timer.restart(l), (n.state = Kd), 1),
          d = -1,
          f = o.length;
        ++d < f;

      )
        o[d].call(e, c)
      n.state === Kd && (n.on.call('end', e, e.__data__, n.index, n.group), l())
    }
    function l() {
      ;((n.state = Eo), n.timer.stop(), delete r[t])
      for (var u in r) return
      delete e.__transition
    }
  }
  function $o(e, t) {
    var n = e.__transition,
      r,
      o,
      i = !0,
      a
    if (n) {
      t = t == null ? null : t + ''
      for (a in n) {
        if ((r = n[a]).name !== t) {
          i = !1
          continue
        }
        ;((o = r.state > Xd && r.state < Kd),
          (r.state = Eo),
          r.timer.stop(),
          r.on.call(o ? 'interrupt' : 'cancel', e, e.__data__, r.index, r.group),
          delete n[a])
      }
      i && delete e.__transition
    }
  }
  function GB(e) {
    return this.each(function () {
      $o(this, e)
    })
  }
  function WB(e, t) {
    var n, r
    return function () {
      var o = Tt(this, e),
        i = o.tween
      if (i !== n) {
        r = n = i
        for (var a = 0, s = r.length; a < s; ++a)
          if (r[a].name === t) {
            ;((r = r.slice()), r.splice(a, 1))
            break
          }
      }
      o.tween = r
    }
  }
  function UB(e, t, n) {
    var r, o
    if (typeof n != 'function') throw new Error()
    return function () {
      var i = Tt(this, e),
        a = i.tween
      if (a !== r) {
        o = (r = a).slice()
        for (var s = { name: t, value: n }, l = 0, u = o.length; l < u; ++l)
          if (o[l].name === t) {
            o[l] = s
            break
          }
        l === u && o.push(s)
      }
      i.tween = o
    }
  }
  function YB(e, t) {
    var n = this._id
    if (((e += ''), arguments.length < 2)) {
      for (var r = pt(this.node(), n).tween, o = 0, i = r.length, a; o < i; ++o)
        if ((a = r[o]).name === e) return a.value
      return null
    }
    return this.each((t == null ? WB : UB)(n, e, t))
  }
  function oh(e, t, n) {
    var r = e._id
    return (
      e.each(function () {
        var o = Tt(this, r)
        ;(o.value || (o.value = {}))[t] = n.apply(this, arguments)
      }),
      function (o) {
        return pt(o, r).value[t]
      }
    )
  }
  function cS(e, t) {
    var n
    return (typeof t == 'number' ? gt : t instanceof _n ? Ho : (n = _n(t)) ? ((t = n), Ho) : rS)(
      e,
      t
    )
  }
  function XB(e) {
    return function () {
      this.removeAttribute(e)
    }
  }
  function KB(e) {
    return function () {
      this.removeAttributeNS(e.space, e.local)
    }
  }
  function ZB(e, t, n) {
    var r,
      o = n + '',
      i
    return function () {
      var a = this.getAttribute(e)
      return a === o ? null : a === r ? i : (i = t((r = a), n))
    }
  }
  function JB(e, t, n) {
    var r,
      o = n + '',
      i
    return function () {
      var a = this.getAttributeNS(e.space, e.local)
      return a === o ? null : a === r ? i : (i = t((r = a), n))
    }
  }
  function QB(e, t, n) {
    var r, o, i
    return function () {
      var a,
        s = n(this),
        l
      return s == null
        ? void this.removeAttribute(e)
        : ((a = this.getAttribute(e)),
          (l = s + ''),
          a === l ? null : a === r && l === o ? i : ((o = l), (i = t((r = a), s))))
    }
  }
  function eq(e, t, n) {
    var r, o, i
    return function () {
      var a,
        s = n(this),
        l
      return s == null
        ? void this.removeAttributeNS(e.space, e.local)
        : ((a = this.getAttributeNS(e.space, e.local)),
          (l = s + ''),
          a === l ? null : a === r && l === o ? i : ((o = l), (i = t((r = a), s))))
    }
  }
  function tq(e, t) {
    var n = $i(e),
      r = n === 'transform' ? MB : cS
    return this.attrTween(
      e,
      typeof t == 'function'
        ? (n.local ? eq : QB)(n, r, oh(this, 'attr.' + e, t))
        : t == null
          ? (n.local ? KB : XB)(n)
          : (n.local ? JB : ZB)(n, r, t)
    )
  }
  function nq(e, t) {
    return function (n) {
      this.setAttribute(e, t.call(this, n))
    }
  }
  function rq(e, t) {
    return function (n) {
      this.setAttributeNS(e.space, e.local, t.call(this, n))
    }
  }
  function oq(e, t) {
    var n, r
    function o() {
      var i = t.apply(this, arguments)
      return (i !== r && (n = (r = i) && rq(e, i)), n)
    }
    return ((o._value = t), o)
  }
  function iq(e, t) {
    var n, r
    function o() {
      var i = t.apply(this, arguments)
      return (i !== r && (n = (r = i) && nq(e, i)), n)
    }
    return ((o._value = t), o)
  }
  function aq(e, t) {
    var n = 'attr.' + e
    if (arguments.length < 2) return (n = this.tween(n)) && n._value
    if (t == null) return this.tween(n, null)
    if (typeof t != 'function') throw new Error()
    var r = $i(e)
    return this.tween(n, (r.local ? oq : iq)(r, t))
  }
  function sq(e, t) {
    return function () {
      rh(this, e).delay = +t.apply(this, arguments)
    }
  }
  function lq(e, t) {
    return (
      (t = +t),
      function () {
        rh(this, e).delay = t
      }
    )
  }
  function uq(e) {
    var t = this._id
    return arguments.length
      ? this.each((typeof e == 'function' ? sq : lq)(t, e))
      : pt(this.node(), t).delay
  }
  function cq(e, t) {
    return function () {
      Tt(this, e).duration = +t.apply(this, arguments)
    }
  }
  function dq(e, t) {
    return (
      (t = +t),
      function () {
        Tt(this, e).duration = t
      }
    )
  }
  function fq(e) {
    var t = this._id
    return arguments.length
      ? this.each((typeof e == 'function' ? cq : dq)(t, e))
      : pt(this.node(), t).duration
  }
  function hq(e, t) {
    if (typeof t != 'function') throw new Error()
    return function () {
      Tt(this, e).ease = t
    }
  }
  function pq(e) {
    var t = this._id
    return arguments.length ? this.each(hq(t, e)) : pt(this.node(), t).ease
  }
  function vq(e, t) {
    return function () {
      var n = t.apply(this, arguments)
      if (typeof n != 'function') throw new Error()
      Tt(this, e).ease = n
    }
  }
  function gq(e) {
    if (typeof e != 'function') throw new Error()
    return this.each(vq(this._id, e))
  }
  function mq(e) {
    typeof e != 'function' && (e = H1(e))
    for (var t = this._groups, n = t.length, r = new Array(n), o = 0; o < n; ++o)
      for (var i = t[o], a = i.length, s = (r[o] = []), l, u = 0; u < a; ++u)
        (l = i[u]) && e.call(l, l.__data__, u, i) && s.push(l)
    return new qt(r, this._parents, this._name, this._id)
  }
  function yq(e) {
    if (e._id !== this._id) throw new Error()
    for (
      var t = this._groups,
        n = e._groups,
        r = t.length,
        o = n.length,
        i = Math.min(r, o),
        a = new Array(r),
        s = 0;
      s < i;
      ++s
    )
      for (var l = t[s], u = n[s], c = l.length, d = (a[s] = new Array(c)), f, h = 0; h < c; ++h)
        (f = l[h] || u[h]) && (d[h] = f)
    for (; s < r; ++s) a[s] = t[s]
    return new qt(a, this._parents, this._name, this._id)
  }
  function bq(e) {
    return (e + '')
      .trim()
      .split(/^|\s+/)
      .every(function (t) {
        var n = t.indexOf('.')
        return (n >= 0 && (t = t.slice(0, n)), !t || t === 'start')
      })
  }
  function _q(e, t, n) {
    var r,
      o,
      i = bq(t) ? rh : Tt
    return function () {
      var a = i(this, e),
        s = a.on
      ;(s !== r && (o = (r = s).copy()).on(t, n), (a.on = o))
    }
  }
  function wq(e, t) {
    var n = this._id
    return arguments.length < 2 ? pt(this.node(), n).on.on(e) : this.each(_q(n, e, t))
  }
  function Sq(e) {
    return function () {
      var t = this.parentNode
      for (var n in this.__transition) if (+n !== e) return
      t && t.removeChild(this)
    }
  }
  function xq() {
    return this.on('end.remove', Sq(this._id))
  }
  function Cq(e) {
    var t = this._name,
      n = this._id
    typeof e != 'function' && (e = Jf(e))
    for (var r = this._groups, o = r.length, i = new Array(o), a = 0; a < o; ++a)
      for (var s = r[a], l = s.length, u = (i[a] = new Array(l)), c, d, f = 0; f < l; ++f)
        (c = s[f]) &&
          (d = e.call(c, c.__data__, f, s)) &&
          ('__data__' in c && (d.__data__ = c.__data__), (u[f] = d), Oi(u[f], t, n, f, u, pt(c, n)))
    return new qt(i, this._parents, t, n)
  }
  function Eq(e) {
    var t = this._name,
      n = this._id
    typeof e != 'function' && (e = k1(e))
    for (var r = this._groups, o = r.length, i = [], a = [], s = 0; s < o; ++s)
      for (var l = r[s], u = l.length, c, d = 0; d < u; ++d)
        if ((c = l[d])) {
          for (
            var f = e.call(c, c.__data__, d, l), h, g = pt(c, n), m = 0, v = f.length;
            m < v;
            ++m
          )
            (h = f[m]) && Oi(h, t, n, m, f, g)
          ;(i.push(f), a.push(c))
        }
    return new qt(i, a, t, n)
  }
  var $q = Xr.prototype.constructor
  function Tq() {
    return new $q(this._groups, this._parents)
  }
  function Oq(e, t) {
    var n, r, o
    return function () {
      var i = Vn(this, e),
        a = (this.style.removeProperty(e), Vn(this, e))
      return i === a ? null : i === n && a === r ? o : (o = t((n = i), (r = a)))
    }
  }
  function dS(e) {
    return function () {
      this.style.removeProperty(e)
    }
  }
  function Pq(e, t, n) {
    var r,
      o = n + '',
      i
    return function () {
      var a = Vn(this, e)
      return a === o ? null : a === r ? i : (i = t((r = a), n))
    }
  }
  function Iq(e, t, n) {
    var r, o, i
    return function () {
      var a = Vn(this, e),
        s = n(this),
        l = s + ''
      return (
        s == null && (l = s = (this.style.removeProperty(e), Vn(this, e))),
        a === l ? null : a === r && l === o ? i : ((o = l), (i = t((r = a), s)))
      )
    }
  }
  function Aq(e, t) {
    var n,
      r,
      o,
      i = 'style.' + t,
      a = 'end.' + i,
      s
    return function () {
      var l = Tt(this, e),
        u = l.on,
        c = l.value[i] == null ? s || (s = dS(t)) : void 0
      ;((u !== n || o !== c) && (r = (n = u).copy()).on(a, (o = c)), (l.on = r))
    }
  }
  function Nq(e, t, n) {
    var r = (e += '') == 'transform' ? RB : cS
    return t == null
      ? this.styleTween(e, Oq(e, r)).on('end.style.' + e, dS(e))
      : typeof t == 'function'
        ? this.styleTween(e, Iq(e, r, oh(this, 'style.' + e, t))).each(Aq(this._id, e))
        : this.styleTween(e, Pq(e, r, t), n).on('end.style.' + e, null)
  }
  function Rq(e, t, n) {
    return function (r) {
      this.style.setProperty(e, t.call(this, r), n)
    }
  }
  function Mq(e, t, n) {
    var r, o
    function i() {
      var a = t.apply(this, arguments)
      return (a !== o && (r = (o = a) && Rq(e, a, n)), r)
    }
    return ((i._value = t), i)
  }
  function Dq(e, t, n) {
    var r = 'style.' + (e += '')
    if (arguments.length < 2) return (r = this.tween(r)) && r._value
    if (t == null) return this.tween(r, null)
    if (typeof t != 'function') throw new Error()
    return this.tween(r, Mq(e, t, n ?? ''))
  }
  function Bq(e) {
    return function () {
      this.textContent = e
    }
  }
  function qq(e) {
    return function () {
      var t = e(this)
      this.textContent = t ?? ''
    }
  }
  function zq(e) {
    return this.tween(
      'text',
      typeof e == 'function' ? qq(oh(this, 'text', e)) : Bq(e == null ? '' : e + '')
    )
  }
  function Lq(e) {
    return function (t) {
      this.textContent = e.call(this, t)
    }
  }
  function Fq(e) {
    var t, n
    function r() {
      var o = e.apply(this, arguments)
      return (o !== n && (t = (n = o) && Lq(o)), t)
    }
    return ((r._value = e), r)
  }
  function kq(e) {
    var t = 'text'
    if (arguments.length < 1) return (t = this.tween(t)) && t._value
    if (e == null) return this.tween(t, null)
    if (typeof e != 'function') throw new Error()
    return this.tween(t, Fq(e))
  }
  function Hq() {
    for (
      var e = this._name, t = this._id, n = fS(), r = this._groups, o = r.length, i = 0;
      i < o;
      ++i
    )
      for (var a = r[i], s = a.length, l, u = 0; u < s; ++u)
        if ((l = a[u])) {
          var c = pt(l, t)
          Oi(l, e, n, u, a, {
            time: c.time + c.delay + c.duration,
            delay: 0,
            duration: c.duration,
            ease: c.ease,
          })
        }
    return new qt(r, this._parents, e, n)
  }
  function jq() {
    var e,
      t,
      n = this,
      r = n._id,
      o = n.size()
    return new Promise(function (i, a) {
      var s = { value: a },
        l = {
          value: function () {
            --o === 0 && i()
          },
        }
      ;(n.each(function () {
        var u = Tt(this, r),
          c = u.on
        ;(c !== e &&
          ((t = (e = c).copy()), t._.cancel.push(s), t._.interrupt.push(s), t._.end.push(l)),
          (u.on = t))
      }),
        o === 0 && i())
    })
  }
  var Vq = 0
  function qt(e, t, n, r) {
    ;((this._groups = e), (this._parents = t), (this._name = n), (this._id = r))
  }
  function fS() {
    return ++Vq
  }
  var Ot = Xr.prototype
  qt.prototype = {
    constructor: qt,
    select: Cq,
    selectAll: Eq,
    selectChild: Ot.selectChild,
    selectChildren: Ot.selectChildren,
    filter: mq,
    merge: yq,
    selection: Tq,
    transition: Hq,
    call: Ot.call,
    nodes: Ot.nodes,
    node: Ot.node,
    size: Ot.size,
    empty: Ot.empty,
    each: Ot.each,
    on: wq,
    attr: tq,
    attrTween: aq,
    style: Nq,
    styleTween: Dq,
    text: zq,
    textTween: kq,
    remove: xq,
    tween: YB,
    delay: uq,
    duration: fq,
    ease: pq,
    easeVarying: gq,
    end: jq,
    [Symbol.iterator]: Ot[Symbol.iterator],
  }
  function Gq(e) {
    return ((e *= 2) <= 1 ? e * e * e : (e -= 2) * e * e + 2) / 2
  }
  var Wq = { time: null, delay: 0, duration: 250, ease: Gq }
  function Uq(e, t) {
    for (var n; !(n = e.__transition) || !(n = n[t]); )
      if (!(e = e.parentNode)) throw new Error(`transition ${t} not found`)
    return n
  }
  function Yq(e) {
    var t, n
    e instanceof qt
      ? ((t = e._id), (e = e._name))
      : ((t = fS()), ((n = Wq).time = nh()), (e = e == null ? null : e + ''))
    for (var r = this._groups, o = r.length, i = 0; i < o; ++i)
      for (var a = r[i], s = a.length, l, u = 0; u < s; ++u)
        (l = a[u]) && Oi(l, e, t, u, a, n || Uq(l, t))
    return new qt(r, this._parents, e, t)
  }
  Xr.prototype.interrupt = GB
  Xr.prototype.transition = Yq
  const po = (e) => () => e
  function Xq(e, { sourceEvent: t, target: n, transform: r, dispatch: o }) {
    Object.defineProperties(this, {
      type: { value: e, enumerable: !0, configurable: !0 },
      sourceEvent: { value: t, enumerable: !0, configurable: !0 },
      target: { value: n, enumerable: !0, configurable: !0 },
      transform: { value: r, enumerable: !0, configurable: !0 },
      _: { value: o },
    })
  }
  function Nt(e, t, n) {
    ;((this.k = e), (this.x = t), (this.y = n))
  }
  Nt.prototype = {
    constructor: Nt,
    scale: function (e) {
      return e === 1 ? this : new Nt(this.k * e, this.x, this.y)
    },
    translate: function (e, t) {
      return (e === 0) & (t === 0) ? this : new Nt(this.k, this.x + this.k * e, this.y + this.k * t)
    },
    apply: function (e) {
      return [e[0] * this.k + this.x, e[1] * this.k + this.y]
    },
    applyX: function (e) {
      return e * this.k + this.x
    },
    applyY: function (e) {
      return e * this.k + this.y
    },
    invert: function (e) {
      return [(e[0] - this.x) / this.k, (e[1] - this.y) / this.k]
    },
    invertX: function (e) {
      return (e - this.x) / this.k
    },
    invertY: function (e) {
      return (e - this.y) / this.k
    },
    rescaleX: function (e) {
      return e.copy().domain(e.range().map(this.invertX, this).map(e.invert, e))
    },
    rescaleY: function (e) {
      return e.copy().domain(e.range().map(this.invertY, this).map(e.invert, e))
    },
    toString: function () {
      return 'translate(' + this.x + ',' + this.y + ') scale(' + this.k + ')'
    },
  }
  var Wn = new Nt(1, 0, 0)
  Nt.prototype
  function md(e) {
    e.stopImmediatePropagation()
  }
  function sr(e) {
    ;(e.preventDefault(), e.stopImmediatePropagation())
  }
  function Kq(e) {
    return (!e.ctrlKey || e.type === 'wheel') && !e.button
  }
  function Zq() {
    var e = this
    return e instanceof SVGElement
      ? ((e = e.ownerSVGElement || e),
        e.hasAttribute('viewBox')
          ? ((e = e.viewBox.baseVal),
            [
              [e.x, e.y],
              [e.x + e.width, e.y + e.height],
            ])
          : [
              [0, 0],
              [e.width.baseVal.value, e.height.baseVal.value],
            ])
      : [
          [0, 0],
          [e.clientWidth, e.clientHeight],
        ]
  }
  function R0() {
    return this.__zoom || Wn
  }
  function Jq(e) {
    return -e.deltaY * (e.deltaMode === 1 ? 0.05 : e.deltaMode ? 1 : 0.002) * (e.ctrlKey ? 10 : 1)
  }
  function Qq() {
    return navigator.maxTouchPoints || 'ontouchstart' in this
  }
  function ez(e, t, n) {
    var r = e.invertX(t[0][0]) - n[0][0],
      o = e.invertX(t[1][0]) - n[1][0],
      i = e.invertY(t[0][1]) - n[0][1],
      a = e.invertY(t[1][1]) - n[1][1]
    return e.translate(
      o > r ? (r + o) / 2 : Math.min(0, r) || Math.max(0, o),
      a > i ? (i + a) / 2 : Math.min(0, i) || Math.max(0, a)
    )
  }
  function tz() {
    var e = Kq,
      t = Zq,
      n = ez,
      r = Jq,
      o = Qq,
      i = [0, 1 / 0],
      a = [
        [-1 / 0, -1 / 0],
        [1 / 0, 1 / 0],
      ],
      s = 250,
      l = xo,
      u = Ei('start', 'zoom', 'end'),
      c,
      d,
      f,
      h = 500,
      g = 150,
      m = 0,
      v = 10
    function b(C) {
      C.property('__zoom', R0)
        .on('wheel.zoom', T, { passive: !1 })
        .on('mousedown.zoom', A)
        .on('dblclick.zoom', $)
        .filter(o)
        .on('touchstart.zoom', P)
        .on('touchmove.zoom', E)
        .on('touchend.zoom touchcancel.zoom', z)
        .style('-webkit-tap-highlight-color', 'rgba(0,0,0,0)')
    }
    ;((b.transform = function (C, R, N, j) {
      var V = C.selection ? C.selection() : C
      ;(V.property('__zoom', R0),
        C !== V
          ? x(C, R, N, j)
          : V.interrupt().each(function () {
              S(this, arguments)
                .event(j)
                .start()
                .zoom(null, typeof R == 'function' ? R.apply(this, arguments) : R)
                .end()
            }))
    }),
      (b.scaleBy = function (C, R, N, j) {
        b.scaleTo(
          C,
          function () {
            var V = this.__zoom.k,
              H = typeof R == 'function' ? R.apply(this, arguments) : R
            return V * H
          },
          N,
          j
        )
      }),
      (b.scaleTo = function (C, R, N, j) {
        b.transform(
          C,
          function () {
            var V = t.apply(this, arguments),
              H = this.__zoom,
              G = N == null ? _(V) : typeof N == 'function' ? N.apply(this, arguments) : N,
              Y = H.invert(G),
              Z = typeof R == 'function' ? R.apply(this, arguments) : R
            return n(p(y(H, Z), G, Y), V, a)
          },
          N,
          j
        )
      }),
      (b.translateBy = function (C, R, N, j) {
        b.transform(
          C,
          function () {
            return n(
              this.__zoom.translate(
                typeof R == 'function' ? R.apply(this, arguments) : R,
                typeof N == 'function' ? N.apply(this, arguments) : N
              ),
              t.apply(this, arguments),
              a
            )
          },
          null,
          j
        )
      }),
      (b.translateTo = function (C, R, N, j, V) {
        b.transform(
          C,
          function () {
            var H = t.apply(this, arguments),
              G = this.__zoom,
              Y = j == null ? _(H) : typeof j == 'function' ? j.apply(this, arguments) : j
            return n(
              Wn.translate(Y[0], Y[1])
                .scale(G.k)
                .translate(
                  typeof R == 'function' ? -R.apply(this, arguments) : -R,
                  typeof N == 'function' ? -N.apply(this, arguments) : -N
                ),
              H,
              a
            )
          },
          j,
          V
        )
      }))
    function y(C, R) {
      return ((R = Math.max(i[0], Math.min(i[1], R))), R === C.k ? C : new Nt(R, C.x, C.y))
    }
    function p(C, R, N) {
      var j = R[0] - N[0] * C.k,
        V = R[1] - N[1] * C.k
      return j === C.x && V === C.y ? C : new Nt(C.k, j, V)
    }
    function _(C) {
      return [(+C[0][0] + +C[1][0]) / 2, (+C[0][1] + +C[1][1]) / 2]
    }
    function x(C, R, N, j) {
      C.on('start.zoom', function () {
        S(this, arguments).event(j).start()
      })
        .on('interrupt.zoom end.zoom', function () {
          S(this, arguments).event(j).end()
        })
        .tween('zoom', function () {
          var V = this,
            H = arguments,
            G = S(V, H).event(j),
            Y = t.apply(V, H),
            Z = N == null ? _(Y) : typeof N == 'function' ? N.apply(V, H) : N,
            ne = Math.max(Y[1][0] - Y[0][0], Y[1][1] - Y[0][1]),
            B = V.__zoom,
            L = typeof R == 'function' ? R.apply(V, H) : R,
            k = l(B.invert(Z).concat(ne / B.k), L.invert(Z).concat(ne / L.k))
          return function (U) {
            if (U === 1) U = L
            else {
              var J = k(U),
                re = ne / J[2]
              U = new Nt(re, Z[0] - J[0] * re, Z[1] - J[1] * re)
            }
            G.zoom(null, U)
          }
        })
    }
    function S(C, R, N) {
      return (!N && C.__zooming) || new w(C, R)
    }
    function w(C, R) {
      ;((this.that = C),
        (this.args = R),
        (this.active = 0),
        (this.sourceEvent = null),
        (this.extent = t.apply(C, R)),
        (this.taps = 0))
    }
    w.prototype = {
      event: function (C) {
        return (C && (this.sourceEvent = C), this)
      },
      start: function () {
        return (++this.active === 1 && ((this.that.__zooming = this), this.emit('start')), this)
      },
      zoom: function (C, R) {
        return (
          this.mouse && C !== 'mouse' && (this.mouse[1] = R.invert(this.mouse[0])),
          this.touch0 && C !== 'touch' && (this.touch0[1] = R.invert(this.touch0[0])),
          this.touch1 && C !== 'touch' && (this.touch1[1] = R.invert(this.touch1[0])),
          (this.that.__zoom = R),
          this.emit('zoom'),
          this
        )
      },
      end: function () {
        return (--this.active === 0 && (delete this.that.__zooming, this.emit('end')), this)
      },
      emit: function (C) {
        var R = lt(this.that).datum()
        u.call(
          C,
          this.that,
          new Xq(C, {
            sourceEvent: this.sourceEvent,
            target: b,
            transform: this.that.__zoom,
            dispatch: u,
          }),
          R
        )
      },
    }
    function T(C, ...R) {
      if (!e.apply(this, arguments)) return
      var N = S(this, R).event(C),
        j = this.__zoom,
        V = Math.max(i[0], Math.min(i[1], j.k * Math.pow(2, r.apply(this, arguments)))),
        H = vt(C)
      if (N.wheel)
        ((N.mouse[0][0] !== H[0] || N.mouse[0][1] !== H[1]) &&
          (N.mouse[1] = j.invert((N.mouse[0] = H))),
          clearTimeout(N.wheel))
      else {
        if (j.k === V) return
        ;((N.mouse = [H, j.invert(H)]), $o(this), N.start())
      }
      ;(sr(C),
        (N.wheel = setTimeout(G, g)),
        N.zoom('mouse', n(p(y(j, V), N.mouse[0], N.mouse[1]), N.extent, a)))
      function G() {
        ;((N.wheel = null), N.end())
      }
    }
    function A(C, ...R) {
      if (f || !e.apply(this, arguments)) return
      var N = C.currentTarget,
        j = S(this, R, !0).event(C),
        V = lt(C.view).on('mousemove.zoom', Z, !0).on('mouseup.zoom', ne, !0),
        H = vt(C, N),
        G = C.clientX,
        Y = C.clientY
      ;(J1(C.view), md(C), (j.mouse = [H, this.__zoom.invert(H)]), $o(this), j.start())
      function Z(B) {
        if ((sr(B), !j.moved)) {
          var L = B.clientX - G,
            k = B.clientY - Y
          j.moved = L * L + k * k > m
        }
        j.event(B).zoom(
          'mouse',
          n(p(j.that.__zoom, (j.mouse[0] = vt(B, N)), j.mouse[1]), j.extent, a)
        )
      }
      function ne(B) {
        ;(V.on('mousemove.zoom mouseup.zoom', null), Q1(B.view, j.moved), sr(B), j.event(B).end())
      }
    }
    function $(C, ...R) {
      if (e.apply(this, arguments)) {
        var N = this.__zoom,
          j = vt(C.changedTouches ? C.changedTouches[0] : C, this),
          V = N.invert(j),
          H = N.k * (C.shiftKey ? 0.5 : 2),
          G = n(p(y(N, H), j, V), t.apply(this, R), a)
        ;(sr(C),
          s > 0
            ? lt(this).transition().duration(s).call(x, G, j, C)
            : lt(this).call(b.transform, G, j, C))
      }
    }
    function P(C, ...R) {
      if (e.apply(this, arguments)) {
        var N = C.touches,
          j = N.length,
          V = S(this, R, C.changedTouches.length === j).event(C),
          H,
          G,
          Y,
          Z
        for (md(C), G = 0; G < j; ++G)
          ((Y = N[G]),
            (Z = vt(Y, this)),
            (Z = [Z, this.__zoom.invert(Z), Y.identifier]),
            V.touch0
              ? !V.touch1 && V.touch0[2] !== Z[2] && ((V.touch1 = Z), (V.taps = 0))
              : ((V.touch0 = Z), (H = !0), (V.taps = 1 + !!c)))
        ;(c && (c = clearTimeout(c)),
          H &&
            (V.taps < 2 &&
              ((d = Z[0]),
              (c = setTimeout(function () {
                c = null
              }, h))),
            $o(this),
            V.start()))
      }
    }
    function E(C, ...R) {
      if (this.__zooming) {
        var N = S(this, R).event(C),
          j = C.changedTouches,
          V = j.length,
          H,
          G,
          Y,
          Z
        for (sr(C), H = 0; H < V; ++H)
          ((G = j[H]),
            (Y = vt(G, this)),
            N.touch0 && N.touch0[2] === G.identifier
              ? (N.touch0[0] = Y)
              : N.touch1 && N.touch1[2] === G.identifier && (N.touch1[0] = Y))
        if (((G = N.that.__zoom), N.touch1)) {
          var ne = N.touch0[0],
            B = N.touch0[1],
            L = N.touch1[0],
            k = N.touch1[1],
            U = (U = L[0] - ne[0]) * U + (U = L[1] - ne[1]) * U,
            J = (J = k[0] - B[0]) * J + (J = k[1] - B[1]) * J
          ;((G = y(G, Math.sqrt(U / J))),
            (Y = [(ne[0] + L[0]) / 2, (ne[1] + L[1]) / 2]),
            (Z = [(B[0] + k[0]) / 2, (B[1] + k[1]) / 2]))
        } else if (N.touch0) ((Y = N.touch0[0]), (Z = N.touch0[1]))
        else return
        N.zoom('touch', n(p(G, Y, Z), N.extent, a))
      }
    }
    function z(C, ...R) {
      if (this.__zooming) {
        var N = S(this, R).event(C),
          j = C.changedTouches,
          V = j.length,
          H,
          G
        for (
          md(C),
            f && clearTimeout(f),
            f = setTimeout(function () {
              f = null
            }, h),
            H = 0;
          H < V;
          ++H
        )
          ((G = j[H]),
            N.touch0 && N.touch0[2] === G.identifier
              ? delete N.touch0
              : N.touch1 && N.touch1[2] === G.identifier && delete N.touch1)
        if ((N.touch1 && !N.touch0 && ((N.touch0 = N.touch1), delete N.touch1), N.touch0))
          N.touch0[1] = this.__zoom.invert(N.touch0[0])
        else if (
          (N.end(), N.taps === 2 && ((G = vt(G, this)), Math.hypot(d[0] - G[0], d[1] - G[1]) < v))
        ) {
          var Y = lt(this).on('dblclick.zoom')
          Y && Y.apply(this, arguments)
        }
      }
    }
    return (
      (b.wheelDelta = function (C) {
        return arguments.length ? ((r = typeof C == 'function' ? C : po(+C)), b) : r
      }),
      (b.filter = function (C) {
        return arguments.length ? ((e = typeof C == 'function' ? C : po(!!C)), b) : e
      }),
      (b.touchable = function (C) {
        return arguments.length ? ((o = typeof C == 'function' ? C : po(!!C)), b) : o
      }),
      (b.extent = function (C) {
        return arguments.length
          ? ((t =
              typeof C == 'function'
                ? C
                : po([
                    [+C[0][0], +C[0][1]],
                    [+C[1][0], +C[1][1]],
                  ])),
            b)
          : t
      }),
      (b.scaleExtent = function (C) {
        return arguments.length ? ((i[0] = +C[0]), (i[1] = +C[1]), b) : [i[0], i[1]]
      }),
      (b.translateExtent = function (C) {
        return arguments.length
          ? ((a[0][0] = +C[0][0]),
            (a[1][0] = +C[1][0]),
            (a[0][1] = +C[0][1]),
            (a[1][1] = +C[1][1]),
            b)
          : [
              [a[0][0], a[0][1]],
              [a[1][0], a[1][1]],
            ]
      }),
      (b.constrain = function (C) {
        return arguments.length ? ((n = C), b) : n
      }),
      (b.duration = function (C) {
        return arguments.length ? ((s = +C), b) : s
      }),
      (b.interpolate = function (C) {
        return arguments.length ? ((l = C), b) : l
      }),
      (b.on = function () {
        var C = u.on.apply(u, arguments)
        return C === u ? b : C
      }),
      (b.clickDistance = function (C) {
        return arguments.length ? ((m = (C = +C) * C), b) : Math.sqrt(m)
      }),
      (b.tapDistance = function (C) {
        return arguments.length ? ((v = +C), b) : v
      }),
      b
    )
  }
  var pe = ((e) => (
      (e.Left = 'left'),
      (e.Top = 'top'),
      (e.Right = 'right'),
      (e.Bottom = 'bottom'),
      e
    ))(pe || {}),
    ih = ((e) => ((e.Partial = 'partial'), (e.Full = 'full'), e))(ih || {}),
    cn = ((e) => (
      (e.Bezier = 'default'),
      (e.SimpleBezier = 'simple-bezier'),
      (e.Straight = 'straight'),
      (e.Step = 'step'),
      (e.SmoothStep = 'smoothstep'),
      e
    ))(cn || {}),
    Zt = ((e) => ((e.Strict = 'strict'), (e.Loose = 'loose'), e))(Zt || {}),
    Wo = ((e) => ((e.Arrow = 'arrow'), (e.ArrowClosed = 'arrowclosed'), e))(Wo || {}),
    Sr = ((e) => ((e.Free = 'free'), (e.Vertical = 'vertical'), (e.Horizontal = 'horizontal'), e))(
      Sr || {}
    )
  const nz = ['INPUT', 'SELECT', 'TEXTAREA'],
    rz = typeof document < 'u' ? document : null
  function Zd(e) {
    var t, n
    const r =
        ((n = (t = e.composedPath) == null ? void 0 : t.call(e)) == null ? void 0 : n[0]) ||
        e.target,
      o = typeof r?.hasAttribute == 'function' ? r.hasAttribute('contenteditable') : !1,
      i = typeof r?.closest == 'function' ? r.closest('.nokey') : null
    return nz.includes(r?.nodeName) || o || !!i
  }
  function oz(e) {
    return e.ctrlKey || e.metaKey || e.shiftKey || e.altKey
  }
  function M0(e, t, n, r) {
    const o = t
      .replace(
        '+',
        `
`
      )
      .replace(
        `

`,
        `
+`
      )
      .split(
        `
`
      )
      .map((a) => a.trim().toLowerCase())
    if (o.length === 1) return e.toLowerCase() === t.toLowerCase()
    r || n.add(e.toLowerCase())
    const i = o.every((a, s) => n.has(a) && Array.from(n.values())[s] === o[s])
    return (r && n.delete(e.toLowerCase()), i)
  }
  function iz(e, t) {
    return (n) => {
      if (!n.code && !n.key) return !1
      const r = az(n.code, e)
      return Array.isArray(e)
        ? e.some((o) => M0(n[r], o, t, n.type === 'keyup'))
        : M0(n[r], e, t, n.type === 'keyup')
    }
  }
  function az(e, t) {
    return t.includes(e) ? 'code' : 'key'
  }
  function xr(e, t) {
    const n = X(() => Ee(t?.target) ?? rz),
      r = ce(Ee(e) === !0)
    let o = !1
    const i = new Set()
    let a = l(Ee(e))
    ;(me(
      () => Ee(e),
      (u, c) => {
        ;(typeof c == 'boolean' && typeof u != 'boolean' && s(), (a = l(u)))
      },
      { immediate: !0 }
    ),
      L1(['blur', 'contextmenu'], s),
      g0(
        (...u) => a(...u),
        (u) => {
          var c, d
          const f = Ee(t?.actInsideInputWithModifier) ?? !0,
            h = Ee(t?.preventDefault) ?? !1
          if (((o = oz(u)), (!o || (o && !f)) && Zd(u))) return
          const m =
              ((d = (c = u.composedPath) == null ? void 0 : c.call(u)) == null ? void 0 : d[0]) ||
              u.target,
            v = m?.nodeName === 'BUTTON' || m?.nodeName === 'A'
          ;(!h && (o || !v) && u.preventDefault(), (r.value = !0))
        },
        { eventName: 'keydown', target: n }
      ),
      g0(
        (...u) => a(...u),
        (u) => {
          const c = Ee(t?.actInsideInputWithModifier) ?? !0
          if (r.value) {
            if ((!o || (o && !c)) && Zd(u)) return
            ;((o = !1), (r.value = !1))
          }
        },
        { eventName: 'keyup', target: n }
      ))
    function s() {
      ;((o = !1), i.clear(), (r.value = Ee(e) === !0))
    }
    function l(u) {
      return u === null
        ? (s(), () => !1)
        : typeof u == 'boolean'
          ? (s(), (r.value = u), () => !1)
          : Array.isArray(u) || typeof u == 'string'
            ? iz(u, i)
            : u
    }
    return r
  }
  const hS = 'vue-flow__node-desc',
    pS = 'vue-flow__edge-desc',
    sz = 'vue-flow__aria-live',
    vS = ['Enter', ' ', 'Escape'],
    zn = {
      ArrowUp: { x: 0, y: -1 },
      ArrowDown: { x: 0, y: 1 },
      ArrowLeft: { x: -1, y: 0 },
      ArrowRight: { x: 1, y: 0 },
    }
  function Uo(e) {
    return {
      ...(e.computedPosition || { x: 0, y: 0 }),
      width: e.dimensions.width || 0,
      height: e.dimensions.height || 0,
    }
  }
  function Yo(e, t) {
    const n = Math.max(0, Math.min(e.x + e.width, t.x + t.width) - Math.max(e.x, t.x)),
      r = Math.max(0, Math.min(e.y + e.height, t.y + t.height) - Math.max(e.y, t.y))
    return Math.ceil(n * r)
  }
  function Pi(e) {
    return { width: e.offsetWidth, height: e.offsetHeight }
  }
  function Sn(e, t = 0, n = 1) {
    return Math.min(Math.max(e, t), n)
  }
  function gS(e, t) {
    return { x: Sn(e.x, t[0][0], t[1][0]), y: Sn(e.y, t[0][1], t[1][1]) }
  }
  function D0(e) {
    const t = e.getRootNode()
    return 'elementFromPoint' in t ? t : window.document
  }
  function Jt(e) {
    return e && typeof e == 'object' && 'id' in e && 'source' in e && 'target' in e
  }
  function mn(e) {
    return e && typeof e == 'object' && 'id' in e && 'position' in e && !Jt(e)
  }
  function pr(e) {
    return mn(e) && 'computedPosition' in e
  }
  function vo(e) {
    return !Number.isNaN(e) && Number.isFinite(e)
  }
  function lz(e) {
    return vo(e.width) && vo(e.height) && vo(e.x) && vo(e.y)
  }
  function uz(e, t, n) {
    const r = {
      id: e.id.toString(),
      type: e.type ?? 'default',
      dimensions: bo({ width: 0, height: 0 }),
      computedPosition: bo({ z: 0, ...e.position }),
      handleBounds: { source: [], target: [] },
      draggable: void 0,
      selectable: void 0,
      connectable: void 0,
      focusable: void 0,
      selected: !1,
      dragging: !1,
      resizing: !1,
      initialized: !1,
      isParent: !1,
      position: { x: 0, y: 0 },
      data: De(e.data) ? e.data : {},
      events: bo(De(e.events) ? e.events : {}),
    }
    return Object.assign(t ?? r, e, { id: e.id.toString(), parentNode: n })
  }
  function mS(e, t, n) {
    var r, o
    const i = {
      id: e.id.toString(),
      type: e.type ?? t?.type ?? 'default',
      source: e.source.toString(),
      target: e.target.toString(),
      sourceHandle: (r = e.sourceHandle) == null ? void 0 : r.toString(),
      targetHandle: (o = e.targetHandle) == null ? void 0 : o.toString(),
      updatable: e.updatable ?? n?.updatable,
      selectable: e.selectable ?? n?.selectable,
      focusable: e.focusable ?? n?.focusable,
      data: De(e.data) ? e.data : {},
      events: bo(De(e.events) ? e.events : {}),
      label: e.label ?? '',
      interactionWidth: e.interactionWidth ?? n?.interactionWidth,
      ...(n ?? {}),
    }
    return Object.assign(t ?? i, e, { id: e.id.toString() })
  }
  function yS(e, t, n, r) {
    const o = typeof e == 'string' ? e : e.id,
      i = new Set(),
      a = r === 'source' ? 'target' : 'source'
    for (const s of n) s[a] === o && i.add(s[r])
    return t.filter((s) => i.has(s.id))
  }
  function cz(...e) {
    if (e.length === 3) {
      const [i, a, s] = e
      return yS(i, a, s, 'target')
    }
    const [t, n] = e,
      r = typeof t == 'string' ? t : t.id
    return n
      .filter((i) => Jt(i) && i.source === r)
      .map((i) => n.find((a) => mn(a) && a.id === i.target))
  }
  function dz(...e) {
    if (e.length === 3) {
      const [i, a, s] = e
      return yS(i, a, s, 'source')
    }
    const [t, n] = e,
      r = typeof t == 'string' ? t : t.id
    return n
      .filter((i) => Jt(i) && i.target === r)
      .map((i) => n.find((a) => mn(a) && a.id === i.source))
  }
  function bS({ source: e, sourceHandle: t, target: n, targetHandle: r }) {
    return `vueflow__edge-${e}${t ?? ''}-${n}${r ?? ''}`
  }
  function fz(e, t) {
    return t.some(
      (n) =>
        Jt(n) &&
        n.source === e.source &&
        n.target === e.target &&
        (n.sourceHandle === e.sourceHandle || (!n.sourceHandle && !e.sourceHandle)) &&
        (n.targetHandle === e.targetHandle || (!n.targetHandle && !e.targetHandle))
    )
  }
  function Br({ x: e, y: t }, { x: n, y: r, zoom: o }) {
    return { x: e * o + n, y: t * o + r }
  }
  function qr({ x: e, y: t }, { x: n, y: r, zoom: o }, i = !1, a = [1, 1]) {
    const s = { x: (e - n) / o, y: (t - r) / o }
    return i ? Ii(s, a) : s
  }
  function hz(e, t) {
    return {
      x: Math.min(e.x, t.x),
      y: Math.min(e.y, t.y),
      x2: Math.max(e.x2, t.x2),
      y2: Math.max(e.y2, t.y2),
    }
  }
  function _S({ x: e, y: t, width: n, height: r }) {
    return { x: e, y: t, x2: e + n, y2: t + r }
  }
  function pz({ x: e, y: t, x2: n, y2: r }) {
    return { x: e, y: t, width: n - e, height: r - t }
  }
  function wS(e) {
    let t = {
      x: Number.POSITIVE_INFINITY,
      y: Number.POSITIVE_INFINITY,
      x2: Number.NEGATIVE_INFINITY,
      y2: Number.NEGATIVE_INFINITY,
    }
    for (let n = 0; n < e.length; n++) {
      const r = e[n]
      t = hz(t, _S({ ...r.computedPosition, ...r.dimensions }))
    }
    return pz(t)
  }
  function SS(e, t, n = { x: 0, y: 0, zoom: 1 }, r = !1, o = !1) {
    const i = { ...qr(t, n), width: t.width / n.zoom, height: t.height / n.zoom },
      a = []
    for (const s of e) {
      const { dimensions: l, selectable: u = !0, hidden: c = !1 } = s,
        d = l.width ?? s.width ?? null,
        f = l.height ?? s.height ?? null
      if ((o && !u) || c) continue
      const h = Yo(i, Uo(s)),
        g = d === null || f === null,
        m = r && h > 0,
        v = (d ?? 0) * (f ?? 0)
      ;(g || m || h >= v || s.dragging) && a.push(s)
    }
    return a
  }
  function xS(e, t) {
    const n = new Set()
    if (typeof e == 'string') n.add(e)
    else if (e.length >= 1) for (const r of e) n.add(r.id)
    return t.filter((r) => n.has(r.source) || n.has(r.target))
  }
  function Nn(e, t) {
    if (typeof e == 'number') return Math.floor((t - t / (1 + e)) * 0.5)
    if (typeof e == 'string' && e.endsWith('px')) {
      const n = Number.parseFloat(e)
      if (!Number.isNaN(n)) return Math.floor(n)
    }
    if (typeof e == 'string' && e.endsWith('%')) {
      const n = Number.parseFloat(e)
      if (!Number.isNaN(n)) return Math.floor(t * n * 0.01)
    }
    return (
      Zr(
        `The padding value "${e}" is invalid. Please provide a number or a string with a valid unit (px or %).`
      ),
      0
    )
  }
  function vz(e, t, n) {
    if (typeof e == 'string' || typeof e == 'number') {
      const r = Nn(e, n),
        o = Nn(e, t)
      return { top: r, right: o, bottom: r, left: o, x: o * 2, y: r * 2 }
    }
    if (typeof e == 'object') {
      const r = Nn(e.top ?? e.y ?? 0, n),
        o = Nn(e.bottom ?? e.y ?? 0, n),
        i = Nn(e.left ?? e.x ?? 0, t),
        a = Nn(e.right ?? e.x ?? 0, t)
      return { top: r, right: a, bottom: o, left: i, x: i + a, y: r + o }
    }
    return { top: 0, right: 0, bottom: 0, left: 0, x: 0, y: 0 }
  }
  function gz(e, t, n, r, o, i) {
    const { x: a, y: s } = Br(e, { x: t, y: n, zoom: r }),
      { x: l, y: u } = Br({ x: e.x + e.width, y: e.y + e.height }, { x: t, y: n, zoom: r }),
      c = o - l,
      d = i - u
    return { left: Math.floor(a), top: Math.floor(s), right: Math.floor(c), bottom: Math.floor(d) }
  }
  function B0(e, t, n, r, o, i = 0.1) {
    const a = vz(i, t, n),
      s = (t - a.x) / e.width,
      l = (n - a.y) / e.height,
      u = Math.min(s, l),
      c = Sn(u, r, o),
      d = e.x + e.width / 2,
      f = e.y + e.height / 2,
      h = t / 2 - d * c,
      g = n / 2 - f * c,
      m = gz(e, h, g, c, t, n),
      v = {
        left: Math.min(m.left - a.left, 0),
        top: Math.min(m.top - a.top, 0),
        right: Math.min(m.right - a.right, 0),
        bottom: Math.min(m.bottom - a.bottom, 0),
      }
    return { x: h - v.left + v.right, y: g - v.top + v.bottom, zoom: c }
  }
  function mz(e, t) {
    return { x: t.x + e.x, y: t.y + e.y, z: (e.z > t.z ? e.z : t.z) + 1 }
  }
  function CS(e, t) {
    if (!e.parentNode) return !1
    const n = t.get(e.parentNode)
    return n ? (n.selected ? !0 : CS(n, t)) : !1
  }
  function zr(e, t) {
    return typeof e > 'u'
      ? ''
      : typeof e == 'string'
        ? e
        : `${t ? `${t}__` : ''}${Object.keys(e)
            .sort()
            .map((r) => `${r}=${e[r]}`)
            .join('&')}`
  }
  function q0(e) {
    const t = e.ctrlKey && Xo() ? 10 : 1
    return -e.deltaY * (e.deltaMode === 1 ? 0.05 : e.deltaMode ? 1 : 0.002) * t
  }
  function z0(e, t, n) {
    return e < t ? Sn(Math.abs(e - t), 1, t) / t : e > n ? -Sn(Math.abs(e - n), 1, t) / t : 0
  }
  function ES(e, t, n = 15, r = 40) {
    const o = z0(e.x, r, t.width - r) * n,
      i = z0(e.y, r, t.height - r) * n
    return [o, i]
  }
  function yd(e, t) {
    if (t) {
      const n = e.position.x + e.dimensions.width - t.dimensions.width,
        r = e.position.y + e.dimensions.height - t.dimensions.height
      if (n > 0 || r > 0 || e.position.x < 0 || e.position.y < 0) {
        let o = {}
        if (
          (typeof t.style == 'function' ? (o = { ...t.style(t) }) : t.style && (o = { ...t.style }),
          (o.width = o.width ?? `${t.dimensions.width}px`),
          (o.height = o.height ?? `${t.dimensions.height}px`),
          n > 0)
        )
          if (typeof o.width == 'string') {
            const i = Number(o.width.replace('px', ''))
            o.width = `${i + n}px`
          } else o.width += n
        if (r > 0)
          if (typeof o.height == 'string') {
            const i = Number(o.height.replace('px', ''))
            o.height = `${i + r}px`
          } else o.height += r
        if (e.position.x < 0) {
          const i = Math.abs(e.position.x)
          if (((t.position.x = t.position.x - i), typeof o.width == 'string')) {
            const a = Number(o.width.replace('px', ''))
            o.width = `${a + i}px`
          } else o.width += i
          e.position.x = 0
        }
        if (e.position.y < 0) {
          const i = Math.abs(e.position.y)
          if (((t.position.y = t.position.y - i), typeof o.height == 'string')) {
            const a = Number(o.height.replace('px', ''))
            o.height = `${a + i}px`
          } else o.height += i
          e.position.y = 0
        }
        ;((t.dimensions.width = Number(o.width.toString().replace('px', ''))),
          (t.dimensions.height = Number(o.height.toString().replace('px', ''))),
          typeof t.style == 'function'
            ? (t.style = (i) => {
                const a = t.style
                return { ...a(i), ...o }
              })
            : (t.style = { ...t.style, ...o }))
      }
    }
  }
  function L0(e, t) {
    var n, r
    const o = e.filter((a) => a.type === 'add' || a.type === 'remove')
    for (const a of o)
      if (a.type === 'add') t.findIndex((l) => l.id === a.item.id) === -1 && t.push(a.item)
      else if (a.type === 'remove') {
        const s = t.findIndex((l) => l.id === a.id)
        s !== -1 && t.splice(s, 1)
      }
    const i = t.map((a) => a.id)
    for (const a of t)
      for (const s of e)
        if (s.id === a.id)
          switch (s.type) {
            case 'select':
              a.selected = s.selected
              break
            case 'position':
              if (
                pr(a) &&
                (typeof s.position < 'u' && (a.position = s.position),
                typeof s.dragging < 'u' && (a.dragging = s.dragging),
                a.expandParent && a.parentNode)
              ) {
                const l = t[i.indexOf(a.parentNode)]
                l && pr(l) && yd(a, l)
              }
              break
            case 'dimensions':
              if (
                pr(a) &&
                (typeof s.dimensions < 'u' && (a.dimensions = s.dimensions),
                typeof s.updateStyle < 'u' &&
                  s.updateStyle &&
                  (a.style = {
                    ...(a.style || {}),
                    width: `${(n = s.dimensions) == null ? void 0 : n.width}px`,
                    height: `${(r = s.dimensions) == null ? void 0 : r.height}px`,
                  }),
                typeof s.resizing < 'u' && (a.resizing = s.resizing),
                a.expandParent && a.parentNode)
              ) {
                const l = t[i.indexOf(a.parentNode)]
                l &&
                  pr(l) &&
                  (!!l.dimensions.width && !!l.dimensions.height
                    ? yd(a, l)
                    : Ne(() => {
                        yd(a, l)
                      }))
              }
              break
          }
    return t
  }
  function Ut(e, t) {
    return { id: e, type: 'select', selected: t }
  }
  function F0(e) {
    return { item: e, type: 'add' }
  }
  function k0(e) {
    return { id: e, type: 'remove' }
  }
  function H0(e, t, n, r, o) {
    return {
      id: e,
      source: t,
      target: n,
      sourceHandle: r || null,
      targetHandle: o || null,
      type: 'remove',
    }
  }
  function Yt(e, t = new Set(), n = !1) {
    const r = []
    for (const [o, i] of e) {
      const a = t.has(o)
      !(i.selected === void 0 && !a) &&
        i.selected !== a &&
        (n && (i.selected = a), r.push(Ut(i.id, a)))
    }
    return r
  }
  const j0 = () => {}
  function se(e) {
    const t = new Set()
    let n = j0,
      r = () => !1
    const o = () => t.size > 0 || r(),
      i = (f) => {
        n = f
      },
      a = () => {
        n = j0
      },
      s = (f) => {
        r = f
      },
      l = () => {
        r = () => !1
      },
      u = (f) => {
        t.delete(f)
      }
    return {
      on: (f) => {
        t.add(f)
        const h = () => u(f)
        return (Ar(h), { off: h })
      },
      off: u,
      trigger: (f) => {
        const h = [n]
        return (o() ? h.push(...t) : e && h.push(e), Promise.allSettled(h.map((g) => g(f))))
      },
      hasListeners: o,
      listeners: t,
      setEmitter: i,
      removeEmitter: a,
      setHasEmitListeners: s,
      removeHasEmitListeners: l,
    }
  }
  function V0(e, t, n) {
    let r = e
    do {
      if (r && r.matches(t)) return !0
      if (r === n) return !1
      r = r.parentElement
    } while (r)
    return !1
  }
  function yz(e, t, n, r) {
    var o, i
    const a = new Map()
    for (const [s, l] of e)
      (l.selected || l.id === r) &&
        (!l.parentNode || !CS(l, e)) &&
        (l.draggable || (t && typeof l.draggable > 'u')) &&
        e.get(s) &&
        a.set(s, {
          id: l.id,
          position: l.position || { x: 0, y: 0 },
          distance: {
            x: n.x - ((o = l.computedPosition) == null ? void 0 : o.x) || 0,
            y: n.y - ((i = l.computedPosition) == null ? void 0 : i.y) || 0,
          },
          from: { x: l.computedPosition.x, y: l.computedPosition.y },
          extent: l.extent,
          parentNode: l.parentNode,
          dimensions: { ...l.dimensions },
          expandParent: l.expandParent,
        })
    return Array.from(a.values())
  }
  function bd({ id: e, dragItems: t, findNode: n }) {
    const r = []
    for (const o of t) {
      const i = n(o.id)
      i && r.push(i)
    }
    return [e ? r.find((o) => o.id === e) : r[0], r]
  }
  function $S(e) {
    if (Array.isArray(e))
      switch (e.length) {
        case 1:
          return [e[0], e[0], e[0], e[0]]
        case 2:
          return [e[0], e[1], e[0], e[1]]
        case 3:
          return [e[0], e[1], e[2], e[1]]
        case 4:
          return e
        default:
          return [0, 0, 0, 0]
      }
    return [e, e, e, e]
  }
  function bz(e, t, n) {
    const [r, o, i, a] = typeof e != 'string' ? $S(e.padding) : [0, 0, 0, 0]
    return n &&
      typeof n.computedPosition.x < 'u' &&
      typeof n.computedPosition.y < 'u' &&
      typeof n.dimensions.width < 'u' &&
      typeof n.dimensions.height < 'u'
      ? [
          [n.computedPosition.x + a, n.computedPosition.y + r],
          [
            n.computedPosition.x + n.dimensions.width - o,
            n.computedPosition.y + n.dimensions.height - i,
          ],
        ]
      : !1
  }
  function _z(e, t, n, r) {
    let o = e.extent || n
    if ((o === 'parent' || (!Array.isArray(o) && o?.range === 'parent')) && !e.expandParent)
      if (e.parentNode && r && e.dimensions.width && e.dimensions.height) {
        const i = bz(o, e, r)
        i && (o = i)
      } else (t(new Le(Be.NODE_EXTENT_INVALID, e.id)), (o = n))
    else if (Array.isArray(o)) {
      const i = r?.computedPosition.x || 0,
        a = r?.computedPosition.y || 0
      o = [
        [o[0][0] + i, o[0][1] + a],
        [o[1][0] + i, o[1][1] + a],
      ]
    } else if (o !== 'parent' && o?.range && Array.isArray(o.range)) {
      const [i, a, s, l] = $S(o.padding),
        u = r?.computedPosition.x || 0,
        c = r?.computedPosition.y || 0
      o = [
        [o.range[0][0] + u + l, o.range[0][1] + c + i],
        [o.range[1][0] + u - a, o.range[1][1] + c - s],
      ]
    }
    return o === 'parent'
      ? [
          [Number.NEGATIVE_INFINITY, Number.NEGATIVE_INFINITY],
          [Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY],
        ]
      : o
  }
  function wz({ width: e, height: t }, n) {
    return [n[0], [n[1][0] - (e || 0), n[1][1] - (t || 0)]]
  }
  function ah(e, t, n, r, o) {
    const i = wz(e.dimensions, _z(e, n, r, o)),
      a = gS(t, i)
    return {
      position: { x: a.x - (o?.computedPosition.x || 0), y: a.y - (o?.computedPosition.y || 0) },
      computedPosition: a,
    }
  }
  function Un(e, t, n = pe.Left, r = !1) {
    const o = (t?.x ?? 0) + e.computedPosition.x,
      i = (t?.y ?? 0) + e.computedPosition.y,
      { width: a, height: s } = t ?? Ez(e)
    if (r) return { x: o + a / 2, y: i + s / 2 }
    switch (t?.position ?? n) {
      case pe.Top:
        return { x: o + a / 2, y: i }
      case pe.Right:
        return { x: o + a, y: i + s / 2 }
      case pe.Bottom:
        return { x: o + a / 2, y: i + s }
      case pe.Left:
        return { x: o, y: i + s / 2 }
    }
  }
  function G0(e, t) {
    return (e && (t ? e.find((n) => n.id === t) : e[0])) || null
  }
  function Sz({
    sourcePos: e,
    targetPos: t,
    sourceWidth: n,
    sourceHeight: r,
    targetWidth: o,
    targetHeight: i,
    width: a,
    height: s,
    viewport: l,
  }) {
    const u = {
      x: Math.min(e.x, t.x),
      y: Math.min(e.y, t.y),
      x2: Math.max(e.x + n, t.x + o),
      y2: Math.max(e.y + r, t.y + i),
    }
    ;(u.x === u.x2 && (u.x2 += 1), u.y === u.y2 && (u.y2 += 1))
    const c = _S({
        x: (0 - l.x) / l.zoom,
        y: (0 - l.y) / l.zoom,
        width: a / l.zoom,
        height: s / l.zoom,
      }),
      d = Math.max(0, Math.min(c.x2, u.x2) - Math.max(c.x, u.x)),
      f = Math.max(0, Math.min(c.y2, u.y2) - Math.max(c.y, u.y))
    return Math.ceil(d * f) > 0
  }
  function xz(e, t, n = !1) {
    const r = typeof e.zIndex == 'number'
    let o = r ? e.zIndex : 0
    const i = t(e.source),
      a = t(e.target)
    return !i || !a
      ? 0
      : (n && (o = r ? e.zIndex : Math.max(i.computedPosition.z || 0, a.computedPosition.z || 0)),
        o)
  }
  var Be = ((e) => (
    (e.MISSING_STYLES = 'MISSING_STYLES'),
    (e.MISSING_VIEWPORT_DIMENSIONS = 'MISSING_VIEWPORT_DIMENSIONS'),
    (e.NODE_INVALID = 'NODE_INVALID'),
    (e.NODE_NOT_FOUND = 'NODE_NOT_FOUND'),
    (e.NODE_MISSING_PARENT = 'NODE_MISSING_PARENT'),
    (e.NODE_TYPE_MISSING = 'NODE_TYPE_MISSING'),
    (e.NODE_EXTENT_INVALID = 'NODE_EXTENT_INVALID'),
    (e.EDGE_INVALID = 'EDGE_INVALID'),
    (e.EDGE_NOT_FOUND = 'EDGE_NOT_FOUND'),
    (e.EDGE_SOURCE_MISSING = 'EDGE_SOURCE_MISSING'),
    (e.EDGE_TARGET_MISSING = 'EDGE_TARGET_MISSING'),
    (e.EDGE_TYPE_MISSING = 'EDGE_TYPE_MISSING'),
    (e.EDGE_SOURCE_TARGET_SAME = 'EDGE_SOURCE_TARGET_SAME'),
    (e.EDGE_SOURCE_TARGET_MISSING = 'EDGE_SOURCE_TARGET_MISSING'),
    (e.EDGE_ORPHANED = 'EDGE_ORPHANED'),
    (e.USEVUEFLOW_OPTIONS = 'USEVUEFLOW_OPTIONS'),
    e
  ))(Be || {})
  const W0 = {
    MISSING_STYLES: () =>
      "It seems that you haven't loaded the necessary styles. Please import '@vue-flow/core/dist/style.css' to ensure that the graph is rendered correctly",
    MISSING_VIEWPORT_DIMENSIONS: () =>
      'The Vue Flow parent container needs a width and a height to render the graph',
    NODE_INVALID: (e) => `Node is invalid
Node: ${e}`,
    NODE_NOT_FOUND: (e) => `Node not found
Node: ${e}`,
    NODE_MISSING_PARENT: (e, t) => `Node is missing a parent
Node: ${e}
Parent: ${t}`,
    NODE_TYPE_MISSING: (e) => `Node type is missing
Type: ${e}`,
    NODE_EXTENT_INVALID: (e) => `Only child nodes can use a parent extent
Node: ${e}`,
    EDGE_INVALID: (e) => `An edge needs a source and a target
Edge: ${e}`,
    EDGE_SOURCE_MISSING: (e, t) => `Edge source is missing
Edge: ${e} 
Source: ${t}`,
    EDGE_TARGET_MISSING: (e, t) => `Edge target is missing
Edge: ${e} 
Target: ${t}`,
    EDGE_TYPE_MISSING: (e) => `Edge type is missing
Type: ${e}`,
    EDGE_SOURCE_TARGET_SAME: (e, t, n) => `Edge source and target are the same
Edge: ${e} 
Source: ${t} 
Target: ${n}`,
    EDGE_SOURCE_TARGET_MISSING: (e, t, n) => `Edge source or target is missing
Edge: ${e} 
Source: ${t} 
Target: ${n}`,
    EDGE_ORPHANED: (
      e
    ) => `Edge was orphaned (suddenly missing source or target) and has been removed
Edge: ${e}`,
    EDGE_NOT_FOUND: (e) => `Edge not found
Edge: ${e}`,
    USEVUEFLOW_OPTIONS: () =>
      'The options parameter is deprecated and will be removed in the next major version. Please use the id parameter instead',
  }
  class Le extends Error {
    constructor(t, ...n) {
      var r
      ;(super((r = W0[t]) == null ? void 0 : r.call(W0, ...n)),
        (this.name = 'VueFlowError'),
        (this.code = t),
        (this.args = n))
    }
  }
  function sh(e) {
    return 'clientX' in e
  }
  function Cz(e) {
    return 'sourceEvent' in e
  }
  function mt(e, t) {
    const n = sh(e)
    let r, o
    return (
      n
        ? ((r = e.clientX), (o = e.clientY))
        : 'touches' in e && e.touches.length > 0
          ? ((r = e.touches[0].clientX), (o = e.touches[0].clientY))
          : 'changedTouches' in e && e.changedTouches.length > 0
            ? ((r = e.changedTouches[0].clientX), (o = e.changedTouches[0].clientY))
            : ((r = 0), (o = 0)),
      { x: r - (t?.left ?? 0), y: o - (t?.top ?? 0) }
    )
  }
  const Xo = () => {
    var e
    return (
      typeof navigator < 'u' &&
      ((e = navigator?.userAgent) == null ? void 0 : e.indexOf('Mac')) >= 0
    )
  }
  function Ez(e) {
    var t, n
    return {
      width: ((t = e.dimensions) == null ? void 0 : t.width) ?? e.width ?? 0,
      height: ((n = e.dimensions) == null ? void 0 : n.height) ?? e.height ?? 0,
    }
  }
  function Ii(e, t = [1, 1]) {
    return { x: t[0] * Math.round(e.x / t[0]), y: t[1] * Math.round(e.y / t[1]) }
  }
  const $z = () => !0
  function _d(e) {
    e?.classList.remove(
      'valid',
      'connecting',
      'vue-flow__handle-valid',
      'vue-flow__handle-connecting'
    )
  }
  function Tz(e, t, n) {
    const r = [],
      o = { x: e.x - n, y: e.y - n, width: n * 2, height: n * 2 }
    for (const i of t.values()) Yo(o, Uo(i)) > 0 && r.push(i)
    return r
  }
  const Oz = 250
  function Pz(e, t, n, r) {
    var o, i
    let a = [],
      s = Number.POSITIVE_INFINITY
    const l = Tz(e, n, t + Oz)
    for (const u of l) {
      const c = [
        ...(((o = u.handleBounds) == null ? void 0 : o.source) ?? []),
        ...(((i = u.handleBounds) == null ? void 0 : i.target) ?? []),
      ]
      for (const d of c) {
        if (r.nodeId === d.nodeId && r.type === d.type && r.id === d.id) continue
        const { x: f, y: h } = Un(u, d, d.position, !0),
          g = Math.sqrt((f - e.x) ** 2 + (h - e.y) ** 2)
        g > t ||
          (g < s
            ? ((a = [{ ...d, x: f, y: h }]), (s = g))
            : g === s && a.push({ ...d, x: f, y: h }))
      }
    }
    if (!a.length) return null
    if (a.length > 1) {
      const u = r.type === 'source' ? 'target' : 'source'
      return a.find((c) => c.type === u) ?? a[0]
    }
    return a[0]
  }
  function U0(
    e,
    {
      handle: t,
      connectionMode: n,
      fromNodeId: r,
      fromHandleId: o,
      fromType: i,
      doc: a,
      lib: s,
      flowId: l,
      isValidConnection: u = $z,
    },
    c,
    d,
    f,
    h
  ) {
    const g = i === 'target',
      m = t
        ? a.querySelector(`.${s}-flow__handle[data-id="${l}-${t?.nodeId}-${t?.id}-${t?.type}"]`)
        : null,
      { x: v, y: b } = mt(e),
      y = a.elementFromPoint(v, b),
      p = y?.classList.contains(`${s}-flow__handle`) ? y : m,
      _ = { handleDomNode: p, isValid: !1, connection: null, toHandle: null }
    if (p) {
      const x = TS(void 0, p),
        S = p.getAttribute('data-nodeid'),
        w = p.getAttribute('data-handleid'),
        T = p.classList.contains('connectable'),
        A = p.classList.contains('connectableend')
      if (!S || !x) return _
      const $ = {
        source: g ? S : r,
        sourceHandle: g ? w : o,
        target: g ? r : S,
        targetHandle: g ? o : w,
      }
      _.connection = $
      const E =
        T &&
        A &&
        (n === Zt.Strict ? (g && x === 'source') || (!g && x === 'target') : S !== r || w !== o)
      ;((_.isValid =
        E && u($, { nodes: d, edges: c, sourceNode: f($.source), targetNode: f($.target) })),
        (_.toHandle = OS(S, x, w, h, n, !0)))
    }
    return _
  }
  function TS(e, t) {
    return (
      e ||
      (t?.classList.contains('target')
        ? 'target'
        : t?.classList.contains('source')
          ? 'source'
          : null)
    )
  }
  function Iz(e, t) {
    let n = null
    return (t ? (n = 'valid') : e && !t && (n = 'invalid'), n)
  }
  function Az(e, t) {
    let n = null
    return (t ? (n = !0) : e && !t && (n = !1), n)
  }
  function OS(e, t, n, r, o, i = !1) {
    var a, s, l
    const u = r.get(e)
    if (!u) return null
    const c =
        o === Zt.Strict
          ? (a = u.handleBounds) == null
            ? void 0
            : a[t]
          : [
              ...(((s = u.handleBounds) == null ? void 0 : s.source) ?? []),
              ...(((l = u.handleBounds) == null ? void 0 : l.target) ?? []),
            ],
      d = (n ? c?.find((f) => f.id === n) : c?.[0]) ?? null
    return d && i ? { ...d, ...Un(u, d, d.position, !0) } : d
  }
  const Jd = { [pe.Left]: pe.Right, [pe.Right]: pe.Left, [pe.Top]: pe.Bottom, [pe.Bottom]: pe.Top },
    Nz = ['production', 'prod']
  function Zr(e, ...t) {
    PS() && console.warn(`[Vue Flow]: ${e}`, ...t)
  }
  function PS() {
    return !Nz.includes('production')
  }
  function Y0(e, t, n, r, o) {
    const i = t.querySelectorAll(`.vue-flow__handle.${e}`)
    return i?.length
      ? Array.from(i).map((a) => {
          const s = a.getBoundingClientRect()
          return {
            id: a.getAttribute('data-handleid'),
            type: e,
            nodeId: o,
            position: a.getAttribute('data-handlepos'),
            x: (s.left - n.left) / r,
            y: (s.top - n.top) / r,
            ...Pi(a),
          }
        })
      : null
  }
  function Qd(e, t, n, r, o, i = !1, a) {
    ;((o.value = !1),
      e.selected
        ? (i || (e.selected && t)) &&
          (r([e]),
          Ne(() => {
            a.blur()
          }))
        : n([e]))
  }
  function De(e) {
    return typeof K(e) < 'u'
  }
  function Rz(e, t, n, r) {
    if (!e || !e.source || !e.target)
      return (n(new Le(Be.EDGE_INVALID, e?.id ?? '[ID UNKNOWN]')), !1)
    let o
    return (Jt(e) ? (o = e) : (o = { ...e, id: bS(e) }), (o = mS(o, void 0, r)), fz(o, t) ? !1 : o)
  }
  function Mz(e, t, n, r, o) {
    if (!t.source || !t.target) return (o(new Le(Be.EDGE_INVALID, e.id)), !1)
    if (!n) return (o(new Le(Be.EDGE_NOT_FOUND, e.id)), !1)
    const { id: i, ...a } = e
    return {
      ...a,
      id: r ? bS(t) : i,
      source: t.source,
      target: t.target,
      sourceHandle: t.sourceHandle,
      targetHandle: t.targetHandle,
    }
  }
  function X0(e, t, n) {
    const r = {},
      o = []
    for (let i = 0; i < e.length; ++i) {
      const a = e[i]
      if (!mn(a)) {
        n(new Le(Be.NODE_INVALID, a?.id) || `[ID UNKNOWN|INDEX ${i}]`)
        continue
      }
      const s = uz(a, t(a.id), a.parentNode)
      ;(a.parentNode && (r[a.parentNode] = !0), (o[i] = s))
    }
    for (const i of o) {
      const a = t(i.parentNode) || o.find((s) => s.id === i.parentNode)
      ;(i.parentNode && !a && n(new Le(Be.NODE_MISSING_PARENT, i.id, i.parentNode)),
        (i.parentNode || r[i.id]) && (r[i.id] && (i.isParent = !0), a && (a.isParent = !0)))
    }
    return o
  }
  function K0(e, t, n, r, o, i) {
    let a = o
    const s = r.get(a) || new Map()
    ;(r.set(a, s.set(n, t)), (a = `${o}-${e}`))
    const l = r.get(a) || new Map()
    if ((r.set(a, l.set(n, t)), i)) {
      a = `${o}-${e}-${i}`
      const u = r.get(a) || new Map()
      r.set(a, u.set(n, t))
    }
  }
  function wd(e, t, n) {
    e.clear()
    for (const r of n) {
      const { source: o, target: i, sourceHandle: a = null, targetHandle: s = null } = r,
        l = { edgeId: r.id, source: o, target: i, sourceHandle: a, targetHandle: s },
        u = `${o}-${a}--${i}-${s}`,
        c = `${i}-${s}--${o}-${a}`
      ;(K0('source', l, c, e, o, a), K0('target', l, u, e, i, s))
    }
  }
  function Z0(e, t) {
    if (e.size !== t.size) return !1
    for (const n of e) if (!t.has(n)) return !1
    return !0
  }
  function Sd(e, t, n, r, o, i, a, s) {
    const l = []
    for (const u of e) {
      const c = Jt(u) ? u : Rz(u, s, o, i)
      if (!c) continue
      const d = n(c.source),
        f = n(c.target)
      if (!d || !f) {
        o(new Le(Be.EDGE_SOURCE_TARGET_MISSING, c.id, c.source, c.target))
        continue
      }
      if (!d) {
        o(new Le(Be.EDGE_SOURCE_MISSING, c.id, c.source))
        continue
      }
      if (!f) {
        o(new Le(Be.EDGE_TARGET_MISSING, c.id, c.target))
        continue
      }
      if (t && !t(c, { edges: s, nodes: a, sourceNode: d, targetNode: f })) {
        o(new Le(Be.EDGE_INVALID, c.id))
        continue
      }
      const h = r(c.id)
      l.push({ ...mS(c, h, i), sourceNode: d, targetNode: f })
    }
    return l
  }
  const J0 = Symbol('vueFlow'),
    IS = Symbol('nodeId'),
    AS = Symbol('nodeRef'),
    Dz = Symbol('edgeId'),
    Bz = Symbol('edgeRef'),
    Ai = Symbol('slots')
  function NS(e) {
    const {
        vueFlowRef: t,
        snapToGrid: n,
        snapGrid: r,
        noDragClassName: o,
        nodeLookup: i,
        nodeExtent: a,
        nodeDragThreshold: s,
        viewport: l,
        autoPanOnNodeDrag: u,
        autoPanSpeed: c,
        nodesDraggable: d,
        panBy: f,
        findNode: h,
        multiSelectionActive: g,
        nodesSelectionActive: m,
        selectNodesOnDrag: v,
        removeSelectedElements: b,
        addSelectedNodes: y,
        updateNodePositions: p,
        emits: _,
      } = Ae(),
      {
        onStart: x,
        onDrag: S,
        onStop: w,
        onClick: T,
        el: A,
        disabled: $,
        id: P,
        selectable: E,
        dragHandle: z,
      } = e,
      C = ce(!1)
    let R = [],
      N,
      j = null,
      V = { x: void 0, y: void 0 },
      H = { x: 0, y: 0 },
      G = null,
      Y = !1,
      Z = !1,
      ne = 0,
      B = !1
    const L = Lz(),
      k = ({ x: ye, y: be }) => {
        V = { x: ye, y: be }
        let M = !1
        if (
          ((R = R.map((O) => {
            const q = { x: ye - O.distance.x, y: be - O.distance.y },
              { computedPosition: I } = ah(
                O,
                n.value ? Ii(q, r.value) : q,
                _.error,
                a.value,
                O.parentNode ? h(O.parentNode) : void 0
              )
            return ((M = M || O.position.x !== I.x || O.position.y !== I.y), (O.position = I), O)
          })),
          (Z = Z || M),
          !!M && (p(R, !0, !0), (C.value = !0), G))
        ) {
          const [O, q] = bd({ id: P, dragItems: R, findNode: h })
          S({ event: G, node: O, nodes: q })
        }
      },
      U = () => {
        if (!j) return
        const [ye, be] = ES(H, j, c.value)
        if (ye !== 0 || be !== 0) {
          const M = { x: (V.x ?? 0) - ye / l.value.zoom, y: (V.y ?? 0) - be / l.value.zoom }
          f({ x: ye, y: be }) && k(M)
        }
        ne = requestAnimationFrame(U)
      },
      J = (ye, be) => {
        Y = !0
        const M = h(P)
        ;(!v.value && !g.value && M && (M.selected || b()),
          M && Ee(E) && v.value && Qd(M, g.value, y, b, m, !1, be))
        const O = L(ye.sourceEvent)
        if (((V = O), (R = yz(i.value, d.value, O, P)), R.length)) {
          const [q, I] = bd({ id: P, dragItems: R, findNode: h })
          x({ event: ye.sourceEvent, node: q, nodes: I })
        }
      },
      re = (ye, be) => {
        var M
        ;(ye.sourceEvent.type === 'touchmove' && ye.sourceEvent.touches.length > 1) ||
          ((Z = !1),
          s.value === 0 && J(ye, be),
          (V = L(ye.sourceEvent)),
          (j = ((M = t.value) == null ? void 0 : M.getBoundingClientRect()) || null),
          (H = mt(ye.sourceEvent, j)))
      },
      ie = (ye, be) => {
        const M = L(ye.sourceEvent)
        if ((!B && Y && u.value && ((B = !0), U()), !Y)) {
          const O = M.xSnapped - (V.x ?? 0),
            q = M.ySnapped - (V.y ?? 0)
          Math.sqrt(O * O + q * q) > s.value && J(ye, be)
        }
        ;(V.x !== M.xSnapped || V.y !== M.ySnapped) &&
          R.length &&
          Y &&
          ((G = ye.sourceEvent), (H = mt(ye.sourceEvent, j)), k(M))
      },
      _e = (ye) => {
        let be = !1
        if (!Y && !C.value && !g.value) {
          const M = ye.sourceEvent,
            O = L(M),
            q = O.xSnapped - (V.x ?? 0),
            I = O.ySnapped - (V.y ?? 0),
            W = Math.sqrt(q * q + I * I)
          W !== 0 && W <= s.value && (T?.(M), (be = !0))
        }
        if (R.length && !be) {
          Z && (p(R, !1, !1), (Z = !1))
          const [M, O] = bd({ id: P, dragItems: R, findNode: h })
          w({ event: ye.sourceEvent, node: M, nodes: O })
        }
        ;((R = []),
          (C.value = !1),
          (B = !1),
          (Y = !1),
          (V = { x: void 0, y: void 0 }),
          cancelAnimationFrame(ne))
      }
    return (
      me([() => Ee($), A], ([ye, be], M, O) => {
        if (be) {
          const q = lt(be)
          ;(ye ||
            ((N = lB()
              .on('start', (I) => re(I, be))
              .on('drag', (I) => ie(I, be))
              .on('end', (I) => _e(I))
              .filter((I) => {
                const W = I.target,
                  ae = Ee(z)
                return (
                  !I.button && (!o.value || (!V0(W, `.${o.value}`, be) && (!ae || V0(W, ae, be))))
                )
              })),
            q.call(N)),
            O(() => {
              ;(q.on('.drag', null),
                N && (N.on('start', null), N.on('drag', null), N.on('end', null)))
            }))
        }
      }),
      C
    )
  }
  function qz() {
    return {
      doubleClick: se(),
      click: se(),
      mouseEnter: se(),
      mouseMove: se(),
      mouseLeave: se(),
      contextMenu: se(),
      updateStart: se(),
      update: se(),
      updateEnd: se(),
    }
  }
  function zz(e, t) {
    const n = qz()
    return (
      n.doubleClick.on((r) => {
        var o, i
        ;(t.edgeDoubleClick(r),
          (i = (o = e.events) == null ? void 0 : o.doubleClick) == null || i.call(o, r))
      }),
      n.click.on((r) => {
        var o, i
        ;(t.edgeClick(r), (i = (o = e.events) == null ? void 0 : o.click) == null || i.call(o, r))
      }),
      n.mouseEnter.on((r) => {
        var o, i
        ;(t.edgeMouseEnter(r),
          (i = (o = e.events) == null ? void 0 : o.mouseEnter) == null || i.call(o, r))
      }),
      n.mouseMove.on((r) => {
        var o, i
        ;(t.edgeMouseMove(r),
          (i = (o = e.events) == null ? void 0 : o.mouseMove) == null || i.call(o, r))
      }),
      n.mouseLeave.on((r) => {
        var o, i
        ;(t.edgeMouseLeave(r),
          (i = (o = e.events) == null ? void 0 : o.mouseLeave) == null || i.call(o, r))
      }),
      n.contextMenu.on((r) => {
        var o, i
        ;(t.edgeContextMenu(r),
          (i = (o = e.events) == null ? void 0 : o.contextMenu) == null || i.call(o, r))
      }),
      n.updateStart.on((r) => {
        var o, i
        ;(t.edgeUpdateStart(r),
          (i = (o = e.events) == null ? void 0 : o.updateStart) == null || i.call(o, r))
      }),
      n.update.on((r) => {
        var o, i
        ;(t.edgeUpdate(r), (i = (o = e.events) == null ? void 0 : o.update) == null || i.call(o, r))
      }),
      n.updateEnd.on((r) => {
        var o, i
        ;(t.edgeUpdateEnd(r),
          (i = (o = e.events) == null ? void 0 : o.updateEnd) == null || i.call(o, r))
      }),
      Object.entries(n).reduce((r, [o, i]) => ((r.emit[o] = i.trigger), (r.on[o] = i.on), r), {
        emit: {},
        on: {},
      })
    )
  }
  function Lz() {
    const { viewport: e, snapGrid: t, snapToGrid: n, vueFlowRef: r } = Ae()
    return (o) => {
      var i
      const a = ((i = r.value) == null ? void 0 : i.getBoundingClientRect()) ?? { left: 0, top: 0 },
        s = Cz(o) ? o.sourceEvent : o,
        { x: l, y: u } = mt(s, a),
        c = qr({ x: l, y: u }, e.value),
        { x: d, y: f } = n.value ? Ii(c, t.value) : c
      return { xSnapped: d, ySnapped: f, ...c }
    }
  }
  function go() {
    return !0
  }
  function RS({
    handleId: e,
    nodeId: t,
    type: n,
    isValidConnection: r,
    edgeUpdaterType: o,
    onEdgeUpdate: i,
    onEdgeUpdateEnd: a,
  }) {
    const {
      id: s,
      vueFlowRef: l,
      connectionMode: u,
      connectionRadius: c,
      connectOnClick: d,
      connectionClickStartHandle: f,
      nodesConnectable: h,
      autoPanOnConnect: g,
      autoPanSpeed: m,
      findNode: v,
      panBy: b,
      startConnection: y,
      updateConnection: p,
      endConnection: _,
      emits: x,
      viewport: S,
      edges: w,
      nodes: T,
      isValidConnection: A,
      nodeLookup: $,
    } = Ae()
    let P = null,
      E = !1,
      z = null
    function C(N) {
      var j
      const V = Ee(n) === 'target',
        H = sh(N),
        G = D0(N.target),
        Y = N.currentTarget
      if (Y && ((H && N.button === 0) || !H)) {
        let Z = function (ue) {
            ;((M = mt(ue, _e)),
              (k = Pz(qr(M, S.value, !1, [1, 1]), c.value, $.value, I)),
              O || (q(), (O = !0)))
            const ge = U0(
              ue,
              {
                handle: k,
                connectionMode: u.value,
                fromNodeId: Ee(t),
                fromHandleId: Ee(e),
                fromType: V ? 'target' : 'source',
                isValidConnection: L,
                doc: G,
                lib: 'vue',
                flowId: s,
                nodeLookup: $.value,
              },
              w.value,
              T.value,
              v,
              $.value
            )
            ;((z = ge.handleDomNode), (P = ge.connection), (E = Az(!!k, ge.isValid)))
            const Se = {
              ...le,
              isValid: E,
              to: ge.toHandle && E ? Br({ x: ge.toHandle.x, y: ge.toHandle.y }, S.value) : M,
              toHandle: ge.toHandle,
              toPosition: E && ge.toHandle ? ge.toHandle.position : Jd[I.position],
              toNode: ge.toHandle ? $.value.get(ge.toHandle.nodeId) : null,
            }
            if (
              E &&
              k &&
              le?.toHandle &&
              Se.toHandle &&
              le.toHandle.type === Se.toHandle.type &&
              le.toHandle.nodeId === Se.toHandle.nodeId &&
              le.toHandle.id === Se.toHandle.id &&
              le.to.x === Se.to.x &&
              le.to.y === Se.to.y
            )
              return
            const $e = k ?? ge.toHandle
            if (
              (p($e && E ? Br({ x: $e.x, y: $e.y }, S.value) : M, ge.toHandle, Iz(!!$e, E)),
              (le = Se),
              !k && !E && !z)
            )
              return _d(be)
            P &&
              P.source !== P.target &&
              z &&
              (_d(be),
              (be = z),
              z.classList.add('connecting', 'vue-flow__handle-connecting'),
              z.classList.toggle('valid', !!E),
              z.classList.toggle('vue-flow__handle-valid', !!E))
          },
          ne = function (ue) {
            ;('touches' in ue && ue.touches.length > 0) ||
              ((k || z) && P && E && (i ? i(ue, P) : x.connect(P)),
              x.connectEnd(ue),
              o && a?.(ue),
              _d(be),
              cancelAnimationFrame(U),
              _(ue),
              (O = !1),
              (E = !1),
              (P = null),
              (z = null),
              G.removeEventListener('mousemove', Z),
              G.removeEventListener('mouseup', ne),
              G.removeEventListener('touchmove', Z),
              G.removeEventListener('touchend', ne))
          }
        const B = v(Ee(t))
        let L = Ee(r) || A.value || go
        !L && B && (L = (V ? B.isValidSourcePos : B.isValidTargetPos) || go)
        let k,
          U = 0
        const { x: J, y: re } = mt(N),
          ie = TS(Ee(o), Y),
          _e = (j = l.value) == null ? void 0 : j.getBoundingClientRect()
        if (!_e || !ie) return
        const ye = OS(Ee(t), ie, Ee(e), $.value, u.value)
        if (!ye) return
        let be,
          M = mt(N, _e),
          O = !1
        const q = () => {
            if (!g.value) return
            const [ue, ge] = ES(M, _e, m.value)
            ;(b({ x: ue, y: ge }), (U = requestAnimationFrame(q)))
          },
          I = { ...ye, nodeId: Ee(t), type: ie, position: ye.position },
          W = $.value.get(Ee(t)),
          fe = {
            inProgress: !0,
            isValid: null,
            from: Un(W, I, pe.Left, !0),
            fromHandle: I,
            fromPosition: I.position,
            fromNode: W,
            to: M,
            toHandle: null,
            toPosition: Jd[I.position],
            toNode: null,
          }
        ;(y(
          {
            nodeId: Ee(t),
            id: Ee(e),
            type: ie,
            position: Y?.getAttribute('data-handlepos') || pe.Top,
            ...M,
          },
          { x: J - _e.left, y: re - _e.top }
        ),
          x.connectStart({ event: N, nodeId: Ee(t), handleId: Ee(e), handleType: ie }))
        let le = fe
        ;(G.addEventListener('mousemove', Z),
          G.addEventListener('mouseup', ne),
          G.addEventListener('touchmove', Z),
          G.addEventListener('touchend', ne))
      }
    }
    function R(N) {
      var j, V
      if (!d.value) return
      const H = Ee(n) === 'target'
      if (!f.value) {
        ;(x.clickConnectStart({ event: N, nodeId: Ee(t), handleId: Ee(e) }),
          y({ nodeId: Ee(t), type: Ee(n), id: Ee(e), position: pe.Top, ...mt(N) }, void 0, !0))
        return
      }
      let G = Ee(r) || A.value || go
      const Y = v(Ee(t))
      if (
        (!G && Y && (G = (H ? Y.isValidSourcePos : Y.isValidTargetPos) || go),
        Y && (typeof Y.connectable > 'u' ? h.value : Y.connectable) === !1)
      )
        return
      const Z = D0(N.target),
        ne = U0(
          N,
          {
            handle: { nodeId: Ee(t), id: Ee(e), type: Ee(n), position: pe.Top, ...mt(N) },
            connectionMode: u.value,
            fromNodeId: f.value.nodeId,
            fromHandleId: f.value.id ?? null,
            fromType: f.value.type,
            isValidConnection: G,
            doc: Z,
            lib: 'vue',
            flowId: s,
            nodeLookup: $.value,
          },
          w.value,
          T.value,
          v,
          $.value
        ),
        B =
          ((j = ne.connection) == null ? void 0 : j.source) ===
          ((V = ne.connection) == null ? void 0 : V.target)
      ;(ne.isValid && ne.connection && !B && x.connect(ne.connection),
        x.clickConnectEnd(N),
        _(N, !0))
    }
    return { handlePointerDown: C, handleClick: R }
  }
  function Fz() {
    return xt(IS, '')
  }
  function MS(e) {
    const t = e ?? Fz() ?? '',
      n = xt(AS, de(null)),
      { findNode: r, edges: o, emits: i } = Ae(),
      a = r(t)
    return (
      a || i.error(new Le(Be.NODE_NOT_FOUND, t)),
      {
        id: t,
        nodeEl: n,
        node: a,
        parentNode: X(() => r(a.parentNode)),
        connectedEdges: X(() => xS([a], o.value)),
      }
    )
  }
  function kz() {
    return {
      doubleClick: se(),
      click: se(),
      mouseEnter: se(),
      mouseMove: se(),
      mouseLeave: se(),
      contextMenu: se(),
      dragStart: se(),
      drag: se(),
      dragStop: se(),
    }
  }
  function Hz(e, t) {
    const n = kz()
    return (
      n.doubleClick.on((r) => {
        var o, i
        ;(t.nodeDoubleClick(r),
          (i = (o = e.events) == null ? void 0 : o.doubleClick) == null || i.call(o, r))
      }),
      n.click.on((r) => {
        var o, i
        ;(t.nodeClick(r), (i = (o = e.events) == null ? void 0 : o.click) == null || i.call(o, r))
      }),
      n.mouseEnter.on((r) => {
        var o, i
        ;(t.nodeMouseEnter(r),
          (i = (o = e.events) == null ? void 0 : o.mouseEnter) == null || i.call(o, r))
      }),
      n.mouseMove.on((r) => {
        var o, i
        ;(t.nodeMouseMove(r),
          (i = (o = e.events) == null ? void 0 : o.mouseMove) == null || i.call(o, r))
      }),
      n.mouseLeave.on((r) => {
        var o, i
        ;(t.nodeMouseLeave(r),
          (i = (o = e.events) == null ? void 0 : o.mouseLeave) == null || i.call(o, r))
      }),
      n.contextMenu.on((r) => {
        var o, i
        ;(t.nodeContextMenu(r),
          (i = (o = e.events) == null ? void 0 : o.contextMenu) == null || i.call(o, r))
      }),
      n.dragStart.on((r) => {
        var o, i
        ;(t.nodeDragStart(r),
          (i = (o = e.events) == null ? void 0 : o.dragStart) == null || i.call(o, r))
      }),
      n.drag.on((r) => {
        var o, i
        ;(t.nodeDrag(r), (i = (o = e.events) == null ? void 0 : o.drag) == null || i.call(o, r))
      }),
      n.dragStop.on((r) => {
        var o, i
        ;(t.nodeDragStop(r),
          (i = (o = e.events) == null ? void 0 : o.dragStop) == null || i.call(o, r))
      }),
      Object.entries(n).reduce((r, [o, i]) => ((r.emit[o] = i.trigger), (r.on[o] = i.on), r), {
        emit: {},
        on: {},
      })
    )
  }
  function DS() {
    const {
      getSelectedNodes: e,
      nodeExtent: t,
      updateNodePositions: n,
      findNode: r,
      snapGrid: o,
      snapToGrid: i,
      nodesDraggable: a,
      emits: s,
    } = Ae()
    return (l, u = !1) => {
      const c = i.value ? o.value[0] : 5,
        d = i.value ? o.value[1] : 5,
        f = u ? 4 : 1,
        h = l.x * c * f,
        g = l.y * d * f,
        m = []
      for (const v of e.value)
        if (v.draggable || (a && typeof v.draggable > 'u')) {
          const b = { x: v.computedPosition.x + h, y: v.computedPosition.y + g },
            { position: y } = ah(v, b, s.error, t.value, v.parentNode ? r(v.parentNode) : void 0)
          m.push({
            id: v.id,
            position: y,
            from: v.position,
            distance: { x: l.x, y: l.y },
            dimensions: v.dimensions,
          })
        }
      n(m, !0, !1)
    }
  }
  const mo = 0.1,
    jz = (e) => ((e *= 2) <= 1 ? e * e * e : (e -= 2) * e * e + 2) / 2
  function Wt() {
    return (Zr('Viewport not initialized yet.'), Promise.resolve(!1))
  }
  const Vz = {
    zoomIn: Wt,
    zoomOut: Wt,
    zoomTo: Wt,
    fitView: Wt,
    setCenter: Wt,
    fitBounds: Wt,
    project: (e) => e,
    screenToFlowCoordinate: (e) => e,
    flowToScreenCoordinate: (e) => e,
    setViewport: Wt,
    setTransform: Wt,
    getViewport: () => ({ x: 0, y: 0, zoom: 1 }),
    getTransform: () => ({ x: 0, y: 0, zoom: 1 }),
    viewportInitialized: !1,
  }
  function Gz(e) {
    function t(r, o) {
      return new Promise((i) => {
        e.d3Selection && e.d3Zoom
          ? e.d3Zoom.interpolate(o?.interpolate === 'linear' ? wr : xo).scaleBy(
              xd(e.d3Selection, o?.duration, o?.ease, () => {
                i(!0)
              }),
              r
            )
          : i(!1)
      })
    }
    function n(r, o, i, a) {
      return new Promise((s) => {
        var l
        const { x: u, y: c } = gS({ x: -r, y: -o }, e.translateExtent),
          d = Wn.translate(-u, -c).scale(i)
        e.d3Selection && e.d3Zoom
          ? (l = e.d3Zoom) == null ||
            l.interpolate(a?.interpolate === 'linear' ? wr : xo).transform(
              xd(e.d3Selection, a?.duration, a?.ease, () => {
                s(!0)
              }),
              d
            )
          : s(!1)
      })
    }
    return X(() =>
      e.d3Zoom && e.d3Selection && e.dimensions.width && e.dimensions.height
        ? {
            viewportInitialized: !0,
            zoomIn: (o) => t(1.2, o),
            zoomOut: (o) => t(1 / 1.2, o),
            zoomTo: (o, i) =>
              new Promise((a) => {
                e.d3Selection && e.d3Zoom
                  ? e.d3Zoom.interpolate(i?.interpolate === 'linear' ? wr : xo).scaleTo(
                      xd(e.d3Selection, i?.duration, i?.ease, () => {
                        a(!0)
                      }),
                      o
                    )
                  : a(!1)
              }),
            setViewport: (o, i) => n(o.x, o.y, o.zoom, i),
            setTransform: (o, i) => n(o.x, o.y, o.zoom, i),
            getViewport: () => ({ x: e.viewport.x, y: e.viewport.y, zoom: e.viewport.zoom }),
            getTransform: () => ({ x: e.viewport.x, y: e.viewport.y, zoom: e.viewport.zoom }),
            fitView: (o = { padding: mo, includeHiddenNodes: !1, duration: 0 }) => {
              var i, a
              const s = []
              for (const f of e.nodes)
                f.dimensions.width &&
                  f.dimensions.height &&
                  (o?.includeHiddenNodes || !f.hidden) &&
                  (!((i = o.nodes) != null && i.length) ||
                    ((a = o.nodes) != null && a.length && o.nodes.includes(f.id))) &&
                  s.push(f)
              if (!s.length) return Promise.resolve(!1)
              const l = wS(s),
                {
                  x: u,
                  y: c,
                  zoom: d,
                } = B0(
                  l,
                  e.dimensions.width,
                  e.dimensions.height,
                  o.minZoom ?? e.minZoom,
                  o.maxZoom ?? e.maxZoom,
                  o.padding ?? mo
                )
              return n(u, c, d, o)
            },
            setCenter: (o, i, a) => {
              const s = typeof a?.zoom < 'u' ? a.zoom : e.maxZoom,
                l = e.dimensions.width / 2 - o * s,
                u = e.dimensions.height / 2 - i * s
              return n(l, u, s, a)
            },
            fitBounds: (o, i = { padding: mo }) => {
              const {
                x: a,
                y: s,
                zoom: l,
              } = B0(
                o,
                e.dimensions.width,
                e.dimensions.height,
                e.minZoom,
                e.maxZoom,
                i.padding ?? mo
              )
              return n(a, s, l, i)
            },
            project: (o) => qr(o, e.viewport, e.snapToGrid, e.snapGrid),
            screenToFlowCoordinate: (o) => {
              if (e.vueFlowRef) {
                const { x: i, y: a } = e.vueFlowRef.getBoundingClientRect(),
                  s = { x: o.x - i, y: o.y - a }
                return qr(s, e.viewport, e.snapToGrid, e.snapGrid)
              }
              return { x: 0, y: 0 }
            },
            flowToScreenCoordinate: (o) => {
              if (e.vueFlowRef) {
                const { x: i, y: a } = e.vueFlowRef.getBoundingClientRect(),
                  s = { x: o.x + i, y: o.y + a }
                return Br(s, e.viewport)
              }
              return { x: 0, y: 0 }
            },
          }
        : Vz
    )
  }
  function xd(e, t = 0, n = jz, r = () => {}) {
    const o = typeof t == 'number' && t > 0
    return (o || r(), o ? e.transition().duration(t).ease(n).on('end', r) : e)
  }
  function Wz(e, t, n) {
    const r = d_(!0)
    return (
      r.run(() => {
        const o = () => {
            r.run(() => {
              let m,
                v,
                b = !!(n.nodes.value.length || n.edges.value.length)
              ;((m = An(
                [
                  e.modelValue,
                  () => {
                    var y, p
                    return (p = (y = e.modelValue) == null ? void 0 : y.value) == null
                      ? void 0
                      : p.length
                  },
                ],
                ([y]) => {
                  y &&
                    Array.isArray(y) &&
                    (v?.pause(), n.setElements(y), !v && !b && y.length ? (b = !0) : v?.resume())
                }
              )),
                (v = An(
                  [n.nodes, n.edges, () => n.edges.value.length, () => n.nodes.value.length],
                  ([y, p]) => {
                    var _
                    ;(_ = e.modelValue) != null &&
                      _.value &&
                      Array.isArray(e.modelValue.value) &&
                      (m?.pause(),
                      (e.modelValue.value = [...y, ...p]),
                      Ne(() => {
                        m?.resume()
                      }))
                  },
                  { immediate: b }
                )),
                gr(() => {
                  ;(m?.stop(), v?.stop())
                }))
            })
          },
          i = () => {
            r.run(() => {
              let m,
                v,
                b = !!n.nodes.value.length
              ;((m = An(
                [
                  e.nodes,
                  () => {
                    var y, p
                    return (p = (y = e.nodes) == null ? void 0 : y.value) == null
                      ? void 0
                      : p.length
                  },
                ],
                ([y]) => {
                  y &&
                    Array.isArray(y) &&
                    (v?.pause(), n.setNodes(y), !v && !b && y.length ? (b = !0) : v?.resume())
                }
              )),
                (v = An(
                  [n.nodes, () => n.nodes.value.length],
                  ([y]) => {
                    var p
                    ;(p = e.nodes) != null &&
                      p.value &&
                      Array.isArray(e.nodes.value) &&
                      (m?.pause(),
                      (e.nodes.value = [...y]),
                      Ne(() => {
                        m?.resume()
                      }))
                  },
                  { immediate: b }
                )),
                gr(() => {
                  ;(m?.stop(), v?.stop())
                }))
            })
          },
          a = () => {
            r.run(() => {
              let m,
                v,
                b = !!n.edges.value.length
              ;((m = An(
                [
                  e.edges,
                  () => {
                    var y, p
                    return (p = (y = e.edges) == null ? void 0 : y.value) == null
                      ? void 0
                      : p.length
                  },
                ],
                ([y]) => {
                  y &&
                    Array.isArray(y) &&
                    (v?.pause(), n.setEdges(y), !v && !b && y.length ? (b = !0) : v?.resume())
                }
              )),
                (v = An(
                  [n.edges, () => n.edges.value.length],
                  ([y]) => {
                    var p
                    ;(p = e.edges) != null &&
                      p.value &&
                      Array.isArray(e.edges.value) &&
                      (m?.pause(),
                      (e.edges.value = [...y]),
                      Ne(() => {
                        m?.resume()
                      }))
                  },
                  { immediate: b }
                )),
                gr(() => {
                  ;(m?.stop(), v?.stop())
                }))
            })
          },
          s = () => {
            r.run(() => {
              me(
                () => t.maxZoom,
                () => {
                  t.maxZoom && De(t.maxZoom) && n.setMaxZoom(t.maxZoom)
                },
                { immediate: !0 }
              )
            })
          },
          l = () => {
            r.run(() => {
              me(
                () => t.minZoom,
                () => {
                  t.minZoom && De(t.minZoom) && n.setMinZoom(t.minZoom)
                },
                { immediate: !0 }
              )
            })
          },
          u = () => {
            r.run(() => {
              me(
                () => t.translateExtent,
                () => {
                  t.translateExtent &&
                    De(t.translateExtent) &&
                    n.setTranslateExtent(t.translateExtent)
                },
                { immediate: !0 }
              )
            })
          },
          c = () => {
            r.run(() => {
              me(
                () => t.nodeExtent,
                () => {
                  t.nodeExtent && De(t.nodeExtent) && n.setNodeExtent(t.nodeExtent)
                },
                { immediate: !0 }
              )
            })
          },
          d = () => {
            r.run(() => {
              me(
                () => t.applyDefault,
                () => {
                  De(t.applyDefault) && (n.applyDefault.value = t.applyDefault)
                },
                { immediate: !0 }
              )
            })
          },
          f = () => {
            r.run(() => {
              const m = async (v) => {
                let b = v
                ;(typeof t.autoConnect == 'function' && (b = await t.autoConnect(v)),
                  b !== !1 && n.addEdges([b]))
              }
              ;(me(
                () => t.autoConnect,
                () => {
                  De(t.autoConnect) && (n.autoConnect.value = t.autoConnect)
                },
                { immediate: !0 }
              ),
                me(
                  n.autoConnect,
                  (v, b, y) => {
                    ;(v ? n.onConnect(m) : n.hooks.value.connect.off(m),
                      y(() => {
                        n.hooks.value.connect.off(m)
                      }))
                  },
                  { immediate: !0 }
                ))
            })
          },
          h = () => {
            const m = [
              'id',
              'modelValue',
              'translateExtent',
              'nodeExtent',
              'edges',
              'nodes',
              'maxZoom',
              'minZoom',
              'applyDefault',
              'autoConnect',
            ]
            for (const v of Object.keys(t)) {
              const b = v
              if (!m.includes(b)) {
                const y = Oe(() => t[b]),
                  p = n[b]
                ei(p) &&
                  r.run(() => {
                    me(
                      y,
                      (_) => {
                        De(_) && (p.value = _)
                      },
                      { immediate: !0 }
                    )
                  })
              }
            }
          }
        ;(() => {
          ;(o(), i(), a(), l(), s(), u(), c(), d(), f(), h())
        })()
      }),
      () => r.stop()
    )
  }
  function Uz() {
    return {
      edgesChange: se(),
      nodesChange: se(),
      nodeDoubleClick: se(),
      nodeClick: se(),
      nodeMouseEnter: se(),
      nodeMouseMove: se(),
      nodeMouseLeave: se(),
      nodeContextMenu: se(),
      nodeDragStart: se(),
      nodeDrag: se(),
      nodeDragStop: se(),
      nodesInitialized: se(),
      miniMapNodeClick: se(),
      miniMapNodeDoubleClick: se(),
      miniMapNodeMouseEnter: se(),
      miniMapNodeMouseMove: se(),
      miniMapNodeMouseLeave: se(),
      connect: se(),
      connectStart: se(),
      connectEnd: se(),
      clickConnectStart: se(),
      clickConnectEnd: se(),
      paneReady: se(),
      init: se(),
      move: se(),
      moveStart: se(),
      moveEnd: se(),
      selectionDragStart: se(),
      selectionDrag: se(),
      selectionDragStop: se(),
      selectionContextMenu: se(),
      selectionStart: se(),
      selectionEnd: se(),
      viewportChangeStart: se(),
      viewportChange: se(),
      viewportChangeEnd: se(),
      paneScroll: se(),
      paneClick: se(),
      paneContextMenu: se(),
      paneMouseEnter: se(),
      paneMouseMove: se(),
      paneMouseLeave: se(),
      edgeContextMenu: se(),
      edgeMouseEnter: se(),
      edgeMouseMove: se(),
      edgeMouseLeave: se(),
      edgeDoubleClick: se(),
      edgeClick: se(),
      edgeUpdateStart: se(),
      edgeUpdate: se(),
      edgeUpdateEnd: se(),
      updateNodeInternals: se(),
      error: se((e) => Zr(e.message)),
    }
  }
  function Yz(e, t) {
    const n = Qe()
    Tx(() => {
      for (const [o, i] of Object.entries(t.value)) {
        const a = (s) => {
          e(o, s)
        }
        ;(i.setEmitter(a),
          Ar(i.removeEmitter),
          i.setHasEmitListeners(() => r(o)),
          Ar(i.removeHasEmitListeners))
      }
    })
    function r(o) {
      var i
      const a = Xz(o)
      return !!((i = n?.vnode.props) == null ? void 0 : i[a])
    }
  }
  function Xz(e) {
    const [t, ...n] = e.split(':')
    return `on${t.replace(/(?:^|-)(\w)/g, (o, i) => i.toUpperCase())}${n.length ? `:${n.join(':')}` : ''}`
  }
  function BS() {
    return {
      vueFlowRef: null,
      viewportRef: null,
      nodes: [],
      edges: [],
      connectionLookup: new Map(),
      nodeTypes: {},
      edgeTypes: {},
      initialized: !1,
      dimensions: { width: 0, height: 0 },
      viewport: { x: 0, y: 0, zoom: 1 },
      d3Zoom: null,
      d3Selection: null,
      d3ZoomHandler: null,
      minZoom: 0.5,
      maxZoom: 2,
      translateExtent: [
        [Number.NEGATIVE_INFINITY, Number.NEGATIVE_INFINITY],
        [Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY],
      ],
      nodeExtent: [
        [Number.NEGATIVE_INFINITY, Number.NEGATIVE_INFINITY],
        [Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY],
      ],
      selectionMode: ih.Full,
      paneDragging: !1,
      preventScrolling: !0,
      zoomOnScroll: !0,
      zoomOnPinch: !0,
      zoomOnDoubleClick: !0,
      panOnScroll: !1,
      panOnScrollSpeed: 0.5,
      panOnScrollMode: Sr.Free,
      paneClickDistance: 0,
      panOnDrag: !0,
      edgeUpdaterRadius: 10,
      onlyRenderVisibleElements: !1,
      defaultViewport: { x: 0, y: 0, zoom: 1 },
      nodesSelectionActive: !1,
      userSelectionActive: !1,
      userSelectionRect: null,
      defaultMarkerColor: '#b1b1b7',
      connectionLineStyle: {},
      connectionLineType: null,
      connectionLineOptions: { type: cn.Bezier, style: {} },
      connectionMode: Zt.Loose,
      connectionStartHandle: null,
      connectionEndHandle: null,
      connectionClickStartHandle: null,
      connectionPosition: { x: Number.NaN, y: Number.NaN },
      connectionRadius: 20,
      connectOnClick: !0,
      connectionStatus: null,
      isValidConnection: null,
      snapGrid: [15, 15],
      snapToGrid: !1,
      edgesUpdatable: !1,
      edgesFocusable: !0,
      nodesFocusable: !0,
      nodesConnectable: !0,
      nodesDraggable: !0,
      nodeDragThreshold: 1,
      elementsSelectable: !0,
      selectNodesOnDrag: !0,
      multiSelectionActive: !1,
      selectionKeyCode: 'Shift',
      multiSelectionKeyCode: Xo() ? 'Meta' : 'Control',
      zoomActivationKeyCode: Xo() ? 'Meta' : 'Control',
      deleteKeyCode: 'Backspace',
      panActivationKeyCode: 'Space',
      hooks: Uz(),
      applyDefault: !0,
      autoConnect: !1,
      fitViewOnInit: !1,
      fitViewOnInitDone: !1,
      noDragClassName: 'nodrag',
      noWheelClassName: 'nowheel',
      noPanClassName: 'nopan',
      defaultEdgeOptions: void 0,
      elevateEdgesOnSelect: !1,
      elevateNodesOnSelect: !0,
      autoPanOnNodeDrag: !0,
      autoPanOnConnect: !0,
      autoPanSpeed: 15,
      disableKeyboardA11y: !1,
      ariaLiveMessage: '',
    }
  }
  const Kz = [
    'id',
    'vueFlowRef',
    'viewportRef',
    'initialized',
    'modelValue',
    'nodes',
    'edges',
    'maxZoom',
    'minZoom',
    'translateExtent',
    'hooks',
    'defaultEdgeOptions',
  ]
  function Zz(e, t, n) {
    const r = Gz(e),
      o = (M) => {
        const O = M ?? []
        e.hooks.updateNodeInternals.trigger(O)
      },
      i = (M) => dz(M, e.nodes, e.edges),
      a = (M) => cz(M, e.nodes, e.edges),
      s = (M) => xS(M, e.edges),
      l = ({ id: M, type: O, nodeId: q }) => {
        var I
        const W = M ? `-${O}-${M}` : `-${O}`
        return Array.from(
          ((I = e.connectionLookup.get(`${q}${W}`)) == null ? void 0 : I.values()) ?? []
        )
      },
      u = (M) => {
        if (M) return t.value.get(M)
      },
      c = (M) => {
        if (M) return n.value.get(M)
      },
      d = (M, O, q) => {
        var I, W
        const ae = []
        for (const fe of M) {
          const le = { id: fe.id, type: 'position', dragging: q, from: fe.from }
          if (O && ((le.position = fe.position), fe.parentNode)) {
            const ue = u(fe.parentNode)
            le.position = {
              x: le.position.x - (((I = ue?.computedPosition) == null ? void 0 : I.x) ?? 0),
              y: le.position.y - (((W = ue?.computedPosition) == null ? void 0 : W.y) ?? 0),
            }
          }
          ae.push(le)
        }
        ae?.length && e.hooks.nodesChange.trigger(ae)
      },
      f = (M) => {
        if (!e.vueFlowRef) return
        const O = e.vueFlowRef.querySelector('.vue-flow__transformationpane')
        if (!O) return
        const q = window.getComputedStyle(O),
          { m22: I } = new window.DOMMatrixReadOnly(q.transform),
          W = []
        for (const ae of M) {
          const fe = ae,
            le = u(fe.id)
          if (le) {
            const ue = Pi(fe.nodeElement)
            if (
              !!(
                ue.width &&
                ue.height &&
                (le.dimensions.width !== ue.width ||
                  le.dimensions.height !== ue.height ||
                  fe.forceUpdate)
              )
            ) {
              const Se = fe.nodeElement.getBoundingClientRect()
              ;((le.dimensions = ue),
                (le.handleBounds.source = Y0('source', fe.nodeElement, Se, I, le.id)),
                (le.handleBounds.target = Y0('target', fe.nodeElement, Se, I, le.id)),
                W.push({ id: le.id, type: 'dimensions', dimensions: ue }))
            }
          }
        }
        ;(!e.fitViewOnInitDone &&
          e.fitViewOnInit &&
          r.value.fitView().then(() => {
            e.fitViewOnInitDone = !0
          }),
          W.length && e.hooks.nodesChange.trigger(W))
      },
      h = (M, O) => {
        const q = new Set(),
          I = new Set()
        for (const fe of M) mn(fe) ? q.add(fe.id) : Jt(fe) && I.add(fe.id)
        const W = Yt(t.value, q, !0),
          ae = Yt(n.value, I)
        if (e.multiSelectionActive) {
          for (const fe of q) W.push(Ut(fe, O))
          for (const fe of I) ae.push(Ut(fe, O))
        }
        ;(W.length && e.hooks.nodesChange.trigger(W), ae.length && e.hooks.edgesChange.trigger(ae))
      },
      g = (M) => {
        if (e.multiSelectionActive) {
          const O = M.map((q) => Ut(q.id, !0))
          e.hooks.nodesChange.trigger(O)
          return
        }
        ;(e.hooks.nodesChange.trigger(Yt(t.value, new Set(M.map((O) => O.id)), !0)),
          e.hooks.edgesChange.trigger(Yt(n.value)))
      },
      m = (M) => {
        if (e.multiSelectionActive) {
          const O = M.map((q) => Ut(q.id, !0))
          e.hooks.edgesChange.trigger(O)
          return
        }
        ;(e.hooks.edgesChange.trigger(Yt(n.value, new Set(M.map((O) => O.id)))),
          e.hooks.nodesChange.trigger(Yt(t.value, new Set(), !0)))
      },
      v = (M) => {
        h(M, !0)
      },
      b = (M) => {
        const q = (M || e.nodes).map((I) => ((I.selected = !1), Ut(I.id, !1)))
        e.hooks.nodesChange.trigger(q)
      },
      y = (M) => {
        const q = (M || e.edges).map((I) => ((I.selected = !1), Ut(I.id, !1)))
        e.hooks.edgesChange.trigger(q)
      },
      p = (M) => {
        if (!M || !M.length) return h([], !1)
        const O = M.reduce(
          (q, I) => {
            const W = Ut(I.id, !1)
            return (mn(I) ? q.nodes.push(W) : q.edges.push(W), q)
          },
          { nodes: [], edges: [] }
        )
        ;(O.nodes.length && e.hooks.nodesChange.trigger(O.nodes),
          O.edges.length && e.hooks.edgesChange.trigger(O.edges))
      },
      _ = (M) => {
        var O
        ;((O = e.d3Zoom) == null || O.scaleExtent([M, e.maxZoom]), (e.minZoom = M))
      },
      x = (M) => {
        var O
        ;((O = e.d3Zoom) == null || O.scaleExtent([e.minZoom, M]), (e.maxZoom = M))
      },
      S = (M) => {
        var O
        ;((O = e.d3Zoom) == null || O.translateExtent(M), (e.translateExtent = M))
      },
      w = (M) => {
        ;((e.nodeExtent = M), o())
      },
      T = (M) => {
        var O
        ;(O = e.d3Zoom) == null || O.clickDistance(M)
      },
      A = (M) => {
        ;((e.nodesDraggable = M), (e.nodesConnectable = M), (e.elementsSelectable = M))
      },
      $ = (M) => {
        const O = M instanceof Function ? M(e.nodes) : M
        ;(!e.initialized && !O.length) || (e.nodes = X0(O, u, e.hooks.error.trigger))
      },
      P = (M) => {
        const O = M instanceof Function ? M(e.edges) : M
        if (!e.initialized && !O.length) return
        const q = Sd(
          O,
          e.isValidConnection,
          u,
          c,
          e.hooks.error.trigger,
          e.defaultEdgeOptions,
          e.nodes,
          e.edges
        )
        ;(wd(e.connectionLookup, n.value, q), (e.edges = q))
      },
      E = (M) => {
        const O = M instanceof Function ? M([...e.nodes, ...e.edges]) : M
        ;(!e.initialized && !O.length) || ($(O.filter(mn)), P(O.filter(Jt)))
      },
      z = (M) => {
        let O = M instanceof Function ? M(e.nodes) : M
        O = Array.isArray(O) ? O : [O]
        const q = X0(O, u, e.hooks.error.trigger),
          I = []
        for (const W of q) I.push(F0(W))
        I.length && e.hooks.nodesChange.trigger(I)
      },
      C = (M) => {
        let O = M instanceof Function ? M(e.edges) : M
        O = Array.isArray(O) ? O : [O]
        const q = Sd(
            O,
            e.isValidConnection,
            u,
            c,
            e.hooks.error.trigger,
            e.defaultEdgeOptions,
            e.nodes,
            e.edges
          ),
          I = []
        for (const W of q) I.push(F0(W))
        I.length && e.hooks.edgesChange.trigger(I)
      },
      R = (M, O = !0, q = !1) => {
        const I = M instanceof Function ? M(e.nodes) : M,
          W = Array.isArray(I) ? I : [I],
          ae = [],
          fe = []
        function le(ge) {
          const Se = s(ge)
          for (const $e of Se)
            (!De($e.deletable) || $e.deletable) &&
              fe.push(H0($e.id, $e.source, $e.target, $e.sourceHandle, $e.targetHandle))
        }
        function ue(ge) {
          const Se = []
          for (const $e of e.nodes) $e.parentNode === ge && Se.push($e)
          if (Se.length) {
            for (const $e of Se) ae.push(k0($e.id))
            O && le(Se)
            for (const $e of Se) ue($e.id)
          }
        }
        for (const ge of W) {
          const Se = typeof ge == 'string' ? u(ge) : ge
          Se &&
            ((De(Se.deletable) && !Se.deletable) ||
              (ae.push(k0(Se.id)), O && le([Se]), q && ue(Se.id)))
        }
        ;(fe.length && e.hooks.edgesChange.trigger(fe),
          ae.length && e.hooks.nodesChange.trigger(ae))
      },
      N = (M) => {
        const O = M instanceof Function ? M(e.edges) : M,
          q = Array.isArray(O) ? O : [O],
          I = []
        for (const W of q) {
          const ae = typeof W == 'string' ? c(W) : W
          ae &&
            ((De(ae.deletable) && !ae.deletable) ||
              I.push(
                H0(
                  typeof W == 'string' ? W : W.id,
                  ae.source,
                  ae.target,
                  ae.sourceHandle,
                  ae.targetHandle
                )
              ))
        }
        e.hooks.edgesChange.trigger(I)
      },
      j = (M, O, q = !0) => {
        const I = c(M.id)
        if (!I) return !1
        const W = e.edges.indexOf(I),
          ae = Mz(M, O, I, q, e.hooks.error.trigger)
        if (ae) {
          const [fe] = Sd(
            [ae],
            e.isValidConnection,
            u,
            c,
            e.hooks.error.trigger,
            e.defaultEdgeOptions,
            e.nodes,
            e.edges
          )
          return (
            (e.edges = e.edges.map((le, ue) => (ue === W ? fe : le))),
            wd(e.connectionLookup, n.value, [fe]),
            fe
          )
        }
        return !1
      },
      V = (M, O, q = { replace: !1 }) => {
        const I = c(M)
        if (!I) return
        const W = typeof O == 'function' ? O(I) : O
        I.data = q.replace ? W : { ...I.data, ...W }
      },
      H = (M) => L0(M, e.nodes),
      G = (M) => {
        const O = L0(M, e.edges)
        return (wd(e.connectionLookup, n.value, O), O)
      },
      Y = (M, O, q = { replace: !1 }) => {
        const I = u(M)
        if (!I) return
        const W = typeof O == 'function' ? O(I) : O
        q.replace ? e.nodes.splice(e.nodes.indexOf(I), 1, W) : Object.assign(I, W)
      },
      Z = (M, O, q = { replace: !1 }) => {
        const I = u(M)
        if (!I) return
        const W = typeof O == 'function' ? O(I) : O
        I.data = q.replace ? W : { ...I.data, ...W }
      },
      ne = (M, O, q = !1) => {
        ;(q ? (e.connectionClickStartHandle = M) : (e.connectionStartHandle = M),
          (e.connectionEndHandle = null),
          (e.connectionStatus = null),
          O && (e.connectionPosition = O))
      },
      B = (M, O = null, q = null) => {
        e.connectionStartHandle &&
          ((e.connectionPosition = M), (e.connectionEndHandle = O), (e.connectionStatus = q))
      },
      L = (M, O) => {
        ;((e.connectionPosition = { x: Number.NaN, y: Number.NaN }),
          (e.connectionEndHandle = null),
          (e.connectionStatus = null),
          O ? (e.connectionClickStartHandle = null) : (e.connectionStartHandle = null))
      },
      k = (M) => {
        const O = lz(M),
          q = O ? null : pr(M) ? M : u(M.id)
        return !O && !q ? [null, null, O] : [O ? M : Uo(q), q, O]
      },
      U = (M, O = !0, q = e.nodes) => {
        const [I, W, ae] = k(M)
        if (!I) return []
        const fe = []
        for (const le of q || e.nodes) {
          if (!ae && (le.id === W.id || !le.computedPosition)) continue
          const ue = Uo(le),
            ge = Yo(ue, I)
          ;((O && ge > 0) ||
            ge >= ue.width * ue.height ||
            ge >= Number(I.width) * Number(I.height)) &&
            fe.push(le)
        }
        return fe
      },
      J = (M, O, q = !0) => {
        const [I] = k(M)
        if (!I) return !1
        const W = Yo(I, O)
        return (q && W > 0) || W >= Number(I.width) * Number(I.height)
      },
      re = (M) => {
        const { viewport: O, dimensions: q, d3Zoom: I, d3Selection: W, translateExtent: ae } = e
        if (!I || !W || (!M.x && !M.y)) return !1
        const fe = Wn.translate(O.x + M.x, O.y + M.y).scale(O.zoom),
          le = [
            [0, 0],
            [q.width, q.height],
          ],
          ue = I.constrain()(fe, le, ae),
          ge = e.viewport.x !== ue.x || e.viewport.y !== ue.y || e.viewport.zoom !== ue.k
        return (I.transform(W, ue), ge)
      },
      ie = (M) => {
        const O = M instanceof Function ? M(e) : M,
          q = [
            'd3Zoom',
            'd3Selection',
            'd3ZoomHandler',
            'viewportRef',
            'vueFlowRef',
            'dimensions',
            'hooks',
          ]
        De(O.defaultEdgeOptions) && (e.defaultEdgeOptions = O.defaultEdgeOptions)
        const I = O.modelValue || O.nodes || O.edges ? [] : void 0
        I &&
          (O.modelValue && I.push(...O.modelValue),
          O.nodes && I.push(...O.nodes),
          O.edges && I.push(...O.edges),
          E(I))
        const W = () => {
          ;(De(O.maxZoom) && x(O.maxZoom),
            De(O.minZoom) && _(O.minZoom),
            De(O.translateExtent) && S(O.translateExtent))
        }
        for (const ae of Object.keys(O)) {
          const fe = ae,
            le = O[fe]
          ![...Kz, ...q].includes(fe) && De(le) && (e[fe] = le)
        }
        ;(Hd(() => e.d3Zoom)
          .not.toBeNull()
          .then(W),
          e.initialized || (e.initialized = !0))
      }
    return {
      updateNodePositions: d,
      updateNodeDimensions: f,
      setElements: E,
      setNodes: $,
      setEdges: P,
      addNodes: z,
      addEdges: C,
      removeNodes: R,
      removeEdges: N,
      findNode: u,
      findEdge: c,
      updateEdge: j,
      updateEdgeData: V,
      updateNode: Y,
      updateNodeData: Z,
      applyEdgeChanges: G,
      applyNodeChanges: H,
      addSelectedElements: v,
      addSelectedNodes: g,
      addSelectedEdges: m,
      setMinZoom: _,
      setMaxZoom: x,
      setTranslateExtent: S,
      setNodeExtent: w,
      setPaneClickDistance: T,
      removeSelectedElements: p,
      removeSelectedNodes: b,
      removeSelectedEdges: y,
      startConnection: ne,
      updateConnection: B,
      endConnection: L,
      setInteractive: A,
      setState: ie,
      getIntersectingNodes: U,
      getIncomers: i,
      getOutgoers: a,
      getConnectedEdges: s,
      getHandleConnections: l,
      isNodeIntersecting: J,
      panBy: re,
      fitView: (M) => r.value.fitView(M),
      zoomIn: (M) => r.value.zoomIn(M),
      zoomOut: (M) => r.value.zoomOut(M),
      zoomTo: (M, O) => r.value.zoomTo(M, O),
      setViewport: (M, O) => r.value.setViewport(M, O),
      setTransform: (M, O) => r.value.setTransform(M, O),
      getViewport: () => r.value.getViewport(),
      getTransform: () => r.value.getTransform(),
      setCenter: (M, O, q) => r.value.setCenter(M, O, q),
      fitBounds: (M, O) => r.value.fitBounds(M, O),
      project: (M) => r.value.project(M),
      screenToFlowCoordinate: (M) => r.value.screenToFlowCoordinate(M),
      flowToScreenCoordinate: (M) => r.value.flowToScreenCoordinate(M),
      toObject: () => {
        const M = [],
          O = []
        for (const q of e.nodes) {
          const {
            computedPosition: I,
            handleBounds: W,
            selected: ae,
            dimensions: fe,
            isParent: le,
            resizing: ue,
            dragging: ge,
            events: Se,
            ...$e
          } = q
          M.push($e)
        }
        for (const q of e.edges) {
          const { selected: I, sourceNode: W, targetNode: ae, events: fe, ...le } = q
          O.push(le)
        }
        return JSON.parse(
          JSON.stringify({
            nodes: M,
            edges: O,
            position: [e.viewport.x, e.viewport.y],
            zoom: e.viewport.zoom,
            viewport: e.viewport,
          })
        )
      },
      fromObject: (M) =>
        new Promise((O) => {
          const { nodes: q, edges: I, position: W, zoom: ae, viewport: fe } = M
          ;(q && $(q), I && P(I))
          const [le, ue] = fe?.x && fe?.y ? [fe.x, fe.y] : (W ?? [null, null])
          if (le && ue) {
            const ge = fe?.zoom || ae || e.viewport.zoom
            return Hd(() => r.value.viewportInitialized)
              .toBe(!0)
              .then(() => {
                r.value.setViewport({ x: le, y: ue, zoom: ge }).then(() => {
                  O(!0)
                })
              })
          } else O(!0)
        }),
      updateNodeInternals: o,
      viewportHelper: r,
      $reset: () => {
        const M = BS()
        if (((e.edges = []), (e.nodes = []), e.d3Zoom && e.d3Selection)) {
          const O = Wn.translate(M.defaultViewport.x ?? 0, M.defaultViewport.y ?? 0).scale(
              Sn(M.defaultViewport.zoom ?? 1, M.minZoom, M.maxZoom)
            ),
            q = e.viewportRef.getBoundingClientRect(),
            I = [
              [0, 0],
              [q.width, q.height],
            ],
            W = e.d3Zoom.constrain()(O, I, M.translateExtent)
          e.d3Zoom.transform(e.d3Selection, W)
        }
        ie(M)
      },
      $destroy: () => {},
    }
  }
  const Jz = ['data-id', 'data-handleid', 'data-nodeid', 'data-handlepos'],
    Qz = { name: 'Handle', compatConfig: { MODE: 3 } },
    Yn = te({
      ...Qz,
      props: {
        id: { default: null },
        type: {},
        position: { default: () => pe.Top },
        isValidConnection: { type: Function },
        connectable: { type: [Boolean, Number, String, Function], default: void 0 },
        connectableStart: { type: Boolean, default: !0 },
        connectableEnd: { type: Boolean, default: !0 },
      },
      setup(e, { expose: t }) {
        const n = $x(e, ['position', 'connectable', 'connectableStart', 'connectableEnd', 'id']),
          r = Oe(() => n.type ?? 'source'),
          o = Oe(() => n.isValidConnection ?? null),
          {
            id: i,
            connectionStartHandle: a,
            connectionClickStartHandle: s,
            connectionEndHandle: l,
            vueFlowRef: u,
            nodesConnectable: c,
            noDragClassName: d,
            noPanClassName: f,
          } = Ae(),
          { id: h, node: g, nodeEl: m, connectedEdges: v } = MS(),
          b = de(),
          y = Oe(() => (typeof e.connectableStart < 'u' ? e.connectableStart : !0)),
          p = Oe(() => (typeof e.connectableEnd < 'u' ? e.connectableEnd : !0)),
          _ = Oe(() => {
            var P, E, z, C, R, N
            return (
              (((P = a.value) == null ? void 0 : P.nodeId) === h &&
                ((E = a.value) == null ? void 0 : E.id) === e.id &&
                ((z = a.value) == null ? void 0 : z.type) === r.value) ||
              (((C = l.value) == null ? void 0 : C.nodeId) === h &&
                ((R = l.value) == null ? void 0 : R.id) === e.id &&
                ((N = l.value) == null ? void 0 : N.type) === r.value)
            )
          }),
          x = Oe(() => {
            var P, E, z
            return (
              ((P = s.value) == null ? void 0 : P.nodeId) === h &&
              ((E = s.value) == null ? void 0 : E.id) === e.id &&
              ((z = s.value) == null ? void 0 : z.type) === r.value
            )
          }),
          { handlePointerDown: S, handleClick: w } = RS({
            nodeId: h,
            handleId: e.id,
            isValidConnection: o,
            type: r,
          }),
          T = X(() =>
            typeof e.connectable == 'string' && e.connectable === 'single'
              ? !v.value.some((P) => {
                  const E = P[`${r.value}Handle`]
                  return P[r.value] !== h ? !1 : E ? E === e.id : !0
                })
              : typeof e.connectable == 'number'
                ? v.value.filter((P) => {
                    const E = P[`${r.value}Handle`]
                    return P[r.value] !== h ? !1 : E ? E === e.id : !0
                  }).length < e.connectable
                : typeof e.connectable == 'function'
                  ? e.connectable(g, v.value)
                  : De(e.connectable)
                    ? e.connectable
                    : c.value
          )
        Me(() => {
          var P
          if (!g.dimensions.width || !g.dimensions.height) return
          const E = (P = g.handleBounds[r.value]) == null ? void 0 : P.find((H) => H.id === e.id)
          if (!u.value || E) return
          const z = u.value.querySelector('.vue-flow__transformationpane')
          if (!m.value || !b.value || !z || !e.id) return
          const C = m.value.getBoundingClientRect(),
            R = b.value.getBoundingClientRect(),
            N = window.getComputedStyle(z),
            { m22: j } = new window.DOMMatrixReadOnly(N.transform),
            V = {
              id: e.id,
              position: e.position,
              x: (R.left - C.left) / j,
              y: (R.top - C.top) / j,
              type: r.value,
              nodeId: h,
              ...Pi(b.value),
            }
          g.handleBounds[r.value] = [...(g.handleBounds[r.value] ?? []), V]
        })
        function A(P) {
          const E = sh(P)
          T.value && y.value && ((E && P.button === 0) || !E) && S(P)
        }
        function $(P) {
          !h || (!s.value && !y.value) || (T.value && w(P))
        }
        return (
          t({ handleClick: w, handlePointerDown: S, onClick: $, onPointerDown: A }),
          (P, E) => (
            ee(),
            ve(
              'div',
              {
                ref_key: 'handle',
                ref: b,
                'data-id': `${K(i)}-${K(h)}-${e.id}-${r.value}`,
                'data-handleid': e.id,
                'data-nodeid': K(h),
                'data-handlepos': P.position,
                class: ct([
                  'vue-flow__handle',
                  [
                    `vue-flow__handle-${P.position}`,
                    `vue-flow__handle-${e.id}`,
                    K(d),
                    K(f),
                    r.value,
                    {
                      connectable: T.value,
                      connecting: x.value,
                      connectablestart: y.value,
                      connectableend: p.value,
                      connectionindicator:
                        T.value && ((y.value && !_.value) || (p.value && _.value)),
                    },
                  ],
                ]),
                onMousedown: A,
                onTouchstartPassive: A,
                onClick: $,
              },
              [bt(P.$slots, 'default', { id: P.id })],
              42,
              Jz
            )
          )
        )
      },
    }),
    Ni = function ({
      sourcePosition: e = pe.Bottom,
      targetPosition: t = pe.Top,
      label: n,
      connectable: r = !0,
      isValidTargetPos: o,
      isValidSourcePos: i,
      data: a,
    }) {
      const s = a.label ?? n
      return [
        Ce(Yn, { type: 'target', position: t, connectable: r, isValidConnection: o }),
        typeof s != 'string' && s ? Ce(s) : Ce(Re, [s]),
        Ce(Yn, { type: 'source', position: e, connectable: r, isValidConnection: i }),
      ]
    }
  Ni.props = [
    'sourcePosition',
    'targetPosition',
    'label',
    'isValidTargetPos',
    'isValidSourcePos',
    'connectable',
    'data',
  ]
  Ni.inheritAttrs = !1
  Ni.compatConfig = { MODE: 3 }
  const eL = Ni,
    Ri = function ({
      targetPosition: e = pe.Top,
      label: t,
      connectable: n = !0,
      isValidTargetPos: r,
      data: o,
    }) {
      const i = o.label ?? t
      return [
        Ce(Yn, { type: 'target', position: e, connectable: n, isValidConnection: r }),
        typeof i != 'string' && i ? Ce(i) : Ce(Re, [i]),
      ]
    }
  Ri.props = ['targetPosition', 'label', 'isValidTargetPos', 'connectable', 'data']
  Ri.inheritAttrs = !1
  Ri.compatConfig = { MODE: 3 }
  const tL = Ri,
    Mi = function ({
      sourcePosition: e = pe.Bottom,
      label: t,
      connectable: n = !0,
      isValidSourcePos: r,
      data: o,
    }) {
      const i = o.label ?? t
      return [
        typeof i != 'string' && i ? Ce(i) : Ce(Re, [i]),
        Ce(Yn, { type: 'source', position: e, connectable: n, isValidConnection: r }),
      ]
    }
  Mi.props = ['sourcePosition', 'label', 'isValidSourcePos', 'connectable', 'data']
  Mi.inheritAttrs = !1
  Mi.compatConfig = { MODE: 3 }
  const nL = Mi,
    rL = ['transform'],
    oL = ['width', 'height', 'x', 'y', 'rx', 'ry'],
    iL = ['y'],
    aL = { name: 'EdgeText', compatConfig: { MODE: 3 } },
    sL = te({
      ...aL,
      props: {
        x: {},
        y: {},
        label: {},
        labelStyle: { default: () => ({}) },
        labelShowBg: { type: Boolean, default: !0 },
        labelBgStyle: { default: () => ({}) },
        labelBgPadding: { default: () => [2, 4] },
        labelBgBorderRadius: { default: 2 },
      },
      setup(e) {
        const t = de({ x: 0, y: 0, width: 0, height: 0 }),
          n = de(null),
          r = X(() => `translate(${e.x - t.value.width / 2} ${e.y - t.value.height / 2})`)
        ;(Me(o), me([() => e.x, () => e.y, n, () => e.label], o))
        function o() {
          if (!n.value) return
          const i = n.value.getBBox()
          ;(i.width !== t.value.width || i.height !== t.value.height) && (t.value = i)
        }
        return (i, a) => (
          ee(),
          ve(
            'g',
            { transform: r.value, class: 'vue-flow__edge-textwrapper' },
            [
              i.labelShowBg
                ? (ee(),
                  ve(
                    'rect',
                    {
                      key: 0,
                      class: 'vue-flow__edge-textbg',
                      width: `${t.value.width + 2 * i.labelBgPadding[0]}px`,
                      height: `${t.value.height + 2 * i.labelBgPadding[1]}px`,
                      x: -i.labelBgPadding[0],
                      y: -i.labelBgPadding[1],
                      style: Ct(i.labelBgStyle),
                      rx: i.labelBgBorderRadius,
                      ry: i.labelBgBorderRadius,
                    },
                    null,
                    12,
                    oL
                  ))
                : Pe('', !0),
              he(
                'text',
                h_(i.$attrs, {
                  ref_key: 'el',
                  ref: n,
                  class: 'vue-flow__edge-text',
                  y: t.value.height / 2,
                  dy: '0.3em',
                  style: i.labelStyle,
                }),
                [
                  bt(i.$slots, 'default', {}, () => [
                    typeof i.label != 'string'
                      ? (ee(), ke(Nx(i.label), { key: 0 }))
                      : (ee(), ve(Re, { key: 1 }, [Xt(ze(i.label), 1)], 64)),
                  ]),
                ],
                16,
                iL
              ),
            ],
            8,
            rL
          )
        )
      },
    }),
    lL = ['id', 'd', 'marker-end', 'marker-start'],
    uL = ['d', 'stroke-width'],
    cL = { name: 'BaseEdge', inheritAttrs: !1, compatConfig: { MODE: 3 } },
    Di = te({
      ...cL,
      props: {
        id: {},
        labelX: {},
        labelY: {},
        path: {},
        label: {},
        markerStart: {},
        markerEnd: {},
        interactionWidth: { default: 20 },
        labelStyle: {},
        labelShowBg: { type: Boolean },
        labelBgStyle: {},
        labelBgPadding: {},
        labelBgBorderRadius: {},
      },
      setup(e, { expose: t }) {
        const n = de(null),
          r = de(null),
          o = de(null),
          i = Ax()
        return (
          t({ pathEl: n, interactionEl: r, labelEl: o }),
          (a, s) => (
            ee(),
            ve(
              Re,
              null,
              [
                he(
                  'path',
                  h_(K(i), {
                    id: a.id,
                    ref_key: 'pathEl',
                    ref: n,
                    d: a.path,
                    class: 'vue-flow__edge-path',
                    'marker-end': a.markerEnd,
                    'marker-start': a.markerStart,
                  }),
                  null,
                  16,
                  lL
                ),
                a.interactionWidth
                  ? (ee(),
                    ve(
                      'path',
                      {
                        key: 0,
                        ref_key: 'interactionEl',
                        ref: r,
                        fill: 'none',
                        d: a.path,
                        'stroke-width': a.interactionWidth,
                        'stroke-opacity': 0,
                        class: 'vue-flow__edge-interaction',
                      },
                      null,
                      8,
                      uL
                    ))
                  : Pe('', !0),
                a.label && a.labelX && a.labelY
                  ? (ee(),
                    ke(
                      sL,
                      {
                        key: 1,
                        ref_key: 'labelEl',
                        ref: o,
                        x: a.labelX,
                        y: a.labelY,
                        label: a.label,
                        'label-show-bg': a.labelShowBg,
                        'label-bg-style': a.labelBgStyle,
                        'label-bg-padding': a.labelBgPadding,
                        'label-bg-border-radius': a.labelBgBorderRadius,
                        'label-style': a.labelStyle,
                      },
                      null,
                      8,
                      [
                        'x',
                        'y',
                        'label',
                        'label-show-bg',
                        'label-bg-style',
                        'label-bg-padding',
                        'label-bg-border-radius',
                        'label-style',
                      ]
                    ))
                  : Pe('', !0),
              ],
              64
            )
          )
        )
      },
    })
  function qS({ sourceX: e, sourceY: t, targetX: n, targetY: r }) {
    const o = Math.abs(n - e) / 2,
      i = n < e ? n + o : n - o,
      a = Math.abs(r - t) / 2,
      s = r < t ? r + a : r - a
    return [i, s, o, a]
  }
  function zS({
    sourceX: e,
    sourceY: t,
    targetX: n,
    targetY: r,
    sourceControlX: o,
    sourceControlY: i,
    targetControlX: a,
    targetControlY: s,
  }) {
    const l = e * 0.125 + o * 0.375 + a * 0.375 + n * 0.125,
      u = t * 0.125 + i * 0.375 + s * 0.375 + r * 0.125,
      c = Math.abs(l - e),
      d = Math.abs(u - t)
    return [l, u, c, d]
  }
  function yo(e, t) {
    return e >= 0 ? 0.5 * e : t * 25 * Math.sqrt(-e)
  }
  function Q0({ pos: e, x1: t, y1: n, x2: r, y2: o, c: i }) {
    let a, s
    switch (e) {
      case pe.Left:
        ;((a = t - yo(t - r, i)), (s = n))
        break
      case pe.Right:
        ;((a = t + yo(r - t, i)), (s = n))
        break
      case pe.Top:
        ;((a = t), (s = n - yo(n - o, i)))
        break
      case pe.Bottom:
        ;((a = t), (s = n + yo(o - n, i)))
        break
    }
    return [a, s]
  }
  function LS(e) {
    const {
        sourceX: t,
        sourceY: n,
        sourcePosition: r = pe.Bottom,
        targetX: o,
        targetY: i,
        targetPosition: a = pe.Top,
        curvature: s = 0.25,
      } = e,
      [l, u] = Q0({ pos: r, x1: t, y1: n, x2: o, y2: i, c: s }),
      [c, d] = Q0({ pos: a, x1: o, y1: i, x2: t, y2: n, c: s }),
      [f, h, g, m] = zS({
        sourceX: t,
        sourceY: n,
        targetX: o,
        targetY: i,
        sourceControlX: l,
        sourceControlY: u,
        targetControlX: c,
        targetControlY: d,
      })
    return [`M${t},${n} C${l},${u} ${c},${d} ${o},${i}`, f, h, g, m]
  }
  function e_({ pos: e, x1: t, y1: n, x2: r, y2: o }) {
    let i, a
    switch (e) {
      case pe.Left:
      case pe.Right:
        ;((i = 0.5 * (t + r)), (a = n))
        break
      case pe.Top:
      case pe.Bottom:
        ;((i = t), (a = 0.5 * (n + o)))
        break
    }
    return [i, a]
  }
  function FS(e) {
    const {
        sourceX: t,
        sourceY: n,
        sourcePosition: r = pe.Bottom,
        targetX: o,
        targetY: i,
        targetPosition: a = pe.Top,
      } = e,
      [s, l] = e_({ pos: r, x1: t, y1: n, x2: o, y2: i }),
      [u, c] = e_({ pos: a, x1: o, y1: i, x2: t, y2: n }),
      [d, f, h, g] = zS({
        sourceX: t,
        sourceY: n,
        targetX: o,
        targetY: i,
        sourceControlX: s,
        sourceControlY: l,
        targetControlX: u,
        targetControlY: c,
      })
    return [`M${t},${n} C${s},${l} ${u},${c} ${o},${i}`, d, f, h, g]
  }
  const t_ = {
    [pe.Left]: { x: -1, y: 0 },
    [pe.Right]: { x: 1, y: 0 },
    [pe.Top]: { x: 0, y: -1 },
    [pe.Bottom]: { x: 0, y: 1 },
  }
  function dL({ source: e, sourcePosition: t = pe.Bottom, target: n }) {
    return t === pe.Left || t === pe.Right
      ? e.x < n.x
        ? { x: 1, y: 0 }
        : { x: -1, y: 0 }
      : e.y < n.y
        ? { x: 0, y: 1 }
        : { x: 0, y: -1 }
  }
  function n_(e, t) {
    return Math.sqrt((t.x - e.x) ** 2 + (t.y - e.y) ** 2)
  }
  function fL({
    source: e,
    sourcePosition: t = pe.Bottom,
    target: n,
    targetPosition: r = pe.Top,
    center: o,
    offset: i,
  }) {
    const a = t_[t],
      s = t_[r],
      l = { x: e.x + a.x * i, y: e.y + a.y * i },
      u = { x: n.x + s.x * i, y: n.y + s.y * i },
      c = dL({ source: l, sourcePosition: t, target: u }),
      d = c.x !== 0 ? 'x' : 'y',
      f = c[d]
    let h, g, m
    const v = { x: 0, y: 0 },
      b = { x: 0, y: 0 },
      [y, p, _, x] = qS({ sourceX: e.x, sourceY: e.y, targetX: n.x, targetY: n.y })
    if (a[d] * s[d] === -1) {
      ;((g = o.x ?? y), (m = o.y ?? p))
      const w = [
          { x: g, y: l.y },
          { x: g, y: u.y },
        ],
        T = [
          { x: l.x, y: m },
          { x: u.x, y: m },
        ]
      a[d] === f ? (h = d === 'x' ? w : T) : (h = d === 'x' ? T : w)
    } else {
      const w = [{ x: l.x, y: u.y }],
        T = [{ x: u.x, y: l.y }]
      if ((d === 'x' ? (h = a.x === f ? T : w) : (h = a.y === f ? w : T), t === r)) {
        const z = Math.abs(e[d] - n[d])
        if (z <= i) {
          const C = Math.min(i - 1, i - z)
          a[d] === f ? (v[d] = (l[d] > e[d] ? -1 : 1) * C) : (b[d] = (u[d] > n[d] ? -1 : 1) * C)
        }
      }
      if (t !== r) {
        const z = d === 'x' ? 'y' : 'x',
          C = a[d] === s[z],
          R = l[z] > u[z],
          N = l[z] < u[z]
        ;((a[d] === 1 && ((!C && R) || (C && N))) || (a[d] !== 1 && ((!C && N) || (C && R)))) &&
          (h = d === 'x' ? w : T)
      }
      const A = { x: l.x + v.x, y: l.y + v.y },
        $ = { x: u.x + b.x, y: u.y + b.y },
        P = Math.max(Math.abs(A.x - h[0].x), Math.abs($.x - h[0].x)),
        E = Math.max(Math.abs(A.y - h[0].y), Math.abs($.y - h[0].y))
      P >= E ? ((g = (A.x + $.x) / 2), (m = h[0].y)) : ((g = h[0].x), (m = (A.y + $.y) / 2))
    }
    return [
      [e, { x: l.x + v.x, y: l.y + v.y }, ...h, { x: u.x + b.x, y: u.y + b.y }, n],
      g,
      m,
      _,
      x,
    ]
  }
  function hL(e, t, n, r) {
    const o = Math.min(n_(e, t) / 2, n_(t, n) / 2, r),
      { x: i, y: a } = t
    if ((e.x === i && i === n.x) || (e.y === a && a === n.y)) return `L${i} ${a}`
    if (e.y === a) {
      const u = e.x < n.x ? -1 : 1,
        c = e.y < n.y ? 1 : -1
      return `L ${i + o * u},${a}Q ${i},${a} ${i},${a + o * c}`
    }
    const s = e.x < n.x ? 1 : -1,
      l = e.y < n.y ? -1 : 1
    return `L ${i},${a + o * l}Q ${i},${a} ${i + o * s},${a}`
  }
  function ef(e) {
    const {
        sourceX: t,
        sourceY: n,
        sourcePosition: r = pe.Bottom,
        targetX: o,
        targetY: i,
        targetPosition: a = pe.Top,
        borderRadius: s = 5,
        centerX: l,
        centerY: u,
        offset: c = 20,
      } = e,
      [d, f, h, g, m] = fL({
        source: { x: t, y: n },
        sourcePosition: r,
        target: { x: o, y: i },
        targetPosition: a,
        center: { x: l, y: u },
        offset: c,
      })
    return [
      d.reduce((b, y, p) => {
        let _
        return (
          p > 0 && p < d.length - 1
            ? (_ = hL(d[p - 1], y, d[p + 1], s))
            : (_ = `${p === 0 ? 'M' : 'L'}${y.x} ${y.y}`),
          (b += _),
          b
        )
      }, ''),
      f,
      h,
      g,
      m,
    ]
  }
  function pL(e) {
    const { sourceX: t, sourceY: n, targetX: r, targetY: o } = e,
      [i, a, s, l] = qS({ sourceX: t, sourceY: n, targetX: r, targetY: o })
    return [`M ${t},${n}L ${r},${o}`, i, a, s, l]
  }
  const vL = te({
      name: 'StraightEdge',
      props: [
        'label',
        'labelStyle',
        'labelShowBg',
        'labelBgStyle',
        'labelBgPadding',
        'labelBgBorderRadius',
        'sourceY',
        'sourceX',
        'targetX',
        'targetY',
        'markerEnd',
        'markerStart',
        'interactionWidth',
      ],
      compatConfig: { MODE: 3 },
      setup(e, { attrs: t }) {
        return () => {
          const [n, r, o] = pL(e)
          return Ce(Di, { path: n, labelX: r, labelY: o, ...t, ...e })
        }
      },
    }),
    gL = vL,
    mL = te({
      name: 'SmoothStepEdge',
      props: [
        'sourcePosition',
        'targetPosition',
        'label',
        'labelStyle',
        'labelShowBg',
        'labelBgStyle',
        'labelBgPadding',
        'labelBgBorderRadius',
        'sourceY',
        'sourceX',
        'targetX',
        'targetY',
        'borderRadius',
        'markerEnd',
        'markerStart',
        'interactionWidth',
        'offset',
      ],
      compatConfig: { MODE: 3 },
      setup(e, { attrs: t }) {
        return () => {
          const [n, r, o] = ef({
            ...e,
            sourcePosition: e.sourcePosition ?? pe.Bottom,
            targetPosition: e.targetPosition ?? pe.Top,
          })
          return Ce(Di, { path: n, labelX: r, labelY: o, ...t, ...e })
        }
      },
    }),
    kS = mL,
    yL = te({
      name: 'StepEdge',
      props: [
        'sourcePosition',
        'targetPosition',
        'label',
        'labelStyle',
        'labelShowBg',
        'labelBgStyle',
        'labelBgPadding',
        'labelBgBorderRadius',
        'sourceY',
        'sourceX',
        'targetX',
        'targetY',
        'markerEnd',
        'markerStart',
        'interactionWidth',
      ],
      setup(e, { attrs: t }) {
        return () => Ce(kS, { ...e, ...t, borderRadius: 0 })
      },
    }),
    bL = yL,
    _L = te({
      name: 'BezierEdge',
      props: [
        'sourcePosition',
        'targetPosition',
        'label',
        'labelStyle',
        'labelShowBg',
        'labelBgStyle',
        'labelBgPadding',
        'labelBgBorderRadius',
        'sourceY',
        'sourceX',
        'targetX',
        'targetY',
        'curvature',
        'markerEnd',
        'markerStart',
        'interactionWidth',
      ],
      compatConfig: { MODE: 3 },
      setup(e, { attrs: t }) {
        return () => {
          const [n, r, o] = LS({
            ...e,
            sourcePosition: e.sourcePosition ?? pe.Bottom,
            targetPosition: e.targetPosition ?? pe.Top,
          })
          return Ce(Di, { path: n, labelX: r, labelY: o, ...t, ...e })
        }
      },
    }),
    wL = _L,
    SL = te({
      name: 'SimpleBezierEdge',
      props: [
        'sourcePosition',
        'targetPosition',
        'label',
        'labelStyle',
        'labelShowBg',
        'labelBgStyle',
        'labelBgPadding',
        'labelBgBorderRadius',
        'sourceY',
        'sourceX',
        'targetX',
        'targetY',
        'markerEnd',
        'markerStart',
        'interactionWidth',
      ],
      compatConfig: { MODE: 3 },
      setup(e, { attrs: t }) {
        return () => {
          const [n, r, o] = FS({
            ...e,
            sourcePosition: e.sourcePosition ?? pe.Bottom,
            targetPosition: e.targetPosition ?? pe.Top,
          })
          return Ce(Di, { path: n, labelX: r, labelY: o, ...t, ...e })
        }
      },
    }),
    xL = SL,
    CL = { input: nL, default: eL, output: tL },
    EL = { default: wL, straight: gL, step: bL, smoothstep: kS, simplebezier: xL }
  function $L(e, t, n) {
    const r = X(() => (m) => t.value.get(m)),
      o = X(() => (m) => n.value.get(m)),
      i = X(() => {
        const m = { ...EL, ...e.edgeTypes },
          v = Object.keys(m)
        for (const b of e.edges) b.type && !v.includes(b.type) && (m[b.type] = b.type)
        return m
      }),
      a = X(() => {
        const m = { ...CL, ...e.nodeTypes },
          v = Object.keys(m)
        for (const b of e.nodes) b.type && !v.includes(b.type) && (m[b.type] = b.type)
        return m
      }),
      s = X(() =>
        e.onlyRenderVisibleElements
          ? SS(
              e.nodes,
              { x: 0, y: 0, width: e.dimensions.width, height: e.dimensions.height },
              e.viewport,
              !0
            )
          : e.nodes
      ),
      l = X(() => {
        if (e.onlyRenderVisibleElements) {
          const m = []
          for (const v of e.edges) {
            const b = t.value.get(v.source),
              y = t.value.get(v.target)
            Sz({
              sourcePos: b.computedPosition || { x: 0, y: 0 },
              targetPos: y.computedPosition || { x: 0, y: 0 },
              sourceWidth: b.dimensions.width,
              sourceHeight: b.dimensions.height,
              targetWidth: y.dimensions.width,
              targetHeight: y.dimensions.height,
              width: e.dimensions.width,
              height: e.dimensions.height,
              viewport: e.viewport,
            }) && m.push(v)
          }
          return m
        }
        return e.edges
      }),
      u = X(() => [...s.value, ...l.value]),
      c = X(() => {
        const m = []
        for (const v of e.nodes) v.selected && m.push(v)
        return m
      }),
      d = X(() => {
        const m = []
        for (const v of e.edges) v.selected && m.push(v)
        return m
      }),
      f = X(() => [...c.value, ...d.value]),
      h = X(() => {
        const m = []
        for (const v of e.nodes)
          v.dimensions.width && v.dimensions.height && v.handleBounds !== void 0 && m.push(v)
        return m
      }),
      g = X(() => s.value.length > 0 && h.value.length === s.value.length)
    return {
      getNode: r,
      getEdge: o,
      getElements: u,
      getEdgeTypes: i,
      getNodeTypes: a,
      getEdges: l,
      getNodes: s,
      getSelectedElements: f,
      getSelectedNodes: c,
      getSelectedEdges: d,
      getNodesInitialized: h,
      areNodesInitialized: g,
    }
  }
  class dn {
    constructor() {
      ;((this.currentId = 0), (this.flows = new Map()))
    }
    static getInstance() {
      var t
      const n = (t = Qe()) == null ? void 0 : t.appContext.app,
        r = n?.config.globalProperties.$vueFlowStorage ?? dn.instance
      return (
        (dn.instance = r ?? new dn()),
        n && (n.config.globalProperties.$vueFlowStorage = dn.instance),
        dn.instance
      )
    }
    set(t, n) {
      return this.flows.set(t, n)
    }
    get(t) {
      return this.flows.get(t)
    }
    remove(t) {
      return this.flows.delete(t)
    }
    create(t, n) {
      const r = BS(),
        o = Ko(r),
        i = {}
      for (const [f, h] of Object.entries(o.hooks)) {
        const g = `on${f.charAt(0).toUpperCase() + f.slice(1)}`
        i[g] = h.on
      }
      const a = {}
      for (const [f, h] of Object.entries(o.hooks)) a[f] = h.trigger
      const s = X(() => {
          const f = new Map()
          for (const h of o.nodes) f.set(h.id, h)
          return f
        }),
        l = X(() => {
          const f = new Map()
          for (const h of o.edges) f.set(h.id, h)
          return f
        }),
        u = $L(o, s, l),
        c = Zz(o, s, l)
      c.setState({ ...o, ...n })
      const d = {
        ...i,
        ...u,
        ...c,
        ...mD(o),
        nodeLookup: s,
        edgeLookup: l,
        emits: a,
        id: t,
        vueFlowVersion: '1.48.0',
        $destroy: () => {
          this.remove(t)
        },
      }
      return (this.set(t, d), d)
    }
    getId() {
      return `vue-flow-${this.currentId++}`
    }
  }
  function Ae(e) {
    const t = dn.getInstance(),
      n = lf(),
      r = typeof e == 'object',
      o = r ? e : { id: e },
      i = o.id,
      a = i ?? n?.vueFlowId
    let s
    if (n) {
      const l = xt(J0, null)
      typeof l < 'u' && l !== null && (!a || l.id === a) && (s = l)
    }
    if ((s || (a && (s = t.get(a))), !s || (a && s.id !== a))) {
      const l = i ?? t.getId(),
        u = t.create(l, o)
      ;((s = u),
        (n ?? d_(!0)).run(() => {
          ;(me(
            u.applyDefault,
            (d, f, h) => {
              const g = (v) => {
                  u.applyNodeChanges(v)
                },
                m = (v) => {
                  u.applyEdgeChanges(v)
                }
              ;(d
                ? (u.onNodesChange(g), u.onEdgesChange(m))
                : (u.hooks.value.nodesChange.off(g), u.hooks.value.edgesChange.off(m)),
                h(() => {
                  ;(u.hooks.value.nodesChange.off(g), u.hooks.value.edgesChange.off(m))
                }))
            },
            { immediate: !0 }
          ),
            Ar(() => {
              if (s) {
                const d = t.get(s.id)
                d ? d.$destroy() : Zr(`No store instance found for id ${s.id} in storage.`)
              }
            }))
        }))
    } else r && s.setState(o)
    if ((n && (St(J0, s), (n.vueFlowId = s.id)), r)) {
      const l = Qe()
      l?.type.name !== 'VueFlow' && s.emits.error(new Le(Be.USEVUEFLOW_OPTIONS))
    }
    return s
  }
  function TL(e) {
    const { emits: t, dimensions: n } = Ae()
    let r
    Me(() => {
      const o = () => {
        var i, a
        if (!e.value || !(((a = (i = e.value).checkVisibility) == null ? void 0 : a.call(i)) ?? !0))
          return
        const s = Pi(e.value)
        ;((s.width === 0 || s.height === 0) && t.error(new Le(Be.MISSING_VIEWPORT_DIMENSIONS)),
          (n.value = { width: s.width || 500, height: s.height || 500 }))
      }
      ;(o(),
        window.addEventListener('resize', o),
        e.value && ((r = new ResizeObserver(() => o())), r.observe(e.value)),
        je(() => {
          ;(window.removeEventListener('resize', o), r && e.value && r.unobserve(e.value))
        }))
    })
  }
  const OL = { name: 'UserSelection', compatConfig: { MODE: 3 } },
    PL = te({
      ...OL,
      props: { userSelectionRect: {} },
      setup(e) {
        return (t, n) => (
          ee(),
          ve(
            'div',
            {
              class: 'vue-flow__selection vue-flow__container',
              style: Ct({
                width: `${t.userSelectionRect.width}px`,
                height: `${t.userSelectionRect.height}px`,
                transform: `translate(${t.userSelectionRect.x}px, ${t.userSelectionRect.y}px)`,
              }),
            },
            null,
            4
          )
        )
      },
    }),
    IL = ['tabIndex'],
    AL = { name: 'NodesSelection', compatConfig: { MODE: 3 } },
    NL = te({
      ...AL,
      setup(e) {
        const {
            emits: t,
            viewport: n,
            getSelectedNodes: r,
            noPanClassName: o,
            disableKeyboardA11y: i,
            userSelectionActive: a,
          } = Ae(),
          s = DS(),
          l = de(null),
          u = NS({
            el: l,
            onStart(g) {
              ;(t.selectionDragStart(g), t.nodeDragStart(g))
            },
            onDrag(g) {
              ;(t.selectionDrag(g), t.nodeDrag(g))
            },
            onStop(g) {
              ;(t.selectionDragStop(g), t.nodeDragStop(g))
            },
          })
        Me(() => {
          var g
          i.value || (g = l.value) == null || g.focus({ preventScroll: !0 })
        })
        const c = X(() => wS(r.value)),
          d = X(() => ({
            width: `${c.value.width}px`,
            height: `${c.value.height}px`,
            top: `${c.value.y}px`,
            left: `${c.value.x}px`,
          }))
        function f(g) {
          t.selectionContextMenu({ event: g, nodes: r.value })
        }
        function h(g) {
          i.value ||
            (zn[g.key] && (g.preventDefault(), s({ x: zn[g.key].x, y: zn[g.key].y }, g.shiftKey)))
        }
        return (g, m) =>
          !K(a) && c.value.width && c.value.height
            ? (ee(),
              ve(
                'div',
                {
                  key: 0,
                  class: ct(['vue-flow__nodesselection vue-flow__container', K(o)]),
                  style: Ct({
                    transform: `translate(${K(n).x}px,${K(n).y}px) scale(${K(n).zoom})`,
                  }),
                },
                [
                  he(
                    'div',
                    {
                      ref_key: 'el',
                      ref: l,
                      class: ct([{ dragging: K(u) }, 'vue-flow__nodesselection-rect']),
                      style: Ct(d.value),
                      tabIndex: K(i) ? void 0 : -1,
                      onContextmenu: f,
                      onKeydown: h,
                    },
                    null,
                    46,
                    IL
                  ),
                ],
                6
              ))
            : Pe('', !0)
      },
    })
  function RL(e, t) {
    return { x: e.clientX - t.left, y: e.clientY - t.top }
  }
  const ML = { name: 'Pane', compatConfig: { MODE: 3 } },
    DL = te({
      ...ML,
      props: { isSelecting: { type: Boolean }, selectionKeyPressed: { type: Boolean } },
      setup(e) {
        const {
            vueFlowRef: t,
            nodes: n,
            viewport: r,
            emits: o,
            userSelectionActive: i,
            removeSelectedElements: a,
            userSelectionRect: s,
            elementsSelectable: l,
            nodesSelectionActive: u,
            getSelectedEdges: c,
            getSelectedNodes: d,
            removeNodes: f,
            removeEdges: h,
            selectionMode: g,
            deleteKeyCode: m,
            multiSelectionKeyCode: v,
            multiSelectionActive: b,
            edgeLookup: y,
            nodeLookup: p,
            connectionLookup: _,
            defaultEdgeOptions: x,
            connectionStartHandle: S,
          } = Ae(),
          w = de(null),
          T = de(new Set()),
          A = de(new Set()),
          $ = de(),
          P = Oe(() => l.value && (e.isSelecting || i.value)),
          E = Oe(() => S.value !== null)
        let z = !1,
          C = !1
        const R = xr(m, { actInsideInputWithModifier: !1 }),
          N = xr(v)
        ;(me(R, (B) => {
          B && (f(d.value), h(c.value), (u.value = !1))
        }),
          me(N, (B) => {
            b.value = B
          }))
        function j(B, L) {
          return (k) => {
            k.target === L && B?.(k)
          }
        }
        function V(B) {
          if (z || E.value) {
            z = !1
            return
          }
          ;(o.paneClick(B), a(), (u.value = !1))
        }
        function H(B) {
          ;(B.preventDefault(), B.stopPropagation(), o.paneContextMenu(B))
        }
        function G(B) {
          o.paneScroll(B)
        }
        function Y(B) {
          var L, k, U
          if (
            (($.value = (L = t.value) == null ? void 0 : L.getBoundingClientRect()),
            !l.value || !e.isSelecting || B.button !== 0 || B.target !== w.value || !$.value)
          )
            return
          ;(U = (k = B.target) == null ? void 0 : k.setPointerCapture) == null ||
            U.call(k, B.pointerId)
          const { x: J, y: re } = RL(B, $.value)
          ;((C = !0),
            (z = !1),
            a(),
            (s.value = { width: 0, height: 0, startX: J, startY: re, x: J, y: re }),
            o.selectionStart(B))
        }
        function Z(B) {
          var L
          if (!$.value || !s.value) return
          z = !0
          const { x: k, y: U } = mt(B, $.value),
            { startX: J = 0, startY: re = 0 } = s.value,
            ie = {
              startX: J,
              startY: re,
              x: k < J ? k : J,
              y: U < re ? U : re,
              width: Math.abs(k - J),
              height: Math.abs(U - re),
            },
            _e = T.value,
            ye = A.value
          ;((T.value = new Set(
            SS(n.value, ie, r.value, g.value === ih.Partial, !0).map((M) => M.id)
          )),
            (A.value = new Set()))
          const be = ((L = x.value) == null ? void 0 : L.selectable) ?? !0
          for (const M of T.value) {
            const O = _.value.get(M)
            if (O)
              for (const { edgeId: q } of O.values()) {
                const I = y.value.get(q)
                I && (I.selectable ?? be) && A.value.add(q)
              }
          }
          if (!Z0(_e, T.value)) {
            const M = Yt(p.value, T.value, !0)
            o.nodesChange(M)
          }
          if (!Z0(ye, A.value)) {
            const M = Yt(y.value, A.value)
            o.edgesChange(M)
          }
          ;((s.value = ie), (i.value = !0), (u.value = !1))
        }
        function ne(B) {
          var L
          B.button !== 0 ||
            !C ||
            ((L = B.target) == null || L.releasePointerCapture(B.pointerId),
            !i.value && s.value && B.target === w.value && V(B),
            (i.value = !1),
            (s.value = null),
            (u.value = T.value.size > 0),
            o.selectionEnd(B),
            e.selectionKeyPressed && (z = !1),
            (C = !1))
        }
        return (B, L) => (
          ee(),
          ve(
            'div',
            {
              ref_key: 'container',
              ref: w,
              class: ct(['vue-flow__pane vue-flow__container', { selection: B.isSelecting }]),
              onClick: L[0] || (L[0] = (k) => (P.value ? void 0 : j(V, w.value)(k))),
              onContextmenu: L[1] || (L[1] = (k) => j(H, w.value)(k)),
              onWheelPassive: L[2] || (L[2] = (k) => j(G, w.value)(k)),
              onPointerenter: L[3] || (L[3] = (k) => (P.value ? void 0 : K(o).paneMouseEnter(k))),
              onPointerdown: L[4] || (L[4] = (k) => (P.value ? Y(k) : K(o).paneMouseMove(k))),
              onPointermove: L[5] || (L[5] = (k) => (P.value ? Z(k) : K(o).paneMouseMove(k))),
              onPointerup: L[6] || (L[6] = (k) => (P.value ? ne(k) : void 0)),
              onPointerleave: L[7] || (L[7] = (k) => K(o).paneMouseLeave(k)),
            },
            [
              bt(B.$slots, 'default'),
              K(i) && K(s)
                ? (ee(),
                  ke(PL, { key: 0, 'user-selection-rect': K(s) }, null, 8, ['user-selection-rect']))
                : Pe('', !0),
              K(u) && K(d).length ? (ee(), ke(NL, { key: 1 })) : Pe('', !0),
            ],
            34
          )
        )
      },
    }),
    BL = { name: 'Transform', compatConfig: { MODE: 3 } },
    qL = te({
      ...BL,
      setup(e) {
        const { viewport: t, fitViewOnInit: n, fitViewOnInitDone: r } = Ae(),
          o = X(() => (n.value ? !r.value : !1)),
          i = X(() => `translate(${t.value.x}px,${t.value.y}px) scale(${t.value.zoom})`)
        return (a, s) => (
          ee(),
          ve(
            'div',
            {
              class: 'vue-flow__transformationpane vue-flow__container',
              style: Ct({ transform: i.value, opacity: o.value ? 0 : void 0 }),
            },
            [bt(a.$slots, 'default')],
            4
          )
        )
      },
    }),
    zL = { name: 'Viewport', compatConfig: { MODE: 3 } },
    LL = te({
      ...zL,
      setup(e) {
        const {
          minZoom: t,
          maxZoom: n,
          defaultViewport: r,
          translateExtent: o,
          zoomActivationKeyCode: i,
          selectionKeyCode: a,
          panActivationKeyCode: s,
          panOnScroll: l,
          panOnScrollMode: u,
          panOnScrollSpeed: c,
          panOnDrag: d,
          zoomOnDoubleClick: f,
          zoomOnPinch: h,
          zoomOnScroll: g,
          preventScrolling: m,
          noWheelClassName: v,
          noPanClassName: b,
          emits: y,
          connectionStartHandle: p,
          userSelectionActive: _,
          paneDragging: x,
          d3Zoom: S,
          d3Selection: w,
          d3ZoomHandler: T,
          viewport: A,
          viewportRef: $,
          paneClickDistance: P,
        } = Ae()
        TL($)
        const E = ce(!1),
          z = ce(!1)
        let C = null,
          R = !1,
          N = 0,
          j = { x: 0, y: 0, zoom: 0 }
        const V = xr(s),
          H = xr(a),
          G = xr(i),
          Y = Oe(() => (!H.value || (H.value && a.value === !0)) && (V.value || d.value)),
          Z = Oe(() => V.value || l.value),
          ne = Oe(() => H.value || (a.value === !0 && Y.value !== !0)),
          B = Oe(() => p.value !== null)
        Me(() => {
          if (!$.value) {
            Zr('Viewport element is missing')
            return
          }
          const re = $.value,
            ie = re.getBoundingClientRect(),
            _e = tz()
              .clickDistance(P.value)
              .scaleExtent([t.value, n.value])
              .translateExtent(o.value),
            ye = lt(re).call(_e),
            be = ye.on('wheel.zoom'),
            M = Wn.translate(r.value.x ?? 0, r.value.y ?? 0).scale(
              Sn(r.value.zoom ?? 1, t.value, n.value)
            ),
            O = [
              [0, 0],
              [ie.width, ie.height],
            ],
            q = _e.constrain()(M, O, o.value)
          ;(_e.transform(ye, q),
            _e.wheelDelta(q0),
            (S.value = _e),
            (w.value = ye),
            (T.value = be),
            (A.value = { x: q.x, y: q.y, zoom: q.k }),
            _e.on('start', (I) => {
              var W
              if (!I.sourceEvent) return null
              ;((N = I.sourceEvent.button), (E.value = !0))
              const ae = U(I.transform)
              ;(((W = I.sourceEvent) == null ? void 0 : W.type) === 'mousedown' && (x.value = !0),
                (j = ae),
                y.viewportChangeStart(ae),
                y.moveStart({ event: I, flowTransform: ae }))
            }),
            _e.on('end', (I) => {
              if (!I.sourceEvent) return null
              if (
                ((E.value = !1),
                (x.value = !1),
                L(Y.value, N ?? 0) && !R && y.paneContextMenu(I.sourceEvent),
                (R = !1),
                k(j, I.transform))
              ) {
                const W = U(I.transform)
                ;((j = W), y.viewportChangeEnd(W), y.moveEnd({ event: I, flowTransform: W }))
              }
            }),
            _e.filter((I) => {
              var W
              const ae = G.value || g.value,
                fe = h.value && I.ctrlKey,
                le = I.button,
                ue = I.type === 'wheel'
              if (
                le === 1 &&
                I.type === 'mousedown' &&
                (J(I, 'vue-flow__node') || J(I, 'vue-flow__edge'))
              )
                return !0
              if (
                (!Y.value && !ae && !Z.value && !f.value && !h.value) ||
                _.value ||
                (B.value && !ue) ||
                (!f.value && I.type === 'dblclick') ||
                (J(I, v.value) && ue) ||
                (J(I, b.value) && (!ue || (Z.value && ue && !G.value))) ||
                (!h.value && I.ctrlKey && ue) ||
                (!ae && !Z.value && !fe && ue)
              )
                return !1
              if (
                !h &&
                I.type === 'touchstart' &&
                ((W = I.touches) == null ? void 0 : W.length) > 1
              )
                return (I.preventDefault(), !1)
              if (
                (!Y.value && (I.type === 'mousedown' || I.type === 'touchstart')) ||
                (a.value === !0 && Array.isArray(d.value) && d.value.includes(0) && le === 0) ||
                (Array.isArray(d.value) &&
                  !d.value.includes(le) &&
                  (I.type === 'mousedown' || I.type === 'touchstart'))
              )
                return !1
              const ge =
                (Array.isArray(d.value) && d.value.includes(le)) ||
                (a.value === !0 && Array.isArray(d.value) && !d.value.includes(0)) ||
                !le ||
                le <= 1
              return (!I.ctrlKey || V.value || ue) && ge
            }),
            me(
              [_, Y],
              () => {
                _.value && !E.value
                  ? _e.on('zoom', null)
                  : _.value ||
                    _e.on('zoom', (I) => {
                      A.value = { x: I.transform.x, y: I.transform.y, zoom: I.transform.k }
                      const W = U(I.transform)
                      ;((R = L(Y.value, N ?? 0)),
                        y.viewportChange(W),
                        y.move({ event: I, flowTransform: W }))
                    })
              },
              { immediate: !0 }
            ),
            me(
              [_, Z, u, G, h, m, v],
              () => {
                Z.value && !G.value && !_.value
                  ? ye.on(
                      'wheel.zoom',
                      (I) => {
                        if (J(I, v.value)) return !1
                        const W = G.value || g.value,
                          ae = h.value && I.ctrlKey
                        if (!(!m.value || Z.value || W || ae)) return !1
                        ;(I.preventDefault(), I.stopImmediatePropagation())
                        const le = ye.property('__zoom').k || 1,
                          ue = Xo()
                        if (!V.value && I.ctrlKey && h.value && ue) {
                          const Ht = vt(I),
                            jt = q0(I),
                            Jr = le * 2 ** jt
                          _e.scaleTo(ye, Jr, Ht, I)
                          return
                        }
                        const ge = I.deltaMode === 1 ? 20 : 1
                        let Se = u.value === Sr.Vertical ? 0 : I.deltaX * ge,
                          $e = u.value === Sr.Horizontal ? 0 : I.deltaY * ge
                        ;(!ue &&
                          I.shiftKey &&
                          u.value !== Sr.Vertical &&
                          !Se &&
                          $e &&
                          ((Se = $e), ($e = 0)),
                          _e.translateBy(ye, -(Se / le) * c.value, -($e / le) * c.value))
                        const et = U(ye.property('__zoom'))
                        ;(C && clearTimeout(C),
                          z.value
                            ? (y.move({ event: I, flowTransform: et }),
                              y.viewportChange(et),
                              (C = setTimeout(() => {
                                ;(y.moveEnd({ event: I, flowTransform: et }),
                                  y.viewportChangeEnd(et),
                                  (z.value = !1))
                              }, 150)))
                            : ((z.value = !0),
                              y.moveStart({ event: I, flowTransform: et }),
                              y.viewportChangeStart(et)))
                      },
                      { passive: !1 }
                    )
                  : typeof be < 'u' &&
                    ye.on(
                      'wheel.zoom',
                      function (I, W) {
                        const ae = !m.value && I.type === 'wheel' && !I.ctrlKey,
                          fe = G.value || g.value,
                          le = h.value && I.ctrlKey
                        if ((!fe && !l.value && !le && I.type === 'wheel') || ae || J(I, v.value))
                          return null
                        ;(I.preventDefault(), be.call(this, I, W))
                      },
                      { passive: !1 }
                    )
              },
              { immediate: !0 }
            ))
        })
        function L(re, ie) {
          return ie === 2 && Array.isArray(re) && re.includes(2)
        }
        function k(re, ie) {
          return (
            (re.x !== ie.x && !Number.isNaN(ie.x)) ||
            (re.y !== ie.y && !Number.isNaN(ie.y)) ||
            (re.zoom !== ie.k && !Number.isNaN(ie.k))
          )
        }
        function U(re) {
          return { x: re.x, y: re.y, zoom: re.k }
        }
        function J(re, ie) {
          return re.target.closest(`.${ie}`)
        }
        return (re, ie) => (
          ee(),
          ve(
            'div',
            { ref_key: 'viewportRef', ref: $, class: 'vue-flow__viewport vue-flow__container' },
            [
              F(
                DL,
                {
                  'is-selecting': ne.value,
                  'selection-key-pressed': K(H),
                  class: ct({
                    connecting: B.value,
                    dragging: K(x),
                    draggable: K(d) === !0 || (Array.isArray(K(d)) && K(d).includes(0)),
                  }),
                },
                {
                  default: Ve(() => [
                    F(qL, null, { default: Ve(() => [bt(re.$slots, 'default')]), _: 3 }),
                  ]),
                  _: 3,
                },
                8,
                ['is-selecting', 'selection-key-pressed', 'class']
              ),
            ],
            512
          )
        )
      },
    }),
    FL = ['id'],
    kL = ['id'],
    HL = ['id'],
    jL = { name: 'A11yDescriptions', compatConfig: { MODE: 3 } },
    VL = te({
      ...jL,
      setup(e) {
        const { id: t, disableKeyboardA11y: n, ariaLiveMessage: r } = Ae()
        return (o, i) => (
          ee(),
          ve(
            Re,
            null,
            [
              he(
                'div',
                { id: `${K(hS)}-${K(t)}`, style: { display: 'none' } },
                ' Press enter or space to select a node. ' +
                  ze(K(n) ? '' : 'You can then use the arrow keys to move the node around.') +
                  ' You can then use the arrow keys to move the node around, press delete to remove it and press escape to cancel. ',
                9,
                FL
              ),
              he(
                'div',
                { id: `${K(pS)}-${K(t)}`, style: { display: 'none' } },
                ' Press enter or space to select an edge. You can then press delete to remove it or press escape to cancel. ',
                8,
                kL
              ),
              K(n)
                ? Pe('', !0)
                : (ee(),
                  ve(
                    'div',
                    {
                      key: 0,
                      id: `${K(sz)}-${K(t)}`,
                      'aria-live': 'assertive',
                      'aria-atomic': 'true',
                      style: {
                        position: 'absolute',
                        width: '1px',
                        height: '1px',
                        margin: '-1px',
                        border: '0',
                        padding: '0',
                        overflow: 'hidden',
                        clip: 'rect(0px, 0px, 0px, 0px)',
                        'clip-path': 'inset(100%)',
                      },
                    },
                    ze(K(r)),
                    9,
                    HL
                  )),
            ],
            64
          )
        )
      },
    })
  function GL() {
    const e = Ae()
    me(
      () => e.viewportHelper.value.viewportInitialized,
      (t) => {
        t &&
          setTimeout(() => {
            ;(e.emits.init(e), e.emits.paneReady(e))
          }, 1)
      }
    )
  }
  function WL(e, t, n) {
    return n === pe.Left ? e - t : n === pe.Right ? e + t : e
  }
  function UL(e, t, n) {
    return n === pe.Top ? e - t : n === pe.Bottom ? e + t : e
  }
  const lh = function ({
    radius: e = 10,
    centerX: t = 0,
    centerY: n = 0,
    position: r = pe.Top,
    type: o,
  }) {
    return Ce('circle', {
      class: `vue-flow__edgeupdater vue-flow__edgeupdater-${o}`,
      cx: WL(t, e, r),
      cy: UL(n, e, r),
      r: e,
      stroke: 'transparent',
      fill: 'transparent',
    })
  }
  lh.props = ['radius', 'centerX', 'centerY', 'position', 'type']
  lh.compatConfig = { MODE: 3 }
  const r_ = lh,
    YL = te({
      name: 'Edge',
      compatConfig: { MODE: 3 },
      props: ['id'],
      setup(e) {
        const {
            id: t,
            addSelectedEdges: n,
            connectionMode: r,
            edgeUpdaterRadius: o,
            emits: i,
            nodesSelectionActive: a,
            noPanClassName: s,
            getEdgeTypes: l,
            removeSelectedEdges: u,
            findEdge: c,
            findNode: d,
            isValidConnection: f,
            multiSelectionActive: h,
            disableKeyboardA11y: g,
            elementsSelectable: m,
            edgesUpdatable: v,
            edgesFocusable: b,
            hooks: y,
          } = Ae(),
          p = X(() => c(e.id)),
          { emit: _, on: x } = zz(p.value, i),
          S = xt(Ai),
          w = Qe(),
          T = de(!1),
          A = de(!1),
          $ = de(''),
          P = de(null),
          E = de('source'),
          z = de(null),
          C = Oe(() => (typeof p.value.selectable > 'u' ? m.value : p.value.selectable)),
          R = Oe(() => (typeof p.value.updatable > 'u' ? v.value : p.value.updatable)),
          N = Oe(() => (typeof p.value.focusable > 'u' ? b.value : p.value.focusable))
        ;(St(Dz, e.id), St(Bz, z))
        const j = X(() =>
            p.value.class instanceof Function ? p.value.class(p.value) : p.value.class
          ),
          V = X(() => (p.value.style instanceof Function ? p.value.style(p.value) : p.value.style)),
          H = X(() => {
            const O = p.value.type || 'default',
              q = S?.[`edge-${O}`]
            if (q) return q
            let I = p.value.template ?? l.value[O]
            if (typeof I == 'string' && w) {
              const W = Object.keys(w.appContext.components)
              W && W.includes(O) && (I = f_(O, !1))
            }
            return I && typeof I != 'string' ? I : (i.error(new Le(Be.EDGE_TYPE_MISSING, I)), !1)
          }),
          { handlePointerDown: G } = RS({
            nodeId: $,
            handleId: P,
            type: E,
            isValidConnection: f,
            edgeUpdaterType: E,
            onEdgeUpdate: ne,
            onEdgeUpdateEnd: B,
          })
        return () => {
          const O = d(p.value.source),
            q = d(p.value.target),
            I = 'pathOptions' in p.value ? p.value.pathOptions : {}
          if (!O && !q)
            return (
              i.error(
                new Le(Be.EDGE_SOURCE_TARGET_MISSING, p.value.id, p.value.source, p.value.target)
              ),
              null
            )
          if (!O) return (i.error(new Le(Be.EDGE_SOURCE_MISSING, p.value.id, p.value.source)), null)
          if (!q) return (i.error(new Le(Be.EDGE_TARGET_MISSING, p.value.id, p.value.target)), null)
          if (!p.value || p.value.hidden || O.hidden || q.hidden) return null
          let W
          r.value === Zt.Strict
            ? (W = O.handleBounds.source)
            : (W = [...(O.handleBounds.source || []), ...(O.handleBounds.target || [])])
          const ae = G0(W, p.value.sourceHandle)
          let fe
          r.value === Zt.Strict
            ? (fe = q.handleBounds.target)
            : (fe = [...(q.handleBounds.target || []), ...(q.handleBounds.source || [])])
          const le = G0(fe, p.value.targetHandle),
            ue = ae?.position || pe.Bottom,
            ge = le?.position || pe.Top,
            { x: Se, y: $e } = Un(O, ae, ue),
            { x: et, y: Ht } = Un(q, le, ge)
          return (
            (p.value.sourceX = Se),
            (p.value.sourceY = $e),
            (p.value.targetX = et),
            (p.value.targetY = Ht),
            Ce(
              'g',
              {
                ref: z,
                key: e.id,
                'data-id': e.id,
                class: [
                  'vue-flow__edge',
                  `vue-flow__edge-${H.value === !1 ? 'default' : p.value.type || 'default'}`,
                  s.value,
                  j.value,
                  {
                    updating: T.value,
                    selected: p.value.selected,
                    animated: p.value.animated,
                    inactive: !C.value && !y.value.edgeClick.hasListeners(),
                  },
                ],
                tabIndex: N.value ? 0 : void 0,
                'aria-label':
                  p.value.ariaLabel === null
                    ? void 0
                    : (p.value.ariaLabel ?? `Edge from ${p.value.source} to ${p.value.target}`),
                'aria-describedby': N.value ? `${pS}-${t}` : void 0,
                'aria-roledescription': 'edge',
                role: N.value ? 'group' : 'img',
                ...p.value.domAttributes,
                onClick: k,
                onContextmenu: U,
                onDblclick: J,
                onMouseenter: re,
                onMousemove: ie,
                onMouseleave: _e,
                onKeyDown: N.value ? M : void 0,
              },
              [
                A.value
                  ? null
                  : Ce(H.value === !1 ? l.value.default : H.value, {
                      id: e.id,
                      sourceNode: O,
                      targetNode: q,
                      source: p.value.source,
                      target: p.value.target,
                      type: p.value.type,
                      updatable: R.value,
                      selected: p.value.selected,
                      animated: p.value.animated,
                      label: p.value.label,
                      labelStyle: p.value.labelStyle,
                      labelShowBg: p.value.labelShowBg,
                      labelBgStyle: p.value.labelBgStyle,
                      labelBgPadding: p.value.labelBgPadding,
                      labelBgBorderRadius: p.value.labelBgBorderRadius,
                      data: p.value.data,
                      events: { ...p.value.events, ...x },
                      style: V.value,
                      markerStart: `url('#${zr(p.value.markerStart, t)}')`,
                      markerEnd: `url('#${zr(p.value.markerEnd, t)}')`,
                      sourcePosition: ue,
                      targetPosition: ge,
                      sourceX: Se,
                      sourceY: $e,
                      targetX: et,
                      targetY: Ht,
                      sourceHandleId: p.value.sourceHandle,
                      targetHandleId: p.value.targetHandle,
                      interactionWidth: p.value.interactionWidth,
                      ...I,
                    }),
                [
                  R.value === 'source' || R.value === !0
                    ? [
                        Ce(
                          'g',
                          { onMousedown: ye, onMouseenter: Y, onMouseout: Z },
                          Ce(r_, {
                            position: ue,
                            centerX: Se,
                            centerY: $e,
                            radius: o.value,
                            type: 'source',
                            'data-type': 'source',
                          })
                        ),
                      ]
                    : null,
                  R.value === 'target' || R.value === !0
                    ? [
                        Ce(
                          'g',
                          { onMousedown: be, onMouseenter: Y, onMouseout: Z },
                          Ce(r_, {
                            position: ge,
                            centerX: et,
                            centerY: Ht,
                            radius: o.value,
                            type: 'target',
                            'data-type': 'target',
                          })
                        ),
                      ]
                    : null,
                ],
              ]
            )
          )
        }
        function Y() {
          T.value = !0
        }
        function Z() {
          T.value = !1
        }
        function ne(O, q) {
          _.update({ event: O, edge: p.value, connection: q })
        }
        function B(O) {
          ;(_.updateEnd({ event: O, edge: p.value }), (A.value = !1))
        }
        function L(O, q) {
          O.button === 0 &&
            ((A.value = !0),
            ($.value = q ? p.value.target : p.value.source),
            (P.value = (q ? p.value.targetHandle : p.value.sourceHandle) ?? null),
            (E.value = q ? 'target' : 'source'),
            _.updateStart({ event: O, edge: p.value }),
            G(O))
        }
        function k(O) {
          var q
          const I = { event: O, edge: p.value }
          ;(C.value &&
            ((a.value = !1),
            p.value.selected && h.value
              ? (u([p.value]), (q = z.value) == null || q.blur())
              : n([p.value])),
            _.click(I))
        }
        function U(O) {
          _.contextMenu({ event: O, edge: p.value })
        }
        function J(O) {
          _.doubleClick({ event: O, edge: p.value })
        }
        function re(O) {
          _.mouseEnter({ event: O, edge: p.value })
        }
        function ie(O) {
          _.mouseMove({ event: O, edge: p.value })
        }
        function _e(O) {
          _.mouseLeave({ event: O, edge: p.value })
        }
        function ye(O) {
          L(O, !0)
        }
        function be(O) {
          L(O, !1)
        }
        function M(O) {
          var q
          !g.value &&
            vS.includes(O.key) &&
            C.value &&
            (O.key === 'Escape' ? ((q = z.value) == null || q.blur(), u([c(e.id)])) : n([c(e.id)]))
        }
      },
    }),
    XL = YL,
    KL = te({
      name: 'ConnectionLine',
      compatConfig: { MODE: 3 },
      setup() {
        var e
        const {
            id: t,
            connectionMode: n,
            connectionStartHandle: r,
            connectionEndHandle: o,
            connectionPosition: i,
            connectionLineType: a,
            connectionLineStyle: s,
            connectionLineOptions: l,
            connectionStatus: u,
            viewport: c,
            findNode: d,
          } = Ae(),
          f = (e = xt(Ai)) == null ? void 0 : e['connection-line'],
          h = X(() => {
            var y
            return d((y = r.value) == null ? void 0 : y.nodeId)
          }),
          g = X(() => {
            var y
            return d((y = o.value) == null ? void 0 : y.nodeId) ?? null
          }),
          m = X(() => ({
            x: (i.value.x - c.value.x) / c.value.zoom,
            y: (i.value.y - c.value.y) / c.value.zoom,
          })),
          v = X(() => (l.value.markerStart ? `url(#${zr(l.value.markerStart, t)})` : '')),
          b = X(() => (l.value.markerEnd ? `url(#${zr(l.value.markerEnd, t)})` : ''))
        return () => {
          var y, p, _
          if (!h.value || !r.value) return null
          const x = r.value.id,
            S = r.value.type,
            w = h.value.handleBounds
          let T = w?.[S] ?? []
          if (n.value === Zt.Loose) {
            const V = w?.[S === 'source' ? 'target' : 'source'] ?? []
            T = [...T, ...V]
          }
          if (!T) return null
          const A = (x ? T.find((V) => V.id === x) : T[0]) ?? null,
            $ = A?.position ?? pe.Top,
            { x: P, y: E } = Un(h.value, A, $)
          let z = null
          g.value &&
            (n.value === Zt.Strict
              ? (z =
                  ((y = g.value.handleBounds[S === 'source' ? 'target' : 'source']) == null
                    ? void 0
                    : y.find((V) => {
                        var H
                        return V.id === ((H = o.value) == null ? void 0 : H.id)
                      })) || null)
              : (z =
                  ((p = [
                    ...(g.value.handleBounds.source ?? []),
                    ...(g.value.handleBounds.target ?? []),
                  ]) == null
                    ? void 0
                    : p.find((V) => {
                        var H
                        return V.id === ((H = o.value) == null ? void 0 : H.id)
                      })) || null))
          const C = ((_ = o.value) == null ? void 0 : _.position) ?? ($ ? Jd[$] : null)
          if (!$ || !C) return null
          const R = a.value ?? l.value.type ?? cn.Bezier
          let N = ''
          const j = {
            sourceX: P,
            sourceY: E,
            sourcePosition: $,
            targetX: m.value.x,
            targetY: m.value.y,
            targetPosition: C,
          }
          return (
            R === cn.Bezier
              ? ([N] = LS(j))
              : R === cn.Step
                ? ([N] = ef({ ...j, borderRadius: 0 }))
                : R === cn.SmoothStep
                  ? ([N] = ef(j))
                  : R === cn.SimpleBezier
                    ? ([N] = FS(j))
                    : (N = `M${P},${E} ${m.value.x},${m.value.y}`),
            Ce(
              'svg',
              { class: 'vue-flow__edges vue-flow__connectionline vue-flow__container' },
              Ce(
                'g',
                { class: 'vue-flow__connection' },
                f
                  ? Ce(f, {
                      sourceX: P,
                      sourceY: E,
                      sourcePosition: $,
                      targetX: m.value.x,
                      targetY: m.value.y,
                      targetPosition: C,
                      sourceNode: h.value,
                      sourceHandle: A,
                      targetNode: g.value,
                      targetHandle: z,
                      markerEnd: b.value,
                      markerStart: v.value,
                      connectionStatus: u.value,
                    })
                  : Ce('path', {
                      d: N,
                      class: [l.value.class, u.value, 'vue-flow__connection-path'],
                      style: { ...s.value, ...l.value.style },
                      'marker-end': b.value,
                      'marker-start': v.value,
                    })
              )
            )
          )
        }
      },
    }),
    ZL = KL,
    JL = ['id', 'markerWidth', 'markerHeight', 'markerUnits', 'orient'],
    QL = { name: 'MarkerType', compatConfig: { MODE: 3 } },
    e3 = te({
      ...QL,
      props: {
        id: {},
        type: {},
        color: { default: 'none' },
        width: { default: 12.5 },
        height: { default: 12.5 },
        markerUnits: { default: 'strokeWidth' },
        orient: { default: 'auto-start-reverse' },
        strokeWidth: { default: 1 },
      },
      setup(e) {
        return (t, n) => (
          ee(),
          ve(
            'marker',
            {
              id: t.id,
              class: 'vue-flow__arrowhead',
              viewBox: '-10 -10 20 20',
              refX: '0',
              refY: '0',
              markerWidth: `${t.width}`,
              markerHeight: `${t.height}`,
              markerUnits: t.markerUnits,
              orient: t.orient,
            },
            [
              t.type === K(Wo).ArrowClosed
                ? (ee(),
                  ve(
                    'polyline',
                    {
                      key: 0,
                      style: Ct({ stroke: t.color, fill: t.color, strokeWidth: t.strokeWidth }),
                      'stroke-linecap': 'round',
                      'stroke-linejoin': 'round',
                      points: '-5,-4 0,0 -5,4 -5,-4',
                    },
                    null,
                    4
                  ))
                : Pe('', !0),
              t.type === K(Wo).Arrow
                ? (ee(),
                  ve(
                    'polyline',
                    {
                      key: 1,
                      style: Ct({ stroke: t.color, strokeWidth: t.strokeWidth }),
                      'stroke-linecap': 'round',
                      'stroke-linejoin': 'round',
                      fill: 'none',
                      points: '-5,-4 0,0 -5,4',
                    },
                    null,
                    4
                  ))
                : Pe('', !0),
            ],
            8,
            JL
          )
        )
      },
    }),
    t3 = { class: 'vue-flow__marker vue-flow__container', 'aria-hidden': 'true' },
    n3 = { name: 'MarkerDefinitions', compatConfig: { MODE: 3 } },
    r3 = te({
      ...n3,
      setup(e) {
        const { id: t, edges: n, connectionLineOptions: r, defaultMarkerColor: o } = Ae(),
          i = X(() => {
            const a = new Set(),
              s = [],
              l = (u) => {
                if (u) {
                  const c = zr(u, t)
                  a.has(c) ||
                    (typeof u == 'object'
                      ? s.push({ ...u, id: c, color: u.color || o.value })
                      : s.push({ id: c, color: o.value, type: u }),
                    a.add(c))
                }
              }
            for (const u of [r.value.markerEnd, r.value.markerStart]) l(u)
            for (const u of n.value) for (const c of [u.markerStart, u.markerEnd]) l(c)
            return s.sort((u, c) => u.id.localeCompare(c.id))
          })
        return (a, s) => (
          ee(),
          ve('svg', t3, [
            he('defs', null, [
              (ee(!0),
              ve(
                Re,
                null,
                yn(
                  i.value,
                  (l) => (
                    ee(),
                    ke(
                      e3,
                      {
                        id: l.id,
                        key: l.id,
                        type: l.type,
                        color: l.color,
                        width: l.width,
                        height: l.height,
                        markerUnits: l.markerUnits,
                        'stroke-width': l.strokeWidth,
                        orient: l.orient,
                      },
                      null,
                      8,
                      [
                        'id',
                        'type',
                        'color',
                        'width',
                        'height',
                        'markerUnits',
                        'stroke-width',
                        'orient',
                      ]
                    )
                  )
                ),
                128
              )),
            ]),
          ])
        )
      },
    }),
    o3 = { name: 'Edges', compatConfig: { MODE: 3 } },
    i3 = te({
      ...o3,
      setup(e) {
        const { findNode: t, getEdges: n, elevateEdgesOnSelect: r } = Ae()
        return (o, i) => (
          ee(),
          ve(
            Re,
            null,
            [
              F(r3),
              (ee(!0),
              ve(
                Re,
                null,
                yn(
                  K(n),
                  (a) => (
                    ee(),
                    ve(
                      'svg',
                      {
                        key: a.id,
                        class: 'vue-flow__edges vue-flow__container',
                        style: Ct({ zIndex: K(xz)(a, K(t), K(r)) }),
                      },
                      [F(K(XL), { id: a.id }, null, 8, ['id'])],
                      4
                    )
                  )
                ),
                128
              )),
              F(K(ZL)),
            ],
            64
          )
        )
      },
    }),
    a3 = te({
      name: 'Node',
      compatConfig: { MODE: 3 },
      props: ['id', 'resizeObserver'],
      setup(e) {
        const {
            id: t,
            noPanClassName: n,
            selectNodesOnDrag: r,
            nodesSelectionActive: o,
            multiSelectionActive: i,
            emits: a,
            removeSelectedNodes: s,
            addSelectedNodes: l,
            updateNodeDimensions: u,
            onUpdateNodeInternals: c,
            getNodeTypes: d,
            nodeExtent: f,
            elevateNodesOnSelect: h,
            disableKeyboardA11y: g,
            ariaLiveMessage: m,
            snapToGrid: v,
            snapGrid: b,
            nodeDragThreshold: y,
            nodesDraggable: p,
            elementsSelectable: _,
            nodesConnectable: x,
            nodesFocusable: S,
            hooks: w,
          } = Ae(),
          T = de(null)
        ;(St(AS, T), St(IS, e.id))
        const A = xt(Ai),
          $ = Qe(),
          P = DS(),
          { node: E, parentNode: z } = MS(e.id),
          { emit: C, on: R } = Hz(E, a),
          N = Oe(() => (typeof E.draggable > 'u' ? p.value : E.draggable)),
          j = Oe(() => (typeof E.selectable > 'u' ? _.value : E.selectable)),
          V = Oe(() => (typeof E.connectable > 'u' ? x.value : E.connectable)),
          H = Oe(() => (typeof E.focusable > 'u' ? S.value : E.focusable)),
          G = X(
            () =>
              j.value ||
              N.value ||
              w.value.nodeClick.hasListeners() ||
              w.value.nodeDoubleClick.hasListeners() ||
              w.value.nodeMouseEnter.hasListeners() ||
              w.value.nodeMouseMove.hasListeners() ||
              w.value.nodeMouseLeave.hasListeners()
          ),
          Y = Oe(() => !!E.dimensions.width && !!E.dimensions.height),
          Z = X(() => {
            const q = E.type || 'default',
              I = A?.[`node-${q}`]
            if (I) return I
            let W = E.template || d.value[q]
            if (typeof W == 'string' && $) {
              const ae = Object.keys($.appContext.components)
              ae && ae.includes(q) && (W = f_(q, !1))
            }
            return W && typeof W != 'string' ? W : (a.error(new Le(Be.NODE_TYPE_MISSING, W)), !1)
          }),
          ne = NS({
            id: e.id,
            el: T,
            disabled: () => !N.value,
            selectable: j,
            dragHandle: () => E.dragHandle,
            onStart(q) {
              C.dragStart(q)
            },
            onDrag(q) {
              C.drag(q)
            },
            onStop(q) {
              C.dragStop(q)
            },
            onClick(q) {
              M(q)
            },
          }),
          B = X(() => (E.class instanceof Function ? E.class(E) : E.class)),
          L = X(() => {
            const q = (E.style instanceof Function ? E.style(E) : E.style) || {},
              I = E.width instanceof Function ? E.width(E) : E.width,
              W = E.height instanceof Function ? E.height(E) : E.height
            return (
              !q.width && I && (q.width = typeof I == 'string' ? I : `${I}px`),
              !q.height && W && (q.height = typeof W == 'string' ? W : `${W}px`),
              q
            )
          }),
          k = Oe(() => Number(E.zIndex ?? L.value.zIndex ?? 0))
        return (
          c((q) => {
            ;(q.includes(e.id) || !q.length) && J()
          }),
          Me(() => {
            me(
              () => E.hidden,
              (q = !1, I, W) => {
                !q &&
                  T.value &&
                  (e.resizeObserver.observe(T.value),
                  W(() => {
                    T.value && e.resizeObserver.unobserve(T.value)
                  }))
              },
              { immediate: !0, flush: 'post' }
            )
          }),
          me([() => E.type, () => E.sourcePosition, () => E.targetPosition], () => {
            Ne(() => {
              u([{ id: e.id, nodeElement: T.value, forceUpdate: !0 }])
            })
          }),
          me(
            [
              () => E.position.x,
              () => E.position.y,
              () => {
                var q
                return (q = z.value) == null ? void 0 : q.computedPosition.x
              },
              () => {
                var q
                return (q = z.value) == null ? void 0 : q.computedPosition.y
              },
              () => {
                var q
                return (q = z.value) == null ? void 0 : q.computedPosition.z
              },
              k,
              () => E.selected,
              () => E.dimensions.height,
              () => E.dimensions.width,
              () => {
                var q
                return (q = z.value) == null ? void 0 : q.dimensions.height
              },
              () => {
                var q
                return (q = z.value) == null ? void 0 : q.dimensions.width
              },
            ],
            ([q, I, W, ae, fe, le]) => {
              const ue = { x: q, y: I, z: le + (h.value && E.selected ? 1e3 : 0) }
              typeof W < 'u' && typeof ae < 'u'
                ? (E.computedPosition = mz({ x: W, y: ae, z: fe }, ue))
                : (E.computedPosition = ue)
            },
            { flush: 'post', immediate: !0 }
          ),
          me([() => E.extent, f], ([q, I], [W, ae]) => {
            ;(q !== W || I !== ae) && U()
          }),
          E.extent === 'parent' ||
          (typeof E.extent == 'object' && 'range' in E.extent && E.extent.range === 'parent')
            ? Hd(() => Y)
                .toBe(!0)
                .then(U)
            : U(),
          () =>
            E.hidden
              ? null
              : Ce(
                  'div',
                  {
                    ref: T,
                    'data-id': E.id,
                    class: [
                      'vue-flow__node',
                      `vue-flow__node-${Z.value === !1 ? 'default' : E.type || 'default'}`,
                      {
                        [n.value]: N.value,
                        dragging: ne?.value,
                        draggable: N.value,
                        selected: E.selected,
                        selectable: j.value,
                        parent: E.isParent,
                      },
                      B.value,
                    ],
                    style: {
                      visibility: Y.value ? 'visible' : 'hidden',
                      zIndex: E.computedPosition.z ?? k.value,
                      transform: `translate(${E.computedPosition.x}px,${E.computedPosition.y}px)`,
                      pointerEvents: G.value ? 'all' : 'none',
                      ...L.value,
                    },
                    tabIndex: H.value ? 0 : void 0,
                    role: H.value ? 'group' : void 0,
                    'aria-describedby': g.value ? void 0 : `${hS}-${t}`,
                    'aria-label': E.ariaLabel,
                    'aria-roledescription': 'node',
                    ...E.domAttributes,
                    onMouseenter: re,
                    onMousemove: ie,
                    onMouseleave: _e,
                    onContextmenu: ye,
                    onClick: M,
                    onDblclick: be,
                    onKeydown: O,
                  },
                  [
                    Ce(Z.value === !1 ? d.value.default : Z.value, {
                      id: E.id,
                      type: E.type,
                      data: E.data,
                      events: { ...E.events, ...R },
                      selected: E.selected,
                      resizing: E.resizing,
                      dragging: ne.value,
                      connectable: V.value,
                      position: E.computedPosition,
                      dimensions: E.dimensions,
                      isValidTargetPos: E.isValidTargetPos,
                      isValidSourcePos: E.isValidSourcePos,
                      parent: E.parentNode,
                      parentNodeId: E.parentNode,
                      zIndex: E.computedPosition.z ?? k.value,
                      targetPosition: E.targetPosition,
                      sourcePosition: E.sourcePosition,
                      label: E.label,
                      dragHandle: E.dragHandle,
                      onUpdateNodeInternals: J,
                    }),
                  ]
                )
        )
        function U() {
          const q = E.computedPosition,
            { computedPosition: I, position: W } = ah(
              E,
              v.value ? Ii(q, b.value) : q,
              a.error,
              f.value,
              z.value
            )
          ;((E.computedPosition.x !== I.x || E.computedPosition.y !== I.y) &&
            (E.computedPosition = { ...E.computedPosition, ...I }),
            (E.position.x !== W.x || E.position.y !== W.y) && (E.position = W))
        }
        function J() {
          T.value && u([{ id: e.id, nodeElement: T.value, forceUpdate: !0 }])
        }
        function re(q) {
          ne?.value || C.mouseEnter({ event: q, node: E })
        }
        function ie(q) {
          ne?.value || C.mouseMove({ event: q, node: E })
        }
        function _e(q) {
          ne?.value || C.mouseLeave({ event: q, node: E })
        }
        function ye(q) {
          return C.contextMenu({ event: q, node: E })
        }
        function be(q) {
          return C.doubleClick({ event: q, node: E })
        }
        function M(q) {
          ;(j.value &&
            (!r.value || !N.value || y.value > 0) &&
            Qd(E, i.value, l, s, o, !1, T.value),
            C.click({ event: q, node: E }))
        }
        function O(q) {
          if (!(Zd(q) || g.value))
            if (vS.includes(q.key) && j.value) {
              const I = q.key === 'Escape'
              Qd(E, i.value, l, s, o, I, T.value)
            } else
              N.value &&
                E.selected &&
                zn[q.key] &&
                (q.preventDefault(),
                (m.value = `Moved selected node ${q.key.replace('Arrow', '').toLowerCase()}. New position, x: ${~~E.position.x}, y: ${~~E.position.y}`),
                P({ x: zn[q.key].x, y: zn[q.key].y }, q.shiftKey))
        }
      },
    }),
    s3 = a3
  function l3(e = { includeHiddenNodes: !1 }) {
    const { nodes: t } = Ae()
    return X(() => {
      if (t.value.length === 0) return !1
      for (const n of t.value)
        if (
          (e.includeHiddenNodes || !n.hidden) &&
          (n?.handleBounds === void 0 || n.dimensions.width === 0 || n.dimensions.height === 0)
        )
          return !1
      return !0
    })
  }
  const u3 = { class: 'vue-flow__nodes vue-flow__container' },
    c3 = { name: 'Nodes', compatConfig: { MODE: 3 } },
    d3 = te({
      ...c3,
      setup(e) {
        const { getNodes: t, updateNodeDimensions: n, emits: r } = Ae(),
          o = l3(),
          i = de()
        return (
          me(
            o,
            (a) => {
              a &&
                Ne(() => {
                  r.nodesInitialized(t.value)
                })
            },
            { immediate: !0 }
          ),
          Me(() => {
            i.value = new ResizeObserver((a) => {
              const s = a.map((l) => ({
                id: l.target.getAttribute('data-id'),
                nodeElement: l.target,
                forceUpdate: !0,
              }))
              Ne(() => n(s))
            })
          }),
          je(() => {
            var a
            return (a = i.value) == null ? void 0 : a.disconnect()
          }),
          (a, s) => (
            ee(),
            ve('div', u3, [
              i.value
                ? (ee(!0),
                  ve(
                    Re,
                    { key: 0 },
                    yn(
                      K(t),
                      (l, u, c, d) => {
                        const f = [l.id]
                        if (d && d.key === l.id && Ox(d, f)) return d
                        const h =
                          (ee(),
                          ke(K(s3), { id: l.id, key: l.id, 'resize-observer': i.value }, null, 8, [
                            'id',
                            'resize-observer',
                          ]))
                        return ((h.memo = f), h)
                      },
                      s,
                      0
                    ),
                    128
                  ))
                : Pe('', !0),
            ])
          )
        )
      },
    })
  function f3() {
    const { emits: e } = Ae()
    Me(() => {
      if (PS()) {
        const t = document.querySelector('.vue-flow__pane')
        t && window.getComputedStyle(t).zIndex !== '1' && e.error(new Le(Be.MISSING_STYLES))
      }
    })
  }
  const h3 = he('div', { class: 'vue-flow__edge-labels' }, null, -1),
    p3 = { name: 'VueFlow', compatConfig: { MODE: 3 } },
    v3 = te({
      ...p3,
      props: {
        id: {},
        modelValue: {},
        nodes: {},
        edges: {},
        edgeTypes: {},
        nodeTypes: {},
        connectionMode: {},
        connectionLineType: {},
        connectionLineStyle: { default: void 0 },
        connectionLineOptions: { default: void 0 },
        connectionRadius: {},
        isValidConnection: { type: [Function, null], default: void 0 },
        deleteKeyCode: { default: void 0 },
        selectionKeyCode: { type: [Boolean, null], default: void 0 },
        multiSelectionKeyCode: { default: void 0 },
        zoomActivationKeyCode: { default: void 0 },
        panActivationKeyCode: { default: void 0 },
        snapToGrid: { type: Boolean, default: void 0 },
        snapGrid: {},
        onlyRenderVisibleElements: { type: Boolean, default: void 0 },
        edgesUpdatable: { type: [Boolean, String], default: void 0 },
        nodesDraggable: { type: Boolean, default: void 0 },
        nodesConnectable: { type: Boolean, default: void 0 },
        nodeDragThreshold: {},
        elementsSelectable: { type: Boolean, default: void 0 },
        selectNodesOnDrag: { type: Boolean, default: void 0 },
        panOnDrag: { type: [Boolean, Array], default: void 0 },
        minZoom: {},
        maxZoom: {},
        defaultViewport: {},
        translateExtent: {},
        nodeExtent: {},
        defaultMarkerColor: {},
        zoomOnScroll: { type: Boolean, default: void 0 },
        zoomOnPinch: { type: Boolean, default: void 0 },
        panOnScroll: { type: Boolean, default: void 0 },
        panOnScrollSpeed: {},
        panOnScrollMode: {},
        paneClickDistance: {},
        zoomOnDoubleClick: { type: Boolean, default: void 0 },
        preventScrolling: { type: Boolean, default: void 0 },
        selectionMode: {},
        edgeUpdaterRadius: {},
        fitViewOnInit: { type: Boolean, default: void 0 },
        connectOnClick: { type: Boolean, default: void 0 },
        applyDefault: { type: Boolean, default: void 0 },
        autoConnect: { type: [Boolean, Function], default: void 0 },
        noDragClassName: {},
        noWheelClassName: {},
        noPanClassName: {},
        defaultEdgeOptions: {},
        elevateEdgesOnSelect: { type: Boolean, default: void 0 },
        elevateNodesOnSelect: { type: Boolean, default: void 0 },
        disableKeyboardA11y: { type: Boolean, default: void 0 },
        edgesFocusable: { type: Boolean, default: void 0 },
        nodesFocusable: { type: Boolean, default: void 0 },
        autoPanOnConnect: { type: Boolean, default: void 0 },
        autoPanOnNodeDrag: { type: Boolean, default: void 0 },
        autoPanSpeed: {},
      },
      emits: [
        'nodesChange',
        'edgesChange',
        'nodesInitialized',
        'paneReady',
        'init',
        'updateNodeInternals',
        'error',
        'connect',
        'connectStart',
        'connectEnd',
        'clickConnectStart',
        'clickConnectEnd',
        'moveStart',
        'move',
        'moveEnd',
        'selectionDragStart',
        'selectionDrag',
        'selectionDragStop',
        'selectionContextMenu',
        'selectionStart',
        'selectionEnd',
        'viewportChangeStart',
        'viewportChange',
        'viewportChangeEnd',
        'paneScroll',
        'paneClick',
        'paneContextMenu',
        'paneMouseEnter',
        'paneMouseMove',
        'paneMouseLeave',
        'edgeUpdate',
        'edgeContextMenu',
        'edgeMouseEnter',
        'edgeMouseMove',
        'edgeMouseLeave',
        'edgeDoubleClick',
        'edgeClick',
        'edgeUpdateStart',
        'edgeUpdateEnd',
        'nodeContextMenu',
        'nodeMouseEnter',
        'nodeMouseMove',
        'nodeMouseLeave',
        'nodeDoubleClick',
        'nodeClick',
        'nodeDragStart',
        'nodeDrag',
        'nodeDragStop',
        'miniMapNodeClick',
        'miniMapNodeDoubleClick',
        'miniMapNodeMouseEnter',
        'miniMapNodeMouseMove',
        'miniMapNodeMouseLeave',
        'update:modelValue',
        'update:nodes',
        'update:edges',
      ],
      setup(e, { expose: t, emit: n }) {
        const r = e,
          o = Ex(),
          i = hd(r, 'modelValue', n),
          a = hd(r, 'nodes', n),
          s = hd(r, 'edges', n),
          l = Ae(r),
          u = Wz({ modelValue: i, nodes: a, edges: s }, r, l)
        return (
          Yz(n, l.hooks),
          GL(),
          f3(),
          St(Ai, o),
          Jo(u),
          t(l),
          (c, d) => (
            ee(),
            ve(
              'div',
              { ref: K(l).vueFlowRef, class: 'vue-flow' },
              [
                F(LL, null, {
                  default: Ve(() => [F(i3), h3, F(d3), bt(c.$slots, 'zoom-pane')]),
                  _: 3,
                }),
                bt(c.$slots, 'default'),
                F(VL),
              ],
              512
            )
          )
        )
      },
    })
  var Rt = ((e) => ((e.Lines = 'lines'), (e.Dots = 'dots'), e))(Rt || {})
  const HS = function ({ dimensions: e, size: t, color: n }) {
      return Ce('path', {
        stroke: n,
        'stroke-width': t,
        d: `M${e[0] / 2} 0 V${e[1]} M0 ${e[1] / 2} H${e[0]}`,
      })
    },
    jS = function ({ radius: e, color: t }) {
      return Ce('circle', { cx: e, cy: e, r: e, fill: t })
    }
  ;(Rt.Lines + '', Rt.Dots + '')
  const g3 = { [Rt.Dots]: '#81818a', [Rt.Lines]: '#eee' },
    m3 = ['id', 'x', 'y', 'width', 'height', 'patternTransform'],
    y3 = { key: 2, height: '100', width: '100' },
    b3 = ['fill'],
    _3 = ['x', 'y', 'fill'],
    w3 = { name: 'Background', compatConfig: { MODE: 3 } },
    S3 = te({
      ...w3,
      props: {
        id: {},
        variant: { default: () => Rt.Dots },
        gap: { default: 20 },
        size: { default: 1 },
        lineWidth: { default: 1 },
        patternColor: {},
        color: {},
        bgColor: {},
        height: { default: 100 },
        width: { default: 100 },
        x: { default: 0 },
        y: { default: 0 },
        offset: { default: 0 },
      },
      setup(e) {
        const { id: t, viewport: n } = Ae(),
          r = X(() => {
            const a = n.value.zoom,
              [s, l] = Array.isArray(e.gap) ? e.gap : [e.gap, e.gap],
              u = [s * a || 1, l * a || 1],
              c = e.size * a,
              [d, f] = Array.isArray(e.offset) ? e.offset : [e.offset, e.offset],
              h = [d * a || 1 + u[0] / 2, f * a || 1 + u[1] / 2]
            return { scaledGap: u, offset: h, size: c }
          }),
          o = Oe(() => `pattern-${t}${e.id ? `-${e.id}` : ''}`),
          i = Oe(() => e.color || e.patternColor || g3[e.variant || Rt.Dots])
        return (a, s) => (
          ee(),
          ve(
            'svg',
            {
              class: 'vue-flow__background vue-flow__container',
              style: Ct({
                height: `${a.height > 100 ? 100 : a.height}%`,
                width: `${a.width > 100 ? 100 : a.width}%`,
              }),
            },
            [
              bt(a.$slots, 'pattern-container', { id: o.value }, () => [
                he(
                  'pattern',
                  {
                    id: o.value,
                    x: K(n).x % r.value.scaledGap[0],
                    y: K(n).y % r.value.scaledGap[1],
                    width: r.value.scaledGap[0],
                    height: r.value.scaledGap[1],
                    patternTransform: `translate(-${r.value.offset[0]},-${r.value.offset[1]})`,
                    patternUnits: 'userSpaceOnUse',
                  },
                  [
                    bt(a.$slots, 'pattern', {}, () => [
                      a.variant === K(Rt).Lines
                        ? (ee(),
                          ke(
                            K(HS),
                            {
                              key: 0,
                              size: a.lineWidth,
                              color: i.value,
                              dimensions: r.value.scaledGap,
                            },
                            null,
                            8,
                            ['size', 'color', 'dimensions']
                          ))
                        : a.variant === K(Rt).Dots
                          ? (ee(),
                            ke(
                              K(jS),
                              { key: 1, color: i.value, radius: r.value.size / 2 },
                              null,
                              8,
                              ['color', 'radius']
                            ))
                          : Pe('', !0),
                      a.bgColor
                        ? (ee(),
                          ve('svg', y3, [
                            he(
                              'rect',
                              { width: '100%', height: '100%', fill: a.bgColor },
                              null,
                              8,
                              b3
                            ),
                          ]))
                        : Pe('', !0),
                    ]),
                  ],
                  8,
                  m3
                ),
              ]),
              he(
                'rect',
                { x: a.x, y: a.y, width: '100%', height: '100%', fill: `url(#${o.value})` },
                null,
                8,
                _3
              ),
              bt(a.$slots, 'default', { id: o.value }),
            ],
            4
          )
        )
      },
    }),
    x3 = { class: 'signal-viewer' },
    C3 = { class: 'signal-viewer__header' },
    E3 = { class: 'signal-viewer__title-row' },
    $3 = { class: 'signal-viewer__title' },
    T3 = { key: 0, class: 'signal-viewer__session' },
    O3 = { class: 'signal-viewer__session-id' },
    P3 = { class: 'signal-viewer__count' },
    I3 = { class: 'signal-viewer__canvas' },
    A3 = { key: 1, class: 'signal-viewer__empty' },
    N3 = te({
      __name: 'SignalViewer',
      setup(e) {
        const t = Kf(),
          { flowNodes: n, flowEdges: r, activeSession: o } = uf(t),
          { fitView: i } = Ae()
        me(
          () => n.value.length,
          (d, f) => {
            d > 0 &&
              d !== f &&
              setTimeout(() => {
                i({ duration: 300 })
              }, 300)
          }
        )
        const a = X(() => o.value?.id || null),
          s = () => {
            a.value ? (t.sendInterrupt(), Po.success('已发送打断信号')) : Po.error('请先选择会话')
          },
          l = X(() =>
            n.value.map((d) => ({
              ...d,
              type: 'handler',
              class: d.data.status === 'active' ? 'node-active' : 'node-inactive',
            }))
          ),
          u = X(() =>
            r.value.map((d) => ({
              ...d,
              type: 'smoothstep',
              sourceHandle: 'right',
              targetHandle: 'left',
              style: {
                stroke: d.animated ? '#22c55e' : '#94a3b8',
                strokeWidth: d.animated ? 2 : 1,
              },
              markerEnd: { type: Wo.ArrowClosed, color: d.animated ? '#22c55e' : '#94a3b8' },
            }))
          ),
          c = te({
            name: 'HandlerNode',
            props: { data: { type: Object, required: !0 } },
            setup(d) {
              const f = () => {
                switch (d.data.status) {
                  case 'active':
                    return 'handler-node--active'
                  case 'timeout':
                    return 'handler-node--timeout'
                  default:
                    return 'handler-node--inactive'
                }
              }
              return () =>
                Ce('div', { class: ['handler-node', f()] }, [
                  Ce(Yn, {
                    id: 'left',
                    type: 'target',
                    position: pe.Left,
                    style: { left: '-6px', top: '50%', transform: 'translateY(-50%)' },
                  }),
                  Ce('div', { class: 'handler-node__status' }),
                  Ce('div', { class: 'handler-node__content' }, [
                    Ce('div', { class: 'handler-node__label' }, d.data.label),
                    Ce(
                      'div',
                      { class: 'handler-node__type' },
                      d.data.endTime && d.data.startTime
                        ? `耗时: ${Math.floor((d.data.endTime - d.data.startTime) * 1e3)}ms`
                        : '暂无耗时数据'
                    ),
                  ]),
                  Ce(Yn, {
                    id: 'right',
                    type: 'source',
                    position: pe.Right,
                    style: { right: '-6px', top: '50%', transform: 'translateY(-50%)' },
                  }),
                ])
            },
          })
        return (d, f) => (
          ee(),
          ve('div', x3, [
            he('div', C3, [
              he('div', E3, [
                he('h3', $3, [
                  f[1] || (f[1] = Xt(' 信号流图 ', -1)),
                  a.value
                    ? (ee(),
                      ve('span', T3, [
                        f[0] ||
                          (f[0] = he(
                            'span',
                            { class: 'signal-viewer__session-label' },
                            'Session:',
                            -1
                          )),
                        he('span', O3, ze(a.value), 1),
                        he(
                          'button',
                          {
                            class: 'signal-viewer__action-btn signal-viewer__action-btn--danger',
                            title: '发送打断信号',
                            onClick: s,
                          },
                          ' 打断 '
                        ),
                      ]))
                    : Pe('', !0),
                ]),
                he('span', P3, ze(l.value.length) + ' 节点', 1),
              ]),
            ]),
            he('div', I3, [
              l.value.length > 0
                ? (ee(),
                  ke(
                    K(v3),
                    {
                      key: 0,
                      nodes: l.value,
                      edges: u.value,
                      'nodes-draggable': !0,
                      'edges-updatable': !1,
                      'nodes-connectable': !1,
                      'edges-deletable': !1,
                      'edges-movable': !1,
                      'edges-selectable': !1,
                      'edges-stylable': !1,
                      'fit-view-on-init': !0,
                      'default-viewport': { zoom: 0.8 },
                      class: 'vue-flow-container',
                    },
                    {
                      'node-handler': Ve((h) => [F(K(c), { data: h.data }, null, 8, ['data'])]),
                      default: Ve(() => [
                        F(K(S3), { gap: 16, size: 1, 'pattern-color': '#e5e7eb' }),
                      ]),
                      _: 1,
                    },
                    8,
                    ['nodes', 'edges']
                  ))
                : (ee(),
                  ve('div', A3, [
                    ...(f[2] ||
                      (f[2] = [
                        he('div', { class: 'signal-viewer__empty-icon' }, '📡', -1),
                        he('p', null, '等待信号数据...', -1),
                      ])),
                  ])),
            ]),
            f[3] ||
              (f[3] = Rx(
                '<div class="signal-viewer__legend" data-v-3c7259a4><div class="legend-item" data-v-3c7259a4><span class="legend-dot legend-dot--active" data-v-3c7259a4></span><span data-v-3c7259a4>数据产生中</span></div><div class="legend-item" data-v-3c7259a4><span class="legend-dot legend-dot--inactive" data-v-3c7259a4></span><span data-v-3c7259a4>已完成</span></div><div class="legend-item" data-v-3c7259a4><span class="legend-dot legend-dot--timeout" data-v-3c7259a4></span><span data-v-3c7259a4>超时(&gt;10s)</span></div><div class="legend-item" data-v-3c7259a4><span class="legend-line legend-line--animated" data-v-3c7259a4></span><span data-v-3c7259a4>数据流动</span></div></div>',
                1
              )),
          ])
        )
      },
    }),
    R3 = xn(N3, [['__scopeId', 'data-v-3c7259a4']]),
    M3 = { class: 'current-config-viewer' },
    D3 = { class: 'current-config-viewer__header' },
    B3 = { key: 0, class: 'current-config-viewer__meta' },
    q3 = { key: 0, class: 'current-config-viewer__empty' },
    z3 = { class: 'current-config-viewer__summary' },
    L3 = { class: 'current-config-viewer__handler-tags' },
    F3 = { class: 'current-config-viewer__json' },
    k3 = { key: 1, class: 'current-config-viewer__empty-tip' },
    H3 = te({
      __name: 'CurrentConfigViewer',
      setup(e) {
        const t = Kf(),
          { currentConfig: n } = uf(t),
          r = X(() => {
            const o = n.value?.handler_configs
            return o
              ? Object.entries(o)
                  .map(([i, a]) => ({
                    name: i,
                    display: JSON.stringify(a || {}, null, 2),
                    fields: Object.keys(a || {}),
                  }))
                  .sort((i, a) => i.name.localeCompare(a.name))
              : []
          })
        return (o, i) => (
          ee(),
          ve('section', M3, [
            he('div', D3, [
              i[0] || (i[0] = he('h3', { class: 'current-config-viewer__title' }, '当前配置', -1)),
              K(n)?.model_root
                ? (ee(), ve('span', B3, ' model_root: ' + ze(K(n).model_root), 1))
                : Pe('', !0),
              typeof K(n)?.concurrent_limit == 'number'
                ? (ee(),
                  ke(
                    K(vn),
                    { key: 1, color: 'blue' },
                    { default: Ve(() => [Xt(' 并发上限 ' + ze(K(n).concurrent_limit), 1)]), _: 1 }
                  ))
                : Pe('', !0),
            ]),
            K(n)
              ? (ee(),
                ve(
                  Re,
                  { key: 1 },
                  [
                    he('div', z3, 'handler 数量：' + ze(r.value.length), 1),
                    r.value.length > 0
                      ? (ee(),
                        ke(
                          K(Dn),
                          {
                            key: 0,
                            class: 'current-config-viewer__collapse',
                            bordered: !1,
                            'expand-icon-position': 'end',
                          },
                          {
                            default: Ve(() => [
                              (ee(!0),
                              ve(
                                Re,
                                null,
                                yn(
                                  r.value,
                                  (a) => (
                                    ee(),
                                    ke(
                                      K(Dn).Panel,
                                      {
                                        key: a.name,
                                        header: `${a.name}（${a.fields.length} 个字段）`,
                                      },
                                      {
                                        default: Ve(() => [
                                          he('div', L3, [
                                            a.fields.length === 0
                                              ? (ee(),
                                                ke(
                                                  K(vn),
                                                  { key: 0, color: 'default' },
                                                  {
                                                    default: Ve(() => [
                                                      ...(i[1] || (i[1] = [Xt('空配置', -1)])),
                                                    ]),
                                                    _: 1,
                                                  }
                                                ))
                                              : Pe('', !0),
                                            (ee(!0),
                                            ve(
                                              Re,
                                              null,
                                              yn(
                                                a.fields,
                                                (s) => (
                                                  ee(),
                                                  ke(
                                                    K(vn),
                                                    { key: s, color: 'processing' },
                                                    { default: Ve(() => [Xt(ze(s), 1)]), _: 2 },
                                                    1024
                                                  )
                                                )
                                              ),
                                              128
                                            )),
                                          ]),
                                          he('pre', F3, ze(a.display), 1),
                                        ]),
                                        _: 2,
                                      },
                                      1032,
                                      ['header']
                                    )
                                  )
                                ),
                                128
                              )),
                            ]),
                            _: 1,
                          }
                        ))
                      : (ee(), ve('div', k3, '当前配置未包含 handler_configs')),
                  ],
                  64
                ))
              : (ee(), ve('div', q3, [F(K(Mx), { description: '等待 current_config 消息...' })])),
          ])
        )
      },
    }),
    j3 = xn(H3, [['__scopeId', 'data-v-5f8a5430']]),
    V3 = { class: 'manager' },
    G3 = { key: 0, class: 'manager__error' },
    W3 = { class: 'manager__content' },
    U3 = { class: 'manager__content-left' },
    Y3 = { class: 'manager__detail' },
    X3 = { key: 0, class: 'manager__empty' },
    K3 = { class: 'manager__content-right' },
    Z3 = te({
      __name: 'index',
      setup(e) {
        const t = Kf(),
          {
            status: n,
            connectionError: r,
            sortedSessions: o,
            activeSession: i,
            activeChatMessages: a,
            currentTime: s,
          } = uf(t),
          { reconnect: l, selectSession: u, removeSession: c } = t
        return (
          Me(() => {
            t.start()
          }),
          je(() => {
            t.stop()
          }),
          (d, f) => (
            ee(),
            ve('div', V3, [
              F(
                bM,
                {
                  status: K(n),
                  'status-text-map': K(dM),
                  'status-class-map': K(fM),
                  onReconnect: K(l),
                },
                null,
                8,
                ['status', 'status-text-map', 'status-class-map', 'onReconnect']
              ),
              K(r) ? (ee(), ve('section', G3, ze(K(r)), 1)) : Pe('', !0),
              he('section', W3, [
                he('div', U3, [
                  F(
                    lD,
                    {
                      sessions: K(o),
                      'active-session-id': K(i)?.id || void 0,
                      now: K(s),
                      onSelect: K(u),
                      onClose: K(c),
                    },
                    null,
                    8,
                    ['sessions', 'active-session-id', 'now', 'onSelect', 'onClose']
                  ),
                  he('main', Y3, [
                    K(i)
                      ? (ee(), ke(ZM, { key: 1, messages: K(a) }, null, 8, ['messages']))
                      : (ee(), ve('div', X3, '请选择或等待会话出现')),
                  ]),
                ]),
                he('div', K3, [F(R3), F(j3)]),
              ]),
            ])
          )
        )
      },
    }),
    J3 = xn(Z3, [['__scopeId', 'data-v-32e21815']]),
    Q3 = te({
      __name: 'ManagerApp',
      setup(e) {
        return (t, n) => (ee(), ke(J3))
      },
    }),
    VS = Dx(Q3),
    eF = Bx()
  VS.use(eF)
  VS.mount('#manager-app')
})
export default tF()

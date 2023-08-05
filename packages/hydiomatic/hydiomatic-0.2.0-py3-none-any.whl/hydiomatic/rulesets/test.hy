(import [adderall.dsl [*]])
(require [adderall.dsl [*]])

(setv import-expr
      '(import [argparse]))

;; hydiomatic...
(defn hydiomatic [test-expr]
  (setv mini-kanren-res
        (run* [out]
             (fresh [match]
                    (== test-expr `(import [~match]))
                    (== `(import ~match) out))))
  (print (get mini-kanren-res 0)))

(hydiomatic import-expr)

(define (domain nosliw)
  (:requirements :strips :typing)
  (:types
    location movable - object
    agent item - movable
    dragon hero wizard - agent
    sorceress - wizard
    sword pen diamond - item
    town mountain cave - location)
  (:predicates
    (at ?movable - movable ?location - location)
    (different ?d1 - diamond ?d2 - diamond)
    (possesses ?agent - agent ?item - item)
    (path-from-to ?from - location ?to - location)
    (asleep ?dragon - dragon)
    (dead ?dragon - dragon)
    (safe ?town - town)
    (strong ?hero - hero))

  (:action travel
	     :parameters (?hero - hero ?from - location ?to - location)
	     :precondition (and (at ?hero ?from) (path-from-to ?from ?to))
	     :effect (and (not (at ?hero ?from)) (at ?hero ?to)))

  (:action trade
       :parameters (?from - agent ?to - agent ?i1 - item ?i2 - item ?l - location)
       :precondition (and (possesses ?from ?i1) (possesses ?to ?i2)
                          (at ?from ?l) (at ?to ?l))
       :effect (and (not (possesses ?from ?i1)) (not (possesses ?to ?i2))
                    (possesses ?from ?i2) (possesses ?to ?i1)))

  (:action pick
       :parameters (?hero - hero ?item - item ?location - location)
       :precondition (and (at ?hero ?location) (at ?item ?location))
       :effect (and (not (at ?item ?location)) (possesses ?hero ?item)))

  (:action drop
       :parameters (?hero - hero ?item - item ?location - location)
       :precondition (and (at ?hero ?location) (possesses ?hero ?item))
       :effect (and (not (possesses ?hero ?item)) (at ?item ?location)))

  (:action strengthen
       :parameters (?hero - hero ?wizard - wizard ?location - location ?d1 - diamond ?d2 - diamond ?d3 - diamond)
       :precondition (and (possesses ?hero ?d1) (possesses ?hero ?d2) (possesses ?hero ?d3)
                          (different ?d1 ?d2) (different ?d1 ?d3) (different ?d2 ?d3)
                          (at ?hero ?location) (at ?wizard ?location))
       :effect (and (possesses ?wizard ?d1) (possesses ?wizard ?d2) (possesses ?wizard ?d3)
                    (not (possesses ?hero ?d1)) (not(possesses ?hero ?d2)) (not(possesses ?hero ?d3))
                    (strong ?hero)))

  (:action kill
       :parameters (?hero - hero ?dragon - dragon ?location - location ?sword - sword)
       :precondition (and (strong ?hero) (at ?hero ?location) (at ?dragon ?location)
                          (possesses ?hero ?sword) (not (dead ?dragon)))
       :effect (and (not (at ?dragon ?location)) (dead ?dragon) (safe happydale)))

  (:action hypnotise
       :parameters (?hero - hero ?dragon - dragon ?pen - pen)
       :precondition (and (possesses ?hero ?pen) (not (dead ?dragon)) (not (asleep ?dragon)))
       :effect (and (asleep ?dragon) (safe happydale)))
)

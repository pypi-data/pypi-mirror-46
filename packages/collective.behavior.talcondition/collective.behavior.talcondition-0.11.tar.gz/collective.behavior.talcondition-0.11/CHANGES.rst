Changelog
=========


0.11 (2019-05-16)
-----------------

- Added parameter `raise_on_error` to `utils.evaluateExpressionFor` to raise an
  error when an exception occurs instead returning False.
  [gbastien]
- Added method `TALCondition.complete_extra_expr_ctx` to the behavior to
  formalize the way to get `extra_expr_ctx` to avoid the `evaluate` method
  to be overrided.
  [gbastien]

0.10 (2018-11-20)
-----------------

- Do not break if parameter `expression` passed to
  `utils._evaluateExpression` is None.
  [gbastien]

0.9 (2018-10-12)
----------------

- Added new parameter `error_pattern=WRONG_TAL_CONDITION` to
  `utils.evaluateExpressionFor` and underlying `utils._evaluateExpression` to
  be able to log a custom message in case an error occurs during
  expression evaluation.
  [gbastien]

0.8 (2018-06-12)
----------------

- Mark elements using behavior with `ITALConditionable` interface so it behaves
  like element using the AT extender.
  [gbastien]

0.7 (2017-03-22)
----------------

- Use CheckBoxWidget for `ITALCondition.roles_bypassing_talcondition` to ease
  selection when displaying several elements.
  [gbastien]

0.6 (2016-01-12)
----------------

- Added parameter `empty_expr_is_true` to utils._evaluateExpression than may be True
  or False depending that we want an empty expression to be considered True or False.
  Previous behavior is kept in utils.evaluateExpressionFor where an empty expression
  is considered True.  This avoid managing an empty expression in the caller method
  [gbastien]


0.5 (2015-12-17)
----------------

- Added method utils._evaluateExpression that receives an expression
  to evaluate, it is called by utils.evaluateExpressionFor.  This way, this
  method may evaluate a TAL expression without getting it from the `tal_condition`
  attribute on the context, in case we want to evaluate arbitrary expression
  [gbastien]


0.4 (2015-09-16)
----------------

- Make the tal_condition field larger (from 30 to 80) for the
  AT extender as well as for the DX behavior
  [gbastien]
- Added possibility to extend TAL expression context by passing
  an `extra_expr_ctx` dict to utils.evaluateExpressionFor, also
  integrated to the `evaluate` method of the DX behavior
  [gbastien]


0.3 (2015-07-14)
----------------

- Corrected default value
  [sgeulette]
- Little optimization
  [sgeulette]


0.2 (2015-06-18)
----------------

- Added field `role_bypassing_talcondition` to define who can bypass the condition
  [anuyens]
- Added translations for new field
  [gbastien]


0.1 (2015-06-01)
----------------

- Initial release.
  [IMIO]

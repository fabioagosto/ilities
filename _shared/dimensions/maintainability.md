*Will this be cheap to change in six months?*
- **Signals:** modular, with clear boundaries; each unit does one well-defined thing
  (high cohesion); dependencies between components are minimal and explicit (loose
  coupling); no hidden state.
- **Smells:** god functions/classes; spooky action at a distance; a change here forcing
  edits in five unrelated places.
- *Absorbs modularity, cohesion, loose coupling, and portability; call them out by
  name in a finding when one is the specific problem.*
# Optomotor Console

A self-contained, single-file browser toy that simulates a fly's compound eye
watching a moving stimulus, and drives a simple animated fly's steering from
that visual input in real time.

Open `index.html` directly in a browser — no build step, no dependencies.

## Background

This started from a GIGAZINE article about
[FlyWire](https://flywire.ai), the Princeton-led consortium that produced the
first complete connectome (full wiring diagram) of the *Drosophila
melanogaster* brain — roughly 140,000 neurons and their synapses. That dataset
is far too large to simulate in a browser tab, so this project is not a
literal connectome simulation. Instead it models the specific, well-studied
circuit responsible for one of the fly's most famous visual behaviors: the
**optomotor reflex**, the reaction that keeps a fly's gaze/heading stable
against the visual world.

## How it works

1. **Retina** — a stimulus (a moving grating, a looming disc, a rotating
   pattern, static noise, or a video file you upload) is sampled by a
   24×12 grid of simulated ommatidia (a real fly eye has roughly 700–800
   per side).
2. **Optic lobe** — each pair of neighboring ommatidia feeds a
   [Hassenstein–Reichardt correlator](https://en.wikipedia.org/wiki/Reichardt_detector):
   the textbook elementary-motion-detector circuit in fly vision. Raw signal
   from one ommatidium is multiplied against a time-delayed signal from its
   neighbor, mirrored, and subtracted — giving a signed local motion estimate.
   These are pooled the way real lobula-plate tangential cells (HS/VS) pool
   local detectors into a wide-field turn signal.
3. **Descending neurons → motor** — the pooled signal drives the simulated
   fly's angular velocity (turn signal) and forward speed (from overall
   retinal flux, as a stand-in for looming/arousal-driven thrust), animated
   in the flight arena panel.
4. **Telemetry** — both signals are plotted live over the trailing 8 seconds.

## Controls

- **Stimulus presets** — canonical vision-science stimuli: drifting gratings
  (left/right), a looming disc, a rotating pattern, and a static-noise control
  (no coherent motion, so the turn signal should hover near zero).
- **Load video…** — feed your own video file through the same pipeline.
- **Eye gain / Turn gain / Stimulus speed** — sliders to tune sensitivity.

## Caveats

This is a simplified, illustrative model for play and intuition-building, not
a research-grade simulation of fly neurobiology or of the actual FlyWire
connectome.

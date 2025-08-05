# System Prompt

## Role

Elite python developer in the geoprocessing field

## Formatting

- Always provide a new jupyter notebook from scratch with markdown formatting.
- Always load all needed data for the analysis requested.
- **Do not** include cell outputs in the jupyter notebook. 

## Constraints

- You always produce an extensive, complete and **finalized** jupyter notebook with the requested analysis.
- You must explore and visualize the analysis and results extensively, performing and allowing throughout evaluation of the methods apply.
- Use creative and cirurgical markdown reports, tables, maps and charts **ready for publication in renowed academic journals**. 
- Always create a new jupyter notebook from scratch: **Do not** continue from the current code base. 

## Current Code Base

You may continue developing the code base using this code as a reference.

Below is the current code, a jupyter notebook exported to markdown format:

{{build-thiessen-polygons.ipynb}} // Notebook as markdown

---

# User Prompt (Find periods with the most rain)

Develop three analysis focused on grouping days or periods with presence of rain and finding the ones with the most significant rain, in the city or Rio de Janeiro.

The three analysis are:

- Based on days: Find the days with rain and the ones with the most rain.
- Based on periods: Find the periods with rain and the ones with the most rain. The idea here is to group intervals of time that represent a single rain (when a rain started and stopped in the city), and find the intervals with the most rain.
- Another method suggested by you to accomplish the intended task. If possible, suggest a known academic method used specifically for pluviometric precipitation data.

---

# User Prompt (Evaluate and compare methods to find periods with the most rain)

Implement a compreensive evaluation and comparison analysis, evaluating extensively in multilpe ways each of the three methods for finding periods with the most rain and, next, compare them against each other in multiple ways.
Constrains

- Continue from the end of the current code base.

Current Code Base Outputs

The outputs of the current code base are attached as images for your reference.

{{images_attached}}

---

## User Prompt (Maps in a grid for each of the top 10 rain events)

Implement a focused visualization analysis with maps in a grid for each of the top 10 rain events.

First, decide which of three methods used to find the periods with most rains generated the best results.

Then, for each of the top 10 rain events, create a grid of maps each map representing a one hour period of the event. Each map must have the thiessen polygons colored by the one hour precipitation of the station associated with the polygon. Each map must also have the flood ocorrences present in that hour as points.
Context

Note that a flood ocorrence has a time of start and end. The event point should be in a map if its period in time intersects with the hour period of the map. Use the entire
Constraints

    Consider all records in the 'ocorrencias' dataframe as flood events.

    If a rain period has more than 10 hours, find the best consecutive 10 hours to use for the visualization.

Format

Continue exactly from where the current base is. There is no need to reload variables or check if they exist.
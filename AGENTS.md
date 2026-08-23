# Notes for agents working on the down counters

## Always hand back an Onshape cleanup list

**If you create anything in Onshape that you cannot delete yourself, tell the
owner exactly what to delete before you finish. Do not leave it unmentioned.**

The owner wants to know what needs cleaning up. An orphan you do not name is an
orphan they will never find — it will sit in the document until someone else
trips over it and has to work out whether it is load-bearing.

This is not hypothetical. The Onshape MCP plugin exposes `delete_feature`,
`delete_feature_by_name` and `delete_document`, but **no tool that deletes an
element**. Every call to `write_featurescript_feature` creates a new Feature
Studio element in the document, and each iteration leaves the previous one
behind. Deleting the *feature* does not delete the Feature Studio that carried
its source. The 2026-08-22 lug session left four orphaned Feature Studios this
way, out of six created.

Orphans are not free here: the account sits at the Onshape free-tier
**10-document cap**, so clutter has a real cost and `create_document` already
returns 409.

### What a cleanup handoff must contain

Before you finish, verify and then report:

1. Run `get_elements` to list what is actually in the document now.
2. Run `describe_part_studio` and read the feature tree, so you know which
   elements are still referenced.
3. Give the owner two explicit lists — **safe to delete** and **must stay** —
   each entry with both the element name and its ID, since generated names
   differ only by a trailing digit (`ClaudeFS_watchLugs` vs
   `ClaudeFS_watchLugs2`) and picking the wrong one breaks the model.
4. Say plainly that the deletion has to happen in the Onshape UI, because the
   API cannot do it.

Never advise deleting something you have not confirmed is unreferenced.

### Do not reach for `delete_document`

It trashes an entire document and is irreversible via the API. It is for
throwaway documents an agent created itself. It is never the answer to
"clean up the leftover Feature Studios", and it must not be called on
`00b1e7c9d07aec2789568fab` or `3db840dfeff4095d8508aa97`.

### The same rule applies beyond Onshape

Any external system where you lack delete permission — files you cannot remove,
cloud resources, generated artefacts — gets the same treatment: name what you
left behind and where, rather than leaving the owner to discover it.

## Reusing `fsElementName` does not reuse the element

Reissuing a feature under an existing `fsElementName` creates a **new** Feature
Studio element that happens to share the name. Verified 2026-08-22: reissuing
`Watch lugs` as `ClaudeFS_watchLugs2` returned element `058db78c…` while the
old `ClaudeFS_watchLugs2` (`cf2f7f85…`) stayed in the document. The result is
two tabs with byte-identical names, one live and one dead, which is worse for
the owner than an obviously-stale name.

So: **give every write a unique `fsElementName`** — add a version or date
suffix — and hand back element **IDs**, not names, in the cleanup list. The
only reliable way to tell same-named tabs apart in the UI is to open each one
and read the `/e/<id>` segment of the URL.

Check `get_elements` after any reissue, precisely because the orphan is
invisible in the returned `ok` status; the giveaway is that the response's
`fs_element_id` differs from the element you meant to reuse.

## Two traps specific to this document

- **`create_extrude` and `create_offset_plane` return HTTP 400** on the working
  copy for every argument combination — bare-number and unit-string values, NEW
  and ADD, required-parameters-only. `create_sketch` works on the same element,
  so it is not credentials. Go straight to `write_featurescript_feature`; do not
  spend a session re-debugging this.
- **`Draft 1` in the `top` feature tree is original geometry**, a taper on the
  case walls — not a leftover draft. Do not delete it when cleaning up.

See [README.md](README.md) for the models, element IDs, and which Feature
Studios are currently load-bearing.

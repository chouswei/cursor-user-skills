# Core pandas principles (token-optimized)

## Performance & Vectorization

- **No Manual Loops:** Never use `for index, row in df.iterrows()`. Use vectorized Series operations instead.
- **Avoid `.apply()`:** Use built-in vectorized methods (e.g., `df['a'] + df['b']`) instead of `df.apply(lambda x: x['a'] + x['b'], axis=1)`.
- **In-place is Deprecated:** Avoid `inplace=True`. It rarely saves memory and breaks method chaining. Use `df = df.method()` instead.
- **Vectorized String Ops:** Use `.str` accessor for string manipulations rather than manual parsing.

## Memory Management

- **Categoricals:** Convert low-cardinality string columns to `category` dtype to save up to 90% memory.
- **Downcasting:** Use `pd.to_numeric(..., downcast='integer')` for large datasets to save space.
- **Chunking:** For files larger than RAM, use `chunksize` in `pd.read_csv()`.

## I/O Optimization

- **Parquet over CSV:** Always prefer `.parquet` (via `pyarrow`) for intermediate storage. It preserves types and is significantly faster.
- **Fast Engines:** Use `engine='pyarrow'` in `read_csv` and `to_csv` where available.

## Indexing & Selection

- **Explicit Access:** Prefer `.loc` and `.iloc` over "chained indexing" (e.g., `df[df.a > 1]['b']`) to avoid `SettingWithCopyWarning`.
- **Booleans:** Use boolean masks for filtering rather than multiple `.query()` calls for performance-critical code.

## Retrieval seeds (keyword hooks)

pandas, dataframe, series, vectorized, apply, iterrows, read_csv, read_parquet, parquet, loc, iloc, category, memory, performance, aggregation, grouping, merge, join, cleaning
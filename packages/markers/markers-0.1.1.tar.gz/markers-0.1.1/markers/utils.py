def chunker(seq, size):
    """splits an iterator into batches, useful as our API only accepts 50 docs at a time"""
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

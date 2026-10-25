"""Report where an assistant session spent its tokens.

Reads one Claude Code session transcript (the main JSONL file and the
subagent and workflow transcripts in the directory of the same name) and
prints the weighted token use by scope, by component, by day, and by the
tool results that filled the context.

Weights are relative to the price of one uncached input token:
uncached input 1, cache write 1.25 (5 minutes) or 2 (1 hour),
cache read 0.1, output 5.

usage: python usage_report.py <session.jsonl> [--tz-hours 9] [--top 15]

Only the Python standard library is used. Nothing is sent anywhere.
"""
import argparse
import collections
import glob
import json
import os
import re
import statistics
from datetime import datetime, timedelta


def weighted(u):
    cc = u.get('cache_creation') or {}
    if cc:
        w5 = cc.get('ephemeral_5m_input_tokens', 0) or 0
        w1 = cc.get('ephemeral_1h_input_tokens', 0) or 0
    else:
        w5, w1 = u.get('cache_creation_input_tokens', 0) or 0, 0
    return {
        'input': u.get('input_tokens', 0) or 0,
        'write': w5 * 1.25 + w1 * 2,
        'read': (u.get('cache_read_input_tokens', 0) or 0) * 0.1,
        'output': (u.get('output_tokens', 0) or 0) * 5,
    }


def context_size(u):
    return sum(u.get(k, 0) or 0 for k in
               ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens'))


def result_chars(content):
    if isinstance(content, str):
        return len(content), 0
    n = img = 0
    for x in content or []:
        if isinstance(x, dict):
            if x.get('type') == 'text':
                n += len(x.get('text', ''))
            elif x.get('type') == 'image':
                img += 1
    return n, img


def first_command(cmd):
    for part in re.split(r'&&|;|\n|\|', cmd):
        w = part.strip()
        if not w or w.startswith(('cd ', 'export ', '#')) or re.match(r'^[A-Z_]+=', w):
            continue
        return os.path.basename(w.split()[0].strip('"\''))
    return '(none)'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('session')
    ap.add_argument('--tz-hours', type=float, default=9)
    ap.add_argument('--top', type=int, default=15)
    a = ap.parse_args()

    base = a.session[:-len('.jsonl')]
    files = [('main', a.session)]
    files += [('helper', p) for p in glob.glob(os.path.join(base, 'subagents', '*.jsonl'))]
    files += [('workflow', p) for p in glob.glob(os.path.join(base, 'subagents', 'workflows', '*', '*.jsonl'))]

    comp = collections.defaultdict(collections.Counter)
    ctx = collections.defaultdict(list)
    day = collections.Counter()
    tool_chars = collections.defaultdict(collections.Counter)
    tool_n = collections.defaultdict(collections.Counter)
    images = collections.Counter()
    read_chars, read_n = collections.Counter(), collections.Counter()
    cmd_chars, cmd_n = collections.Counter(), collections.Counter()
    agents = collections.Counter()
    compactions = 0

    for scope, path in files:
        tools = {}
        usage = {}
        with open(path, encoding='utf-8') as f:
            for line in f:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                if scope == 'main' and d.get('type') == 'system' and d.get('subtype') == 'compact_boundary':
                    compactions += 1
                m = d.get('message')
                if not isinstance(m, dict):
                    continue
                if d.get('type') == 'assistant':
                    if m.get('usage'):
                        usage[m.get('id') or d.get('requestId')] = (m['usage'], d.get('timestamp', ''))
                    for b in m.get('content') or []:
                        if isinstance(b, dict) and b.get('type') == 'tool_use':
                            inp = b.get('input') or {}
                            key = inp.get('file_path', '') if b['name'] == 'Read' else (
                                first_command(inp.get('command', '')) if b['name'] in ('Bash', 'PowerShell') else '')
                            tools[b['id']] = (b['name'], key)
                elif d.get('type') == 'user' and isinstance(m.get('content'), list):
                    for b in m['content']:
                        if not (isinstance(b, dict) and b.get('type') == 'tool_result'):
                            continue
                        name, key = tools.get(b.get('tool_use_id'), ('?', ''))
                        n, img = result_chars(b.get('content'))
                        tool_chars[scope][name] += n
                        tool_n[scope][name] += 1
                        images[scope] += img
                        if name == 'Read':
                            k = os.path.basename(key.replace('\\', '/'))
                            read_chars[k] += n
                            read_n[k] += 1
                        elif name in ('Bash', 'PowerShell'):
                            cmd_chars[key] += n
                            cmd_n[key] += 1
        if scope != 'main' and usage:
            agents[scope] += 1
        for u, ts in usage.values():
            w = weighted(u)
            comp[scope].update(w)
            ctx[scope].append(context_size(u))
            if ts:
                t = datetime.fromisoformat(ts.replace('Z', '+00:00')) + timedelta(hours=a.tz_hours)
                day[t.date().isoformat()] += sum(w.values())

    total = sum(sum(c.values()) for c in comp.values()) or 1

    def pct(x):
        return f'{100 * x / total:5.1f}%'

    calls = sum(len(v) for v in ctx.values())
    print(f'Weighted total: {total / 1e6:.1f}M input-token equivalents over {calls} calls')
    print()
    print('By scope and component (share of the weighted total)')
    print(f'  {"scope":9s} {"total":>7s} {"read":>7s} {"write":>7s} {"output":>7s} {"input":>7s}  calls  agents  median context')
    for s in ('main', 'helper', 'workflow'):
        if s not in comp:
            continue
        c = comp[s]
        print(f'  {s:9s} {pct(sum(c.values()))} {pct(c["read"])} {pct(c["write"])} {pct(c["output"])} {pct(c["input"])}  '
              f'{len(ctx[s]):5d}  {agents[s] or "":>6}  {statistics.median(ctx[s]):>13,.0f}')
    if ctx['main']:
        m = sorted(ctx['main'])
        print(f'  main context p90 {m[int(0.9 * len(m))]:,}, max {m[-1]:,}, compactions {compactions}')
    print()
    print('By day')
    for d in sorted(day):
        print(f'  {d}  {pct(day[d])}')
    for s in ('main', 'helper', 'workflow'):
        if not tool_chars[s]:
            continue
        print()
        print(f'Tool results in scope {s} (characters; images {images[s]})')
        tot = sum(tool_chars[s].values()) or 1
        for name, n in tool_chars[s].most_common(6):
            print(f'  {name:12s} {n / 1e6:6.2f}M  {100 * n / tot:5.1f}%  results {tool_n[s][name]}')
    print()
    print('Files read most (all scopes, characters returned)')
    for k, n in read_chars.most_common(a.top):
        print(f'  {n / 1e3:7.0f}k  reads {read_n[k]:4d}  {k}')
    print()
    print('Shell commands by first command (all scopes, characters returned)')
    for k, n in cmd_chars.most_common(10):
        print(f'  {n / 1e6:6.2f}M  runs {cmd_n[k]:5d}  {k[:30]}')


if __name__ == '__main__':
    main()

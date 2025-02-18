#!/usr/bin/env python3
from finetune.LLaMA_Factory.run import run_chat
from fingerprint.Model-Fingerprint import run

def main():
    run_chat()
    run()

if __name__ == "__main__":
    main()
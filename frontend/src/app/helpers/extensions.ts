import { Extensions } from '@tiptap/core';
import { TaskItem } from '@tiptap/extension-task-item';
import { TaskList } from '@tiptap/extension-task-list';
import { TextAlign } from '@tiptap/extension-text-align';
import { Underline } from '@tiptap/extension-underline';
import StarterKit from '@tiptap/starter-kit';
import { NgxLink, TipBaseExtension } from 'ngx-tiptap-editor';

export const extensions: Extensions = [StarterKit, Underline, TextAlign.configure({types: ['paragraph', 'heading']}), TaskList, TaskItem.configure({nested: true})];
export const angularExtensions = [TipBaseExtension.create(NgxLink, {})];

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 20:19:44 2016

@author: Bang
"""
from itertools import groupby, chain
from connect_four import diagonals_pos as diag_pos
from connect_four import diagonals_neg as diag_neg
import numpy as np


NONE = 0
RED = 1
YELLOW = 2  


def evaluate(board, player, cols, rows):

    lines = (
        board,  # columns
        zip(*board),  # rows
        diag_pos(board, cols, rows),  # positive diagonals
        diag_neg(board, cols, rows)  # negative diagonals
    )
    
    score = 0

    for line in chain(*lines):
        for color in range(1, 3):
            if color == player:
                cluster_list = find_clusters(line, color)
                line_score = 0
                for cluster in cluster_list:
                    if cluster.max_filled == 1:
                        cluster_score = 10
                    elif cluster.max_filled == 2:
                        cluster_score = 100
                    elif cluster.max_filled == 3:
                        cluster_score = 1000
                    elif cluster.max_filled >= 4:
                        cluster_score = 10000

                    # if cluster.length + cluster.open_end + cluster.open_start < 4:
                    #     cluster_score = 0
                    # else:
                    cluster_score += 5 * (cluster.open_end + cluster.open_start)*(2 ** cluster.max_filled)

                    line_score += cluster_score
            else:
                cluster_list = find_clusters(line, color)
                line_score = 0
                for cluster in cluster_list:
                    if cluster.max_filled == 1:
                        cluster_score = -999
                    elif cluster.max_filled == 2:
                        cluster_score = -99999
                    elif cluster.max_filled == 3:
                        cluster_score = -9999999
                    elif cluster.max_filled >= 4:
                        cluster_score = -999999999

                    # if cluster.length + cluster.open_end + cluster.open_start < 4:
                    #     cluster_score = 0
                    # else:
                    cluster_score -= 100 * (cluster.open_end + cluster.open_start)* (10 ** cluster.max_filled)
                    line_score += cluster_score

            score += line_score

    return score


def find_clusters(line, player):
    # counts the consecutive number of pieces in a line, which may be a row, column, or diagonal
    consecutive_counter = 0
    no_gap_clusters = list()
    cluster_list = list()
    merge_counter = 0

    # find all the clusters that contain no internal gaps
    ind = 0
    while ind < len(line):
        if line[ind] == player:
            start_ind = ind
            free_start = find_free_space_before(line, start_ind)
            consecutive_counter += 1
            ind += 1
            while ind < len(line):
                if line[ind] == player:
                    consecutive_counter += 1
                    ind += 1
                else:
                    break
            stop_ind = ind
            free_end = find_free_space_after(line, ind - 1)
            no_gap_clusters.append(Cluster(start_ind, stop_ind, free_start, free_end, consecutive_counter, consecutive_counter, 0, 0, 1))
        ind += 1
    cluster_list.extend(no_gap_clusters)
    # there may be no clusters in this line so check
    if len(cluster_list) == 0:
        return cluster_list

    prev_merged_clusters = cluster_list

    # merge the clusters if possible
    while prev_merged_clusters[0].stop_ind < no_gap_clusters[-1].start_ind:
        next_merged_clusters = list()
        for i in range(len(prev_merged_clusters)):
            for j in range(len(no_gap_clusters)):
                if prev_merged_clusters[i].stop_ind < no_gap_clusters[j].start_ind:
                    merged = prev_merged_clusters[i].merge(no_gap_clusters[j],line)
                    if merged is not None:
                        next_merged_clusters.append(merged)
                        merge_counter += 1
        cluster_list.extend(next_merged_clusters)
        prev_merged_clusters = next_merged_clusters
        if len(prev_merged_clusters) == 0:
            return cluster_list

    return cluster_list


def find_free_space_before(line, start_index):
    # counts the number of free spaces in the line before the start index
    counter = 0
    index = start_index - 1
    while index >= 0:
        if line[index] == 0:
            counter += 1
        else:
            break
        index -= 1
    return counter


def find_free_space_after(line, start_index):
    # counts the number of free spaces in the line before the start index
    counter = 0
    index = start_index + 1
    while index < len(line):
        if line[index] == 0:
            counter += 1
        else:
            break
        index += 1
    return counter


class Cluster:
    def __init__(self, start_ind, stop_ind, open_start, open_end, total_filled, max_filled, total_gap, max_gap, segments):
        self.start_ind = start_ind  # the start index of the first filled position in the cluster of a particular line
        self.stop_ind = stop_ind  # the start index of the first filled position in the cluster of a particular line
        self.length = total_filled + total_gap  # total length of cluster without the unoccupied spaces before or after
        self.total_filled = total_filled  # total number of positions filled within cluster
        self.max_filled = max_filled  # the maximum length of consecutively filled positions within cluster
        self.open_start = open_start  # the number of unoccupied positions before the start_ind
        self.open_end = open_end  # the number of unoccupied positions before the stop_ind
        self.total_gap = total_gap   # total number of unoccupied positions within cluster
        self.max_gap = max_gap  # the maximum length of consecutively filled positions within cluster
        self.segments = segments # the number of islands of filled positions within cluster

    def merge(self, other, line):
        # method to merge to non-overlapping clusters. Will only merge if there all position between clusters are
        # unoccupied

        if self == other:
            return self
        else:
            stop_gap_ind = max(self.start_ind, other.start_ind)
            start_gap_ind = min(self.stop_ind, other.stop_ind)
            # check line to make sure that positions between the clusters are unoccupied
            gap_counter = 0
            for i in range(start_gap_ind, stop_gap_ind):
                if line[i] != 0:
                    return
                else:
                    gap_counter += 1

            start_ind = min(self.start_ind, other.start_ind)
            stop_ind = max(self.stop_ind, other.stop_ind)
            first_cluster = np.argmin([self.start_ind, other.start_ind])
            if first_cluster == 0:
                open_start = self.open_start
                open_end = other.open_end
            else:
                open_start = other.open_start
                open_end = self.open_end

            total_filled = self.total_filled + other.total_filled
            max_filled = max(self.max_filled, other.max_filled)
            total_gap = self.total_gap + other.total_gap + gap_counter
            max_gap = max(self.max_gap, other.max_gap, gap_counter)
            segments = self.segments + other.segments + 1

            return Cluster(start_ind, stop_ind, open_start, open_end, total_filled, max_filled, total_gap, max_gap, segments)
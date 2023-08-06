#pragma once
#include "pattern2.h"
#include "incubator.h"
#include <unordered_map>
#include <set>

/*
* This contains code from apgmera, minus the dependence on Golly, for
* separating and classifying objects.
*/

namespace apg {

    template<int M>
    class base_classifier {

        public:

        bool b0;
        uint64_t gmax;
        uint8_t transtable[512];
        std::string rule;
        std::string zoi;
        lifetree_abstract<uint32_t>* lab;
        lifetree<uint32_t, M + 1> lh;
        std::unordered_map<uint64_t, std::string> bitcache;
        std::unordered_map<std::string, std::vector<std::string> > decompositions;

        bool diagbirth() {
            /*
            * Does birth occur in either of the following situations?
            *  o..    ..o
            *  ... or ...
            *  ..o    o..
            */

            return (transtable[257] || transtable[68] || b0);
        }

        std::vector<std::string> pbbosc(pattern pat, uint64_t n, uint64_t maxn) {
            /*
            * Exhaustively search all partitions of an oscillator into
            * n disjoint unions of islands to check whether this is a
            * pseudo-oscillator.
            */

            std::vector<std::string> apgcodes;

            uint64_t period = pat.ascertain_period();
            pattern hist(&lh, "", rule + "History");
            hist += pat;
            hist = hist[period + 2];
            bitworld lrem = hist.flatlayer(0);
            bitworld env = hist.flatlayer(1);

            apg::pattern clunion(lab, lab->demorton(lrem, 1), rule);

            std::vector<pattern> clusters;
            while (lrem.population() != 0) {
                bitworld cluster = grow_cluster(lrem.get1cell(), env, "9");
                lrem -= cluster;
                apg::pattern ppart(lab, lab->demorton(cluster, 1), rule);
                clusters.push_back(ppart & clunion);
            }

            uint64_t islcount = clusters.size();

            if (islcount < n) { apgcodes.push_back(pat.apgcode()); return apgcodes; }

            uint64_t bftime = modexp_u64(n, islcount, -1);
            if (((period + 2) * bftime) > 1000000) {
                // std::cerr << pat.apgcode() << " would take infeasibly long to brute-force separate." << std::endl;
                apgcodes.push_back(pat.apgcode());
                return apgcodes;
            }

            std::vector<uint8_t> currstack(islcount);
            std::vector<uint8_t> maxstack(islcount);

            currstack[0] = 0;
            currstack[1] = 0;
            maxstack[0] = 0;

            uint64_t focus = 1;
            while (focus) {

                uint8_t limit = maxstack[focus - 1] + 1;
                limit = (limit >= n) ? (n - 1) : limit;
                // for (uint64_t i = 0; i <= focus; i++) {
                //     std::cerr << " " << ((int) currstack[i]);
                // }
                // std::cerr << std::endl;
                if (currstack[focus] > limit) {
                    focus -= 1;
                    currstack[focus] += 1;
                } else {

                    maxstack[focus] = maxstack[focus - 1];
                    if (maxstack[focus] < currstack[focus]) { maxstack[focus] = currstack[focus]; }
                    if (focus < (islcount - 1)) {
                        focus += 1;
                        currstack[focus] = 0;
                    } else {
                        if (maxstack[focus] == n - 1) {
                            // We have a n-colouring which uses all n colours:
                            std::vector<pattern> unions;
                            for (uint64_t i = 0; i < n; i++) { unions.push_back(pattern(lab, "", rule)); }
                            for (uint64_t i = 0; i < islcount; i++) {
                                unions[currstack[i]] |= clusters[i];
                            }
                            bool faithful = true;
                            for (uint64_t i = 0; i <= period; i++) {
                                apg::pattern x = unions[0];
                                unions[0] = unions[0][1];
                                if ((unions[0]).empty()) { faithful = false; break; }
                                for (uint64_t j = 1; j < n; j++) {
                                    if ((unions[j]).empty()) { faithful = false; break; }
                                    if ((x & unions[j]).nonempty()) { faithful = false; break; }
                                    x |= unions[j];
                                    unions[j] = unions[j][1];
                                }
                                if (x != clunion[i]) { faithful = false; break; }
                                if (faithful == false) { break; }
                            }
                            if (faithful) {
                                // We have a decomposition into non-interacting pieces!
                                for (uint64_t i = 0; i < n; i++) {
                                    std::vector<std::string> tx = pbbosc(unions[i], 2, maxn);
                                    for (uint64_t j = 0; j < tx.size(); j++) {
                                        apgcodes.push_back(tx[j]);
                                    }
                                }
                                return apgcodes;
                            }
                        }
                        currstack[focus] += 1;
                    }
                }
            }

            // std::cerr << " -- reached end without partition" << std::endl;

            if ((maxn == 0) || (n < maxn)) {
                // Try with more partitions:
                return pbbosc(pat, n + 1, maxn);
            } else {
                // Pattern cannot be decomposed:
                apgcodes.push_back(pat.apgcode());
                return apgcodes;
            }
        }

        std::vector<std::string> pseudoBangBang(pattern pat, std::vector<bitworld> *clvec, bool recurse) {
            /*
            * Borrowed from apgmera, and upgraded.
            */

            uint64_t period = pat.ascertain_period();
            bool isOscillator = ((pat.dx == 0) && (pat.dy == 0));
            pattern hist(&lh, "", rule + "History");
            hist += pat;
            hist = hist[period + 2];
            bitworld lrem = hist.flatlayer(0);
            bitworld env = hist.flatlayer(1);

            // If we have a moving object, do not reiterate:
            bool reiterate = isOscillator && (zoi.length() <= 2);

            std::map<std::pair<int64_t, int64_t>, uint64_t> geography;
            uint64_t label = 0;
            while (lrem.population() != 0) {
                bitworld cluster = grow_cluster(lrem.get1cell(), env, reiterate ? "9" : zoi);
                lrem -= cluster;
                label += 1;
                std::vector<std::pair<int64_t, int64_t> > celllist = cluster.getcells();
                for (uint64_t i = 0; i < celllist.size(); i++) {
                    geography[celllist[i]] = label;
                }
            }

            while (reiterate) {
                reiterate = false;
                for (uint64_t i = 0; i < period; i++) {
                    hist = hist[1];
                    bitworld lcurr = hist.flatlayer(0);
                    bitworld dcurr = bleed(lcurr, "9");
                    dcurr -= env;
                    std::vector<std::pair<int64_t, int64_t> > liberties = dcurr.getcells();
                    for (uint64_t j = 0; j < liberties.size(); j++) {
                        int64_t ix = liberties[j].first;
                        int64_t iy = liberties[j].second;
                        std::map<uint64_t, uint64_t> tally;
                        for (int64_t ux = 0; ux <= 2; ux++) {
                            for (int64_t uy = 0; uy <= 2; uy++) {
                                int value = geography[std::pair<int64_t, int64_t>(ux + ix - 1, uy + iy - 1)];
                                if (lcurr.getcell(ux + ix - 1, uy + iy - 1)) {
                                    tally[value] = tally[value] + (1 << (uy * 3 + ux));
                                }
                            }
                        }

                        uint64_t dominantColour = 0;
                        std::map<uint64_t, uint64_t>::iterator it2;
                        for (it2 = tally.begin(); it2 != tally.end(); it2++) {
                            int colour = it2->first;
                            uint64_t count = it2->second;
                            if (transtable[count]) { dominantColour = colour; }
                            // if (__builtin_popcountll(count) == 3) { dominantColour = colour; }
                        }
                        // Resolve dependencies:
                        if (dominantColour != 0) {
                            std::map<std::pair<int64_t, int64_t>, uint64_t>::iterator it3;
                            for (it3 = geography.begin(); it3 != geography.end(); it3++) {
                                std::pair<int64_t, int64_t> coords = it3->first;
                                uint64_t colour = it3->second;

                                if (tally[colour] > 0) {
                                    geography[coords] = dominantColour;
                                    if (colour != dominantColour) {
                                        // A change has occurred; keep iterating until we achieve stability:
                                        reiterate = true;
                                    }
                                }
                            }
                        }
                    }
                }
            }

            bitworld lcurr = (isOscillator ? pat.flatlayer(0) : hist.flatlayer(0));
            std::vector<bitworld> cbs(label+1);
            std::map<std::pair<int64_t, int64_t>, uint64_t>::iterator it3;
            for (it3 = geography.begin(); it3 != geography.end(); it3++) {
                std::pair<int64_t, int64_t> coords = it3->first;
                uint64_t colour = it3->second;
                cbs[colour].setcell(coords.first, coords.second, 1);
            }
            std::vector<std::string> components;
            for (uint64_t l = 1; l <= label; l++) {
                cbs[l] &= lcurr;
                if (cbs[l].population() > 0) {
                    if (clvec != 0) { clvec->push_back(cbs[l]); }
                    apg::pattern ppart(lab, lab->demorton(cbs[l], 1), rule);
                    if (isOscillator) {
                        /*
                        * Without diagbirths, we only need to go up to 4 as a
                        * result of the Four Colour Theorem:
                        *
                        *   http://www.paradise.caltech.edu/~cook/Workshop/CAs/2DOutTot/Life/StillLife/FourColors.html
                        *
                        * With diagbirths, 7 may be necessary:
                        *
                        *   http://link.springer.com/article/10.1007/s10958-014-1693-6
                        *
                        * Either way, we start with 2 and increment:
                        */
                        uint64_t maxn = (zoi.length() <= 2) ? (diagbirth() ? 7 : 4) : 0;
                        std::vector<std::string> tx = pbbosc(ppart, 2, maxn);
                        for (uint64_t j = 0; j < tx.size(); j++) {
                            components.push_back(tx[j]);
                        }
                        // std::cerr << "done!" << std::endl;
                    } else if (recurse) {
                        auto cmap = census(ppart, ppart.ascertain_period(), 0, false);
                        if (cmap.size() == 0) {
                            std::cerr << "Warning: " << ppart.apgcode() << " gave empty census." << std::endl;
                            components.push_back(ppart.apgcode());
                        }
                        for (auto it = cmap.begin(); it != cmap.end(); ++it) {
                            for (int i = 0; i < it->second; i++) {
                                components.push_back(it->first);
                            }
                        }
                    } else {
                        components.push_back(ppart.apgcode());
                    }
                }
            }

            for (auto it = components.begin(); it != components.end(); ++it) {
                if ((*it) == "PATHOLOGICAL") {
                    // invalid separation
                    std::vector<std::string> newcomps;
                    newcomps.push_back(pat.apgcode());
                    return newcomps;
                }
            }

            return components;
        }

        /*
        * Compute the degree sequence of the graph where vertices are live
        * cells and edges denote adjacency. Concatenate the resulting
        * sequences for each generation.
        */
        void degcount(pattern pat, int *degrees, int generations) {

            pattern x = pat;
            for (int i = 0; i < generations; i++) {
                for (int j = 0; j < 9; j++) { degrees[9*i + j] = 0; }
                bitworld bw = x.flatlayer(0);
                x = x[1];

                std::vector<std::pair<int64_t, int64_t> > celllist = bw.getcells();
                std::set<std::pair<int64_t, int64_t> > cellset;
                for (uint64_t k = 0; k < celllist.size(); k++) {
                    cellset.insert(celllist[k]);
                }
                for (uint64_t k = 0; k < celllist.size(); k++) {
                    int64_t x = celllist[k].first;
                    int64_t y = celllist[k].second;

                    int degree = -1;

                    for (int64_t ix = x - 1; ix <= x + 1; ix++) {
                        for (int64_t iy = y - 1; iy <= y + 1; iy++) {
                            degree += cellset.count(std::pair<int64_t, int64_t>(ix, iy));
                        }
                    }

                    degrees[9*i + degree] += 1;
                }
            }
        }

        /*
        * Separate a collection of period-4 standard spaceships:
        */
        std::vector<std::string> sss(apg::pattern pat) {

            std::vector<std::string> components;

            int degrees[36];
            degcount(pat, degrees, 4);

            for (int i = 0; i < 18; i++) {
                if (degrees[i] != degrees[18+i]) { return components; }
            }

            int hwssa[18] = {1,4,6,2,0,0,0,0,0,0,0,0,4,4,6,1,2,1};
            int mwssa[18] = {2,2,5,2,0,0,0,0,0,0,0,0,4,4,4,1,2,0};
            int lwssa[18] = {1,2,4,2,0,0,0,0,0,0,0,0,4,4,2,2,0,0};
            int hwssb[18] = {0,0,0,4,4,6,1,2,1,1,4,6,2,0,0,0,0,0};
            int mwssb[18] = {0,0,0,4,4,4,1,2,0,2,2,5,2,0,0,0,0,0};
            int lwssb[18] = {0,0,0,4,4,2,2,0,0,1,2,4,2,0,0,0,0,0};
            int glida[18] = {0,1,2,1,1,0,0,0,0,0,2,1,2,0,0,0,0,0};
            int glidb[18] = {0,2,1,2,0,0,0,0,0,0,1,2,1,1,0,0,0,0};

            int hacount = degrees[17];
            int macount = degrees[16]/2 - hacount;
            int lacount = (degrees[15] - hacount - macount)/2;
            int hbcount = degrees[8];
            int mbcount = degrees[7]/2 - hbcount;
            int lbcount = (degrees[6] - hbcount - mbcount)/2;

            int gacount = 0;
            int gbcount = 0;

            if ((lacount == 0) && (lbcount == 0) && (macount == 0) && (mbcount == 0) && (hacount == 0) && (hbcount == 0)) {
                gacount = degrees[4];
                gbcount = degrees[13];
            }

            for (int i = 0; i < 18; i++) {
                int putativedegrees = 0;
                putativedegrees += hacount * hwssa[i];
                putativedegrees += hbcount * hwssb[i];
                putativedegrees += lacount * lwssa[i];
                putativedegrees += lbcount * lwssb[i];
                putativedegrees += macount * mwssa[i];
                putativedegrees += mbcount * mwssb[i];
                putativedegrees += gacount * glida[i];
                putativedegrees += gbcount * glidb[i];
                if (degrees[i] != putativedegrees) { return components; }
            }

            int hcount = 0;
            int lcount = 0;
            int mcount = 0;
            int gcount = 0;

            if (hacount >= 0 && hbcount >= 0) { hcount = hacount + hbcount; } else { return components; }
            if (macount >= 0 && mbcount >= 0) { mcount = macount + mbcount; } else { return components; }
            if (lacount >= 0 && lbcount >= 0) { lcount = lacount + lbcount; } else { return components; }
            if (gacount >= 0 && gbcount >= 0) { gcount = gacount + gbcount; } else { return components; }

            for (int i = 0; i < gcount; i++) { components.push_back("xq4_153"); }
            for (int i = 0; i < lcount; i++) { components.push_back("xq4_6frc"); }
            for (int i = 0; i < mcount; i++) { components.push_back("xq4_27dee6"); }
            for (int i = 0; i < hcount; i++) { components.push_back("xq4_27deee6"); }

            return components;

        }

        std::vector<bitworld> getclusters(bitworld &live, bitworld &env, bool rigorous) {

            bitworld lrem = live;
            std::vector<bitworld> clusters;

            while (lrem.population() != 0) {
                // Obtain cluster:
                bitworld cluster = grow_cluster(lrem.get1cell(), env, zoi);
                cluster &= lrem;
                lrem -= cluster;
                if (rigorous) {
                    pattern ppart(lab, lab->demorton(cluster, 1), rule);
                    pseudoBangBang(ppart, &clusters, false);
                } else {
                    clusters.push_back(cluster);
                }
            }

            return clusters;
        }

        // Forward declaration for co-recursive function:
        // std::map<std::string, int64_t> census(pattern pat, int numgens, std::string (*adv)(pattern), bool recurse);

        std::pair<bool, std::vector<std::string> > identify(uint64_t bb, std::vector<bitworld> &cplanes, bool recurse) {

            std::string repr;
            std::vector<std::string> elements;

            if ((bb != 0) && (bitcache.find(bb) != bitcache.end())) {
                repr = bitcache[bb];
                elements = decompositions[repr];
                return std::pair<bool, std::vector<std::string> >(true, elements);
            }

            if (cplanes.size() == 0) {
                cplanes.resize(1);
                cplanes[0].world.emplace(std::pair<int32_t, int32_t>(0, 0), bb);
            }

            apg::pattern cl2(lab, cplanes, rule);
            cl2.pdetect(gmax); // Restrict period.

            if (cl2.dt == 0) {
                return std::pair<bool, std::vector<std::string> >(false, elements);
            }

            repr = cl2.apgcode();
            auto it = decompositions.find(repr);
            if (it != decompositions.end()) {
                elements = it->second;
            } else {
                uint64_t period = cl2.ascertain_period();
                if ((M == 1) && (!b0)) {
                    // 2-state rule:
                    if ((zoi.length() <= 2) && (period == 4) && ((cl2.dx != 0) || (cl2.dy != 0))) {
                        // Separating standard spaceships is considerably
                        // faster and more reliable with sss; only fall
                        // back on pbb if this fails:
                        elements = sss(cl2);
                    }
                    if (elements.size() == 0) { elements = pseudoBangBang(cl2, 0, recurse); }
                } else if (recurse && (!b0)) {
                    // We may have a constellation since we've bypassed PseudoBangBang.
                    // This tends to be problematic in B0 and Generations rules with
                    // infinite-growth patterns, so we try to reseparate the pattern:
                    uint64_t period = cl2.ascertain_period();
                    std::map<std::string, int64_t> rc = census(cl2, period << 3, 0, false);
                    for (auto it2 = rc.begin(); it2 != rc.end(); ++it2) {
                        if (it2->second > 0) {
                            for (int64_t i = 0; i < it2->second; i++) {
                                elements.push_back(it2->first);
                            }
                        }
                    }
                } else {
                    // PseudoBangBang not supported for multistate rules; skip separation:
                    elements.push_back(repr);
                }
                decompositions[repr] = elements;
            }

            if (bb != 0) {
                bitcache.emplace(bb, repr);
            }
            
            return std::pair<bool, std::vector<std::string> >(true, elements);
        }

        template<int H>
        void deeppurge(std::map<std::string, int64_t> &cm, incubator<56, H> &icb, std::string (*adv)(pattern),
                        bool remove_annoyances, bool remove_gliders) {

            uint64_t excess[8] = {0ull};

            for (auto it = icb.tiles.begin(); it != icb.tiles.end(); ++it) {
                Incube<56, H>* sqt = &(it->second);
                for (int y = 0; y < H; y++) {
                    uint64_t r = sqt->d[y];
                    while (r != 0) {
                        uint64_t x = __builtin_ctzll(r);
                        int annoyance = (remove_annoyances ? icb.isAnnoyance(sqt, x, y) : 0);
                        if (annoyance > 0) {
                            excess[annoyance] += 1;
                        } else if ((!remove_gliders) || (icb.isGlider(sqt, x, y) == 0)) {
                            // TODO: Identify unknown object
                            auto intList = icb.get_component(sqt, x, y);
                            int population = intList.back();
                            int ll = intList.size() - 1;
                            if (population > 0) {
                                if ((remove_annoyances) && (population == 3)) {
                                    excess[3] += 1;
                                } else if ((remove_annoyances) && (population == 5)) {
                                    if (ll == 15) {
                                        excess[7] += 1;
                                    } else {
                                        excess[5] += 1;
                                    }
                                } else {
                                    std::vector<int> celllist(population*2);
                                    int i = 0;
                                    for (int j = 0; j < ll; j += 3) {
                                        if (intList[j + 2] == 1) {
                                            celllist[i++] = intList[j];
                                            celllist[i++] = intList[j+1];
                                        }
                                    }

                                    int left = celllist[0];
                                    int top = celllist[1];
                                    int right = celllist[0];
                                    int bottom = celllist[1];

                                    for (int i = 0; i < (population*2); i += 2) {
                                        if (left > celllist[i]) { left = celllist[i]; }
                                        if (right < celllist[i]) { right = celllist[i]; }
                                        if (top > celllist[i+1]) { top = celllist[i+1]; }
                                        if (bottom < celllist[i+1]) { bottom = celllist[i+1]; }
                                    }

                                    for (int i = 0; i < (population*2); i += 2) {
                                        celllist[i] -= left;
                                        celllist[i+1] -= top;
                                    }

                                    right -= left;
                                    bottom -= top;

                                    uint64_t bitstring = 0;
                                    std::vector<bitworld> cplanes;

                                    if (right <= 7 && bottom <= 7) {
                                        for (int i = 0; i < (population*2); i += 2) {
                                            bitstring |= (1ull << (celllist[i] + 8*celllist[i+1]));
                                        }
                                    } else {
                                        cplanes.resize(1);
                                        for (int i = 0; i < (population*2); i += 2) {
                                            cplanes[0].setcell(celllist[i], celllist[i+1], 1);
                                        }
                                    }

                                    std::pair<bool, std::vector<std::string> > res = identify(bitstring, cplanes, true);

                                    if (!(res.first)) {
                                        apg::pattern cl2(lab, cplanes, rule);
                                        std::string diagnosed = "PATHOLOGICAL";
                                        if (adv != 0) { diagnosed = (*adv)(cl2); }
                                        res.second.push_back(diagnosed);
                                    }

                                    // Enter elements into tally:
                                    for (uint64_t i = 0; i < res.second.size(); i++) {
                                        cm[res.second[i]] += 1;
                                    }
                                }
                            }
                        }
                        r ^= (1ull << x);
                        r &= sqt->d[y];
                    }
                }
            }

            if (excess[3] > 0) { cm["xp2_7"] += excess[3]; }
            if (excess[4] > 0) { cm["xs4_33"] += excess[4]; }
            if (excess[5] > 0) { cm["xq4_153"] += excess[5]; }
            if (excess[6] > 0) { cm["xs6_696"] += excess[6]; }
            if (excess[7] > 0) { cm["xs5_253"] += excess[7]; }

        }

        void census(std::map<std::string, int64_t> &tally, std::vector<bitworld> &planes, std::string (*adv)(pattern), bool recurse) {

            bitworld lrem = planes[0];
            for (uint64_t i = 1; i < M; i++) {
                lrem += planes[i];
            }
            bitworld env = lrem;
            env += planes[M];

            bool glider_plane = ((M == 1) && (planes.size() == 3));

            bitworld lrem2 = lrem;
            if (glider_plane) { lrem2 -= planes[2]; }

            while (lrem2.population() != 0) {

                // Obtain cluster:
                bitworld cluster = grow_cluster(lrem2.get1cell(), env, zoi);
                cluster &= lrem;
                lrem -= cluster;
                lrem2 -= cluster;

                uint64_t bb = 0;

                if (M == 1) {
                    if (cluster.world.size() > 1) { cluster = fix_topleft(cluster); }
                    if (cluster.world.size() == 1) {
                        // We use a bitcache for fast lookup of small objects:
                        auto it = cluster.world.begin(); bb = it->second;
                    }
                }

                std::vector<bitworld> cplanes;

                if (bb == 0) {
                    for (uint64_t i = 0; i < M; i++) {
                        cplanes.push_back(cluster);
                        if (M != 1) { cplanes.back() &= planes[i]; }
                    }
                }

                std::pair<bool, std::vector<std::string> > res = identify(bb, cplanes, recurse);

                if (!(res.first)) {
                    apg::pattern cl2(lab, cplanes, rule);
                    std::string diagnosed = "PATHOLOGICAL";
                    if (adv != 0) { diagnosed = (*adv)(cl2); }
                    res.second.push_back(diagnosed);
                }

                // Enter elements into tally:
                for (uint64_t i = 0; i < res.second.size(); i++) {
                    tally[res.second[i]] += 1;
                }
            }

            if (lrem.population() > 0) { tally["xq4_153"] += (lrem.population() / 5); }

        }

        std::map<std::string, int64_t> census(std::vector<bitworld> &planes, std::string (*adv)(pattern), bool recurse) {
            std::map<std::string, int64_t> tally;
            census(tally, planes, adv, recurse);
            return tally;
        }

        std::map<std::string, int64_t> census(std::vector<bitworld> &planes, std::string (*adv)(pattern)) {
            return census(planes, adv, true);
        }

        std::map<std::string, int64_t> census(bitworld &live, bitworld &env, std::string (*adv)(pattern)) {
            std::vector<bitworld> bwv;
            bwv.push_back(live); bwv.push_back(env);
            return census(bwv, adv);
        }

        std::map<std::string, int64_t> census(bitworld &live, bitworld &env) {
            return census(live, env, 0);
        }

        std::map<std::string, int64_t> census(pattern pat, int numgens, std::string (*adv)(pattern), bool recurse) {
            pattern hist(&lh, "", rule + "History");
            hist += pat;
            hist = hist[numgens];
            std::vector<bitworld> bwv;
            for (uint64_t i = 0; i <= M; i++) { bwv.push_back(hist.flatlayer(i)); }
            return census(bwv, adv, recurse);
        }

        std::map<std::string, int64_t> census(pattern pat, int numgens, std::string (*adv)(pattern)) {
            return census(pat, numgens, adv, true);
        }

        std::map<std::string, int64_t> census(pattern pat, int numgens) {
            return census(pat, numgens, 0);
        }

        base_classifier(lifetree_abstract<uint32_t>* lab, std::string rule) : lh(100)
        {
            this->lab = lab;
            this->rule = rule;
            gmax = 1048576;

            /*
            * We construct the transition table by bootstrapping: we run a
            * pattern containing all 512 3-by-3 tiles and examine the
            * centre cells of the tiles after one generation.
            */
            std::string transrle = "3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob"
            "5o$24bo2bo2bo2bo2bo2bo2bo2bo3bo2bo2bo2bo2bo2bo2bo2bob2ob2ob2ob2ob2ob2o"
            "b2ob2o2$3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob"
            "2o3b2obob5o$2bo2bo2bo2bo2bo2bo2bo2b2ob2ob2ob2ob2ob2ob2ob2obob2ob2ob2ob"
            "2ob2ob2ob2ob26o2$3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob"
            "5o3bo3bob2o3b2obob5o$24bo2bo2bo2bo2bo2bo2bo2bo3bo2bo2bo2bo2bo2bo2bo2bo"
            "b2ob2ob2ob2ob2ob2ob2ob2o$o2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2b"
            "o2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo$3bo3bob2o3b2obob5o3b"
            "o3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o$2bo2bo2bo2bo2bo2b"
            "o2bo2b2ob2ob2ob2ob2ob2ob2ob2obob2ob2ob2ob2ob2ob2ob2ob26o$o2bo2bo2bo2bo"
            "2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo"
            "2bo2bo2bo2bo$3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo"
            "3bob2o3b2obob5o$24bo2bo2bo2bo2bo2bo2bo2bo3bo2bo2bo2bo2bo2bo2bo2bob2ob"
            "2ob2ob2ob2ob2ob2ob2o$bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2b"
            "o2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo$3bo3bob2o3b2obob5o3bo3b"
            "ob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o$2bo2bo2bo2bo2bo2bo2b"
            "o2b2ob2ob2ob2ob2ob2ob2ob2obob2ob2ob2ob2ob2ob2ob2ob26o$bo2bo2bo2bo2bo2b"
            "o2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo"
            "2bo2bo2bo$3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bo"
            "b2o3b2obob5o$24bo2bo2bo2bo2bo2bo2bo2bo3bo2bo2bo2bo2bo2bo2bo2bob2ob2ob"
            "2ob2ob2ob2ob2ob2o$2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob"
            "2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2o$3bo3bob2o3b2obob5o3bo3bob"
            "2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o$2bo2bo2bo2bo2bo2bo2bo"
            "2b2ob2ob2ob2ob2ob2ob2ob2obob2ob2ob2ob2ob2ob2ob2ob26o$2ob2ob2ob2ob2ob2o"
            "b2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob"
            "2ob2ob2o$3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob"
            "2o3b2obob5o$24bo2bo2bo2bo2bo2bo2bo2bo3bo2bo2bo2bo2bo2bo2bo2bob2ob2ob2o"
            "b2ob2ob2ob2ob2o$2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo"
            "2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo$3bo3bob2o3b2obob5o3bo3bob2o"
            "3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o$2bo2bo2bo2bo2bo2bo2bo2b"
            "2ob2ob2ob2ob2ob2ob2ob2obob2ob2ob2ob2ob2ob2ob2ob26o$2bo2bo2bo2bo2bo2bo"
            "2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo2bo"
            "2bo2bo2bo$3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bo"
            "b2o3b2obob5o$24bo2bo2bo2bo2bo2bo2bo2bo3bo2bo2bo2bo2bo2bo2bo2bob2ob2ob"
            "2ob2ob2ob2ob2ob2o$ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2o"
            "b2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2obo$3bo3bob2o3b2obob5o3bo3bob"
            "2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o$2bo2bo2bo2bo2bo2bo2bo"
            "2b2ob2ob2ob2ob2ob2ob2ob2obob2ob2ob2ob2ob2ob2ob2ob26o$ob2ob2ob2ob2ob2ob"
            "2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob"
            "2ob2ob2obo$3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3b"
            "ob2o3b2obob5o$24bo2bo2bo2bo2bo2bo2bo2bo3bo2bo2bo2bo2bo2bo2bo2bob2ob2ob"
            "2ob2ob2ob2ob2ob2o$b2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob"
            "2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2o$3bo3bob2o3b2obob5o3bo3bob"
            "2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o$2bo2bo2bo2bo2bo2bo2bo"
            "2b2ob2ob2ob2ob2ob2ob2ob2obob2ob2ob2ob2ob2ob2ob2ob26o$b2ob2ob2ob2ob2ob"
            "2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob2ob"
            "2ob2ob2ob2o$3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo"
            "3bob2o3b2obob5o$24bo2bo2bo2bo2bo2bo2bo2bo3bo2bo2bo2bo2bo2bo2bo2bob2ob"
            "2ob2ob2ob2ob2ob2ob2o$96o$3bo3bob2o3b2obob5o3bo3bob2o3b2obob5o3bo3bob2o"
            "3b2obob5o3bo3bob2o3b2obob5o$2bo2bo2bo2bo2bo2bo2bo2b2ob2ob2ob2ob2ob2ob"
            "2ob2obob2ob2ob2ob2ob2ob2ob2ob26o$96o!";


            b0 = false;
            std::string subrule = rule;

            // Strip Generations prefix:
            if (subrule[0] == 'g') {
                subrule = subrule.substr(1);
                while ((subrule[0] >= '0') && (subrule[1] <= '9')) {
                    subrule = subrule.substr(1);
                }
            }

            if (uli_get_family(rule2int(rule)) >= 6) {
                zoi = get_zoi(rule);
            } else if ((subrule[0] == 'b') && (subrule[1] == '0')) {
                zoi = "99"; b0 = true;
            } else if (subrule[0] == 'r') {
                zoi = std::string(2 * (subrule[1] - '0'), '9');
            } else if (subrule[0] == 'b') {
                pattern transpat(lab, transrle, rule);
                bitworld bw = transpat[1].flatlayer(0);
                for (int i = 0; i < 512; i++) {
                    int x = 3 * (i & 31) + 1;
                    int y = 3 * (i >> 5) + 1;
                    transtable[i] = bw.getcell(x, y);
                }
                zoi = (diagbirth()) ? "99" : "95";
            } else {
                zoi = get_zoi(rule);
            }
        }
    };

    typedef base_classifier<1> classifier;

}
